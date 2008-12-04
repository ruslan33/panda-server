import sys
import time
import datetime
from taskbuffer.DBProxy import DBProxy
import userinterface.Client as Client
from dataservice.DDM import ddm

timeL = 60
if len(sys.argv) == 2:
    timeL = int(sys.argv[1])

# password
from config import panda_config
passwd = panda_config.dbpasswd

# erase datasets
def eraseDispDatasets(ids):
    datasets = []
    # get jobs
    status,jobs = Client.getJobStatus(ids)
    if status != 0:
        return
    # gather dispDBlcoks
    for job in jobs:
        for file in job.Files:
            if not file.dispatchDBlock in datasets:
                datasets.append(file.dispatchDBlock)
    # erase
    for dataset in datasets:
        ddm.DQ2.main(['eraseDataset',datasets])

# time limit
timeLimit = datetime.datetime.utcnow() - datetime.timedelta(minutes=int(timeL))

# instantiate DB proxies
proxyS = DBProxy()
proxyS.connect(panda_config.dbhost,panda_config.dbpasswd,panda_config.dbuser,panda_config.dbname)

while True:
    # get PandaIDs
    res = proxyS.querySQL("SELECT PandaID from jobsDefined4 where jobStatus='defined' and modificationTime<'%s' and prodSourceLabel='managed' and cloud<>'NULL' ORDER BY PandaID"
                          % timeLimit.strftime('%Y-%m-%d %H:%M:%S'))
    # escape
    if len(res) == 0:
        break
    # convert to list
    jobs = []
    for id, in res:
        jobs.append(id)
    # reassign
    nJob = 100
    iJob = 0
    while iJob < len(jobs):
        print 'reassignJobs(%s)' % jobs[iJob:iJob+nJob]
        Client.reassignJobs(jobs[iJob:iJob+nJob])
        iJob += nJob
        time.sleep(120)


