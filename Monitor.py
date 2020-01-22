import sys
from java.io import File
from java.io import FileOutputStream
from java.io import FileInputStream
from java.util import Properties
import thread
import weblogic.management.timer
from java.util import Date
from time import strftime

#=======================================================================================
# Load Properties
#=======================================================================================
def loadPropertiesFromFile(filename):
        props = addPropertiesFromFile(filename, {})
        return props

#=======================================================================================
# Load Properties
#=======================================================================================
def addPropertiesFromFile(filename, props):
    properties = Properties()
    input = FileInputStream(filename)
    properties.load(input)
    input.close()
    for entry in properties.entrySet(): props[entry.key.strip()] = entry.value.strip()
    return props

#======================================================================================

userprops = loadPropertiesFromFile("build.properties")

today = strftime("%Y-%m-%d")

global logfile
logfile = open("WLSMon%s.log"%today,"a")

global domainName

global threadIdle
threadIdle = userprops['ExecuteThreadIdleCount']

global pendingRequests
pendingRequests = userprops['PendingRequests']

global heapUsed
heapUsed = userprops['HeapUsed']

global waitSec
waitSec = userprops['WaitSecondsHighCount']

#=====================================================================================
# Monitors Server Status
#===================================================================================== 
def getRunningServerNames():
     domainConfig()
     serverNames = cmo.getServers()
     for name in serverNames:
          Name = [name.getName()] 
          print >>logfile,Date(), '%35s %9s %9s ' % ('****Info*****    Servers confgiured in ',domainName ,tuple(Name))

def checkHealth():
     svrName = server.getName()
     slBean = getSLCRT(svrName)
     status = slBean.getState()
     if status != "RUNNING":
          print >>logfile,Date(),'%16s %9s %s %9s %9s ' % ('****ERROR****    ',domainName,'.',svrName,'is down') 
     else:
          print >>logfile,Date(),'%11s %9s %s %9s %9s %9s' % ('****Info*****    ',domainName,'.',svrName,'. Status=',status)

def getSLCRT(svrName):
     domainRuntime()
     slrBean = getMBean('ServerLifeCycleRuntimes/'+svrName)
     return slrBean

#=====================================================================================
# Monitors Cluster  Status
#=====================================================================================
def ClusterHealth():
     clusterList = adminHome.getMBeansByType('Cluster')
     for cluster in clusterList:
           status = state(cluster.getName(),'Cluster')
           print >>logfile,Date(),status





#=====================================================================================
# Monitors Server Threads 
#=====================================================================================
def QueStats():
     print  >>logfile,Date(),'%11s %s ' % ("****Message****    The Runtime Thread Stats of",svr) 
     thread = getMBean('domainRuntime:/ServerRuntimes/'+svr+'/ThreadPoolRuntime/ThreadPoolRuntime')
     print ' '
     try: 
     #for thread in tlist:
          ithreads = thread.getExecuteThreadIdleCount()
          tthreads = thread.getExecuteThreadTotalCount()
          pthreads = thread.getPendingUserRequestCount()
          qlength  = thread.getQueueLength()
          sthreads = thread.getStandbyThreadCount()
          health   = thread.getHealthState()

          if (ithreads <= threadIdle):
               print >>logfile,Date(),'%17s %s %s %9s %9s ' % ('****Warning****    ',domainName,'.',svr,'JVM is running low on Idle Threads.') 
          
          if (pthreads >= pendingRequests):
               print >>logfile,Date(),'%17s %s %s %9s %9s ' % ('****Warning****    ',domainName,'.',svr,'has more than 100 requests pending') 
          
          else: 
               print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',domainName,'.',svr,'.ThreadIdleCount=',ithreads)
               print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',domainName,'.',svr,'.TotalCount=',tthreads) 
               print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',domainName,'.',svr,'.PendingRequestCount=',pthreads) 
               print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',domainName,'.',svr,'.QueueLength=',qlength) 
               print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',domainName,'.',svr,'.StandbyThreadCount=',sthreads) 
               print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',domainName,'.',svr,'.ThreadState=',health) 
               print ' '
     except:
          print >>logfile,Date(),'%17s %9s %s %9s %9s ' % ('****ERROR****    No Runtime Threads found for ',domainName,'.',svr ,' Please Check the status manually') 

