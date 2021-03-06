import re


# get core count
def getCoreCount(actualCoreCount,defCoreCount,jobMetrics):
    coreCount = 1
    try:
        if actualCoreCount != None:
            coreCount = actualCoreCount
        else:
            tmpMatch = None
            if jobMetrics != None:
                # extract coreCount
                tmpMatch = re.search('coreCount=(\d+)',jobMetrics)
            if tmpMatch != None:
                coreCount = long(tmpMatch.group(1))
            else:
                # use jobdef
                if not defCoreCount in [None,0]:
                    coreCount = defCoreCount
    except:
        pass
    return coreCount



# get HS06sec
def getHS06sec(startTime,endTime,baseWalltime,cpuEfficiency,corePower,coreCount):
    try:
        # no scaling
        if cpuEfficiency == 0:
            return 0
        # get execution time
        tmpTimeDelta = endTime-startTime
        tmpVal = (tmpTimeDelta.seconds+tmpTimeDelta.days*24*3600)
        # execution time is shorter than offset
        if tmpVal <= baseWalltime:
            return 0
        tmpVal = float(tmpVal-baseWalltime)*corePower*coreCount*float(cpuEfficiency)/100.0
        return tmpVal
    except:
        return None
    
