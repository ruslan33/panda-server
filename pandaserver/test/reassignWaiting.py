import time
import datetime
from taskbuffer.DBProxy import DBProxy
import userinterface.Client as Client

# password
from config import panda_config
passwd = panda_config.dbpasswd

# time limit
timeLimit = datetime.datetime.utcnow() - datetime.timedelta(hours=1)

# instantiate DB proxies
proxyS = DBProxy()
proxyS.connect(panda_config.dbhost,panda_config.dbpasswd,panda_config.dbuser,panda_config.dbname)

while True:
    # get PandaIDs
    res = proxyS.querySQL("SELECT PandaID FROM jobsWaiting4 WHERE modificationTime<'%s' ORDER BY PandaID"
                          % timeLimit.strftime('%Y-%m-%d %H:%M:%S'))
    # escape
    if len(res) == 0:
        break
    # convert to list
    jobs = []
    for id, in res:
        jobs.append(id)
    # reassign
    nJob = 300
    iJob = 0
    while iJob < len(jobs):
        print 'reassignJobs(%s)' % jobs[iJob:iJob+nJob]
        Client.reassignJobs(jobs[iJob:iJob+nJob])
        iJob += nJob
        time.sleep(60)