#===================================================================================
# Monitors Servers JVM 
#===================================================================================
def JVMStats():
     svr= server.getName()
     print >>logfile,Date(),'%13s %s ' % ("****Message****    The Runtime JVM Stats of",svr) 
     jvmRT=getMBean('domainRuntime:/ServerRuntimes/'+svr+'/JVMRuntime/'+svr)
     print ' '
     try:
          GCStart = jvmRT.getLastGCStart()
          GCEnd = jvmRT.getLastGCEnd()
          GCTime = jvmRT.getTotalGarbageCollectionTime()
          GCCount = jvmRT.getTotalGarbageCollectionCount()

          freejvm = jvmRT.getHeapFreeCurrent()
          totaljvm = jvmRT.getHeapSizeCurrent()
          freepercent = jvmRT.getHeapFreePercent() 
          usedjvm = (totaljvm - freejvm)

          print  >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ("****Info****    ",domainName,".",svr,".GCStart=",GCStart) 
          print  >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ("****Info****    ",domainName,".",svr,".GCEnd=",GCEnd) 
          print  >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ("****Info****    ",domainName,".",svr,".GCTime=",GCTime)
          print  >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ("****Info****    ",domainName,".",svr,".GCCount=",GCCount)

          print  >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ("****Info****    ",domainName,".",svr,".TotalJVM=",totaljvm) 
          print  >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ("****Info****    ",domainName,".",svr,".UsedJVM=",usedjvm) 
          print  >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ("****Info****    ",domainName,".",svr,".FreeJVM=",int(freejvm))
          print ' '
     except:
          print >>logfile,Date(),'%16s %9s %9s %9s ' % ('****ERROR****   Server ',svr,' Not Running in domain ',domainName) 



#=====================================================================================
# Monitors JDBC Connection Pools 
#=====================================================================================
def JDBCStats():
     print >>logfile,Date(),'%13s %s ' % ("****Message****    The Runtime JDBC Stats of",svr) 
     dsNames = getMBean('domainRuntime:/ServerRuntimes/' + svr + '/JDBCServiceRuntime/' + svr ).getJDBCDataSourceRuntimeMBeans()
     for dsName in [c.getName() for c in dsNames ]: 
          if dsName != '': 
               poolRT = getMBean('domainRuntime:/ServerRuntimes/'  + svr + '/JDBCServiceRuntime/' + svr + '/JDBCDataSourceRuntimeMBeans/' + dsName)
               if not poolRT.isEnabled(): 
                    print>>logfile,Date(),'%14s %s %s ' % ('****ERROR****    ',dsName,'. PoolDisabled ')    
               else:
                    state = poolRT.getState() 
                    if state != 'Running':
                         print >>logfile,Date(),'%14s %s %s %s ' % ('****Warning****    Current state of ',dsName,'=',state) 

                     
                    if poolRT.getWaitSecondsHighCount() > waitSec: 
                         print >>logfile,Date(),'%16s %s %s %s %s' % ('****Warning****    ',domainName,'.',svr,' has a wait delay of more than 1 second ') 

                    else:
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.ReserveRequestCount=',poolRT.getReserveRequestCount()) 
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.ConnectionsTotalCount=',poolRT.getConnectionsTotalCount())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.ActiveConnectionsAverageCount=',poolRT.getActiveConnectionsAverageCount())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.ActiveConnectionsCurrentCount=',poolRT.getActiveConnectionsCurrentCount())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.ActiveConnectionsHighCount=',poolRT.getActiveConnectionsHighCount())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.CurrCapacity=',poolRT.getCurrCapacity())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.CurrCapacityHighCount=',poolRT.getCurrCapacityHighCount()) 
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.FailuresToReconnectCount=',poolRT.getFailuresToReconnectCount())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.LeakedConnectionCount=',poolRT.getLeakedConnectionCount())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.NumAvailable=',poolRT.getNumAvailable())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.HighestNumAvailable=',poolRT.getHighestNumAvailable())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.NumUnavailable=',poolRT.getNumUnavailable())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.HighestNumUnavailable=',poolRT.getHighestNumUnavailable())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.WaitingForConnectionCurrent=',poolRT.getWaitingForConnectionCurrentCount())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.WaitingForConnectionHigh=',poolRT.getWaitingForConnectionHighCount())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.WaitSecondsHigh=',poolRT.getWaitSecondsHighCount())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.WaitingForConnectionFailure=',poolRT.getWaitingForConnectionFailureTotal())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.WaitingForConnectionSuccess=',poolRT.getWaitingForConnectionSuccessTotal())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.WaitingForConnectionTotal=',poolRT.getWaitingForConnectionTotal())
                         print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ',dsName,'.',svr,'.ConnectionDelayTime=',poolRT.getConnectionDelayTime())

          else:
               print >>logfile,Date(),'%13s %s %s %s' % ('****ERROR****    No Pools Configured in ',domainName,'.',svr) 


