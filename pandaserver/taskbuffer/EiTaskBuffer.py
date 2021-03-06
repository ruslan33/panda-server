from config import panda_config

from DBProxyPool import DBProxyPool
from EiDBProxy import EiDBProxy


# logger
from pandalogger.PandaLogger import PandaLogger
_logger = PandaLogger().getLogger('EiTaskBuffer')


class EiTaskBuffer:
    """
    task queue
    
    """

    # constructor 
    def __init__(self):
        self.proxyPool = None

    # initialize
    def init(self):
        # create Proxy Pool
        if self.proxyPool == None:
            self.proxyPool = DBProxyPool(panda_config.ei_dbhost,panda_config.ei_dbpasswd,
                                         1,dbProxyClass=EiDBProxy)


    # get GUIDs from EventIndex
    def getGUIDsFromEventIndex(self,runEventList,streamName,amiTags,dataType):
        # get DB proxy
        proxy = self.proxyPool.getProxy()
        # exec
        res = proxy.getGUIDsFromEventIndex(runEventList,streamName,amiTags,dataType)
        # release DB proxy
        self.proxyPool.putProxy(proxy)
        # return
        return res



# Singleton
eiTaskBuffer = EiTaskBuffer()

