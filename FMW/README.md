# DevOps

This is a weblogic server , cluster , threads , JDBC connections monitoring script.
The script is written in Python and tested with weblogic 1222 as part of Fusion middleware infrastructure.
The script is driven by properties file.

The properties file need the following:
1)Weblogic home
2) User key file : username and password not required.Additonal security
3) User config file.

Addtionally , thresholds for parameters can also be defined. Parameters include  
ExecuteThreadIdleCount,OpenSessionsCurrentCount,HeapUsed ,PendingRequests,WaitSecondsHighCount.

The python script when executed on Linux/Windows prompts will connect to runtime instance of weblogic domain and prints a log file
with the timestamps (GMT format) . 
The logs include :
1) Server Status
2) Cluster  Status
3) Server Threads
4) Servers JVM status
5) JDBC Connection Pools status ( active/disabled / blocked)
6) JMS destinations


Usage : 

WLST.sh <absolute pathof>Monitor.py