#=====================================================================================
# Monitors JMS 
#=====================================================================================
def JmsStats():
     print  >>logfile,Date(),'%13s %s %s ' % ("****Message****    The Runtime JMS Stats of",svr) 
     jmsrtlist=home.getMBeansByType('JMSDestinationRuntime')
     print ' '
     for jmsRT in jmsrtlist:
          jmsname = jmsRT.getAttribute("Name")
          jmsbcc = jmsRT.getAttribute("BytesCurrentCount")
          jmsbpc = jmsRT.getAttribute("BytesPendingCount")
          jmsbrc = jmsRT.getAttribute("BytesReceivedCount")
          jmsbhc = jmsRT.getAttribute("BytesHighCount")
          jmsmcc = jmsRT.getAttribute("MessagesCurrentCount")
          jmsmpc = jmsRT.getAttribute("MessagesPendingCount")
          jmsmhc = jmsRT.getAttribute("MessagesHighCount")
          jmsmrc = jmsRT.getAttribute("MessagesReceivedCount")
          jmsctc = jmsRT.getAttribute("ConsumersTotalCount")
          print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ",domainName,".",svr,".Name=',jmsname) 
          print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ",domainName,".",svr,".BytesCurrentCount=',jmsbcc) 
          print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ",domainName,".",svr,".BytesPendingCount=',jmsbpc) 
          print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ",domainName,".",svr,".BytesReceived=',jmsbrc) 
          print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ",domainName,".",svr,".BytesHighCount=',jmsbhc) 
          print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ",domainName,".",svr,".MessagesCurrrent=',jmsmcc) 
          print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ",domainName,".",svr,".MsgPendingCount=',jmsmpc) 
          print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ",domainName,".",svr,".MsgHighCount=',jmsmhc) 
          print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ",domainName,".",svr,".MsgReceived=',jmsmrc) 
          print >>logfile,Date(),'%16s %9s %s %9s %9s %s' % ('****Info****    ",domainName,".",svr,".MsgConsumersTotal=',jmsctc) 
          print ' '


#=====================================================================================
#  Invoke Main and end
#=====================================================================================

#userprops = loadPropertiesFromFile("build.properties")
#userprops = loadPropertiesFromFile("/opt/app/phone/poc/41/phonedomain/servers/eusbadminsvr/security/boot.properties")
#username = weblogic.security.Decrypt(userprops['username'])
#passwd   = weblogic.security.Decrypt(userprops['password'])



try:
     connect(userConfigFile=userprops['ucf'], userKeyFile=userprops['ukf'], url=userprops['admin.url']) 
 
#     connect(userprops['user.name'],userprops['user.password'],userprops['admin.url'])
#storeUserConfig('/opt/app/phone_stage/Monitor/myuserconfigfile.secure','/opt/app/phone_stage/Monitor/myuserkeyfile.secure')

     getRunningServerNames()
     serverRuntime()
     while 1: 
          serverlist=adminHome.getMBeansByType('Server')
          for server in serverlist:
               svr= server.getName()
  
               try:
                    checkHealth()
                    QueStats()
                    JVMStats() 
                    JDBCStats()               
                    JmsStats() 
          
               except:           
                    continue
     lang.Thread.currentThread().sleep(30)

except WLSTException:
     print >>logfile,Date(),'%13s %s %s ' % ("****ERROR****    Could not connect to ",domainName,".Admin server ") 
     print >>logfile,Date(),'%13s %s %s ' % ("****ERROR****    Please Check the status of Admin Server in",domainName) 
     exit()

#lang.Thread.currentThread().sleep(30000)
logfile.close()
disconnect()
exit()         








