import re
from string import strip, atoi

def get_input():
    try:
        return raw_input().replace('\\', '/')
    except EOFError:
        exit()


#<ioexp;
#EXCHANGE IDENTITY DATA

#IDENTITY
#BEIMSC 141/00/00/1  148

#END
def check_ioexp(input_str):
    output_str = ['#EXCHANGE IDENTITY: ']
    while True:
        input_str = strip(get_input())

        if input_str == 'IDENTITY':
            input_str = strip(get_input()).split(" ")[0]
            output_str[0] += input_str

        elif input_str == 'END':
            return output_str


#<dpwsp; 
#CP STATE
#
#MAU  SB SBSTATE      RPH-A       RPH-B       BUA STATE
#NRM  B  WO           -           -                   1
#
#END
def check_dpwsp(input_str):
    output_str = ['#CP STATE: ']
    while True:
        input_str = strip(get_input()).split()
        if len(input_str) == 0:
            continue

        if input_str[0] == 'MAU':
            input_str = strip(get_input()).split()
            if (input_str[0] == 'NRM') and (input_str[2] == 'WO'):
                output_str[0] += 'OK' 
            else:
                output_str[0] += 'FAIL: '+ input_str[0] + ' ' + input_str[2]

        elif input_str[0] == 'END':
            return output_str


#<allip:acl=a2;
#ALARM LIST
#
#A2/APT "BEIMSC 141/00/0" 870 140905   0116      
#MT IMEI SUPERVISION LOG FAULT
#
#LOG
#GREY
#
#END
def check_allip(input_str):
    output_str = ['#CP ALARM: ']
    state = 'OK'

    while True:
        input_str = strip(get_input()).split()
        if len(input_str) == 0:
            continue

        if re.search(r"APZ", input_str[0]):
            state = 'FAIL' 
            alarm_str = '-\t' + input_str[0] + ": "
            input_str = strip(get_input())
            output_str.append(alarm_str + input_str)

        elif input_str[0] == 'END':
            output_str[0] += state
            return output_str

#<apamp;
#AP MAINTENANCE DATA
#
#DIRECTORY ADDRESS DATA
#
#AP  NODE  LAN   IP               PORT  STATUS  CATEGORY
#1   A     1     192.168.169.1    14000 ACTIVE
#1   A     2     192.168.170.1    14000 PASSIVE
#1   B     2     192.168.170.2    14000 PASSIVE
#1   B     1     192.168.169.2    14000 ACTIVE
#
#AP MAINTENANCE TABLE
#
#AP  IO    ACTIVENODE  LOCALIP1          LOCALIP2
#1   YES   A           192.168.169.57    192.168.170.57
#
#END
def check_apamp(input_str):
    output_str = ['#AP MAINTENANCE DATA: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"FAULTY", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str

#PROCESSOR LOAD DATA
#INT PLOAD CALIM OFFDO OFFDI FTCHDO FTCHDI OFFMPH OFFMPL FTCHMPH FTCHMPL
# 1    1   75000     3     2     3      2     15      9     15       9
# 2    1   75000     2     3     2      3     13      9     13       9
# 3    1   75000     2     4     2      4     12      5     12       5
# 4    1   75000     3     3     3      3     14      0     14       0
# 5    1   75000     3     3     3      3     17      1     17       1
# 6    1   75000     0     2     0      2     13      0     13       0
# 7    1   75000     1     6     1      6     13      1     13       1
# 8    1   75000     0     4     0      4     10      1     10       1
# 9    1   75000     1     2     1      2      9      0      9       0
#10    1   75000     3     3     3      3     17      1     17       1
#11    1   75000     7     5     7      5     15      3     15       3
#12    1   75000     2     3     2      3     18      9     18       9
#
#INT OFFTCAP FTDTCAP
# 1      0       0
# 2      0       0
# 3      0       0
# 4      0       0
# 5      0       0
# 6      0       0
# 7      0       0
# 8      0       0
# 9      0       0
#10      0       0
#11      0       0
#12      0       0
#END
def check_plldp(input_str):
    output_str = ['#PROCESSOR LOAD DATA: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"PLOAD", input_str):
            input_str = strip(get_input()).split()
            output_str[0] += '= ' + input_str[1] + '%'

        elif input_str == 'END':
            output_str[0] += ' ' + state
            return output_str

#<mgsvp;
#MT MOBILE SUBSCRIBER SURVEY
#
#HLRADDR             NSUB       NSUBA
#4-870772001199        10824       7859
#4-639879990005          221        155
#4-8613492233333        9179       7262
#
#TOTNSUB
#20224
#
#TOTNSUBA
#15276
#
#END
def check_mgsvp(input_str):
    output_str = ['#MT MOBILE SUBSCRIBER SURVEY: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"HLRADDR", input_str):
            output_str.append("\t" + input_str)
            while True:
                input_str = (strip(get_input()).split())
                if len(input_str) == 0:
                    break
                output_str.append("\t" + "\t".join(input_str))

        elif input_str == 'END':
            output_str[0] += state
            return output_str

#<strsp:r=all;
#DEVICE STATE SURVEY
#R        NDV         NOCC        NIDL        NBLO        RSTAT
#TC                0           0           0           0  NORES
#TCT               0           0           0           0  NORES
#TCONI          1024           0        1024           0  NORES
#TCIAL1            1           1           0           0  NORES
#TCIAR1            0           0           0           0  NORES
#BJNER1O          29           3          26          10  NORES
#BJNER1I          29           3          26          10  NORES
#END
def check_strsp(input_str):
    output_str = ['#DEVICE STATE SURVEY: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"NBLO", input_str):
            continue

        elif input_str == 'END':
            output_str[0] += state
            return output_str
        
        input_str = input_str.split()
        if len(input_str) < 4:
            continue

        if atoi(input_str[4]) > 0:
            state = 'FAIL'
            output_str.append("-\t" + "\t".join(input_str))

#<exrpp:rp=all;
#RP DATA
#
#RP    STATE  TYPE     TWIN  STATE   DS     MAINT.STATE
#   0  WO     RPSCB1E                       IDLE
#   1  WO     RPSCB1E                       IDLE
#   2  WO     GARP2E                        IDLE
#   3  WO     GARP2E                        IDLE
#   4  WO     RPSCB1E                       IDLE
#END
def check_exrpp(input_str):
    output_str = ['#RP DATA: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"AB", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str

#<exemp:rp=all,em=all;
#EM DATA
#
#RP    TYPE   EM  EQM                       TWIN  CNTRL  PP     STATE
#   2  GARP2E  0  OCITS-0                         PRIM          WO
#   2  GARP2E  1  JOB-0                           PRIM          WO
#
#   3  GARP2E  0  OCITS-1                         PRIM          WO
#   3  GARP2E  1  JOB-1                           PRIM          WO
#
#END
def check_exemp(input_str):
    output_str = ['#EM DATA: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"AB", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str


#<ihcop:ipport=all;
#IP PORT CONNECTION DATA
#
#IPPORT  MHROLE   MHRELPORT  CURROLE
#IP-0-2  ACTIVE   IP-1-2     ACTIVE
#
#IPADD             SUBMASK
#10.128.228.50     255.255.255.248
#
#MTU
#1500
#
#IPMIGR          IPBK
#0               
#
#SVRATE  SVTO  SVMAXTX  SVMINRX
#10      3     2        2
#
#SVI  SVR
#65   82
#
#SVGW
#
#
#IPPORT  MHROLE   MHRELPORT  CURROLE
#IP-1-2  STAND-BY IP-0-2     STAND-BY
#
#IPADD             SUBMASK
#10.128.228.58     255.255.255.248
#
#MTU
#1500
#
#IPMIGR          IPBK
#0               
#
#SVRATE  SVTO  SVMAXTX  SVMINRX
#10      3     2        2
#
#SVI  SVR
#65   82
#
#SVGW
#
#END
def check_ihcop(input_str):
    output_str = ['#IP PORT CONNECTION DATA: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"IPPORT", input_str):
            input_str = strip(get_input())
            output_str.append('\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str

#<ihstp:ipport=all;
#IP PORT STATE
#
#IPPORT         OPSTATE  BLSTATE
#IP-0-2         BUSY     
#IP-1-2         BUSY     
#IP-2-2         BUSY     
#IP-3-2         BUSY     
#IP-4-2         BUSY     
#IP-5-2         BUSY     
#
#END
def check_ihstp(input_str):
    output_str = ['#IP PORT STATE: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"ABL", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif re.search(r"CBL", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str


#<m3asp;
#M3UA ASSOCIATION STATUS
#
#SAID             STATE  BLSTATE          AUTOBLSTATE
#BJSAS3           ACT                     
#
#BJSAS2           ACT                     
#
#BJSAS1           ACT                     
#
#END
def check_m3asp(input_str):
    output_str = ['#M3UA ASSOCIATION STATUS: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"DOWN", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif re.search(r"INACT", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str


#<m3rsp:dest=all;
#M3UA ROUTING DATA
#
#DEST           SPID         DST    LSHM
#0-9154         BJCU001      AVA    PP
#
#               SAID             PRIO  RST              CW     CWU
#               BJSAS3              1  EN-ACT-AVA              
#
#0-9163         BJCTSTP      AVA    PP
#
#               SAID             PRIO  RST              CW     CWU
#               BJSAS3              1  EN-ACT-AVA              
#
#END
def check_m3rsp(input_str):
    output_str = ['#M3UA ROUTING DATA: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"DIS", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif re.search(r"INAC", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif re.search(r"UNAVA", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str

#<chopp;
#COMMON CHARGING OUTPUT ADJUNCT PROCESSOR INTERFACE DATA
#
#STATUS    BSIZE    OUTP    MSNAME          DEFMSNAME       DEFBSIZE
#OPEN          4    00000   CHS             CHS                    4
#END
def check_chopp(input_str):
    output_str = ['#COMMON CHARGING OUTPUT: ']
    state = 'FAIL'

    while True:
        input_str = strip(get_input())

        if re.search(r"STATUS", input_str):
            input_str = strip(get_input()).split()
            if input_str[0] == 'OPEN' and atoi(input_str[1]) < 100:
                state = 'OK'

        elif input_str == 'END':
            output_str[0] += state
            return output_str


#<c7ncp:sp=all,ssn=all;
#CCITT7 SCCP NETWORK CONFIGURATION DATA
#
#SP             SPID     SPSTATE     BROADCASTSTATUS  SCCPSTATE
#0-9154         BJCU001  ALLOWED     CON              ALLOWED
#
#                        SSN         SUBSYSTEMSTATE   SST
#                        7           ALLOWED          YES
#                        8           ALLOWED          YES
#
#END
def check_c7ncp(input_str):
    output_str = ['#CCITT7 SCCP NETWORK: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if input_str == 'END':
            output_str[0] += state
            return output_str


# Directory of K:\ACS\data\RTR\CHS_CP0EX\DATAFILES\REPORTED
#
#08/19/2015  05:50 AM    <DIR>          .
#08/19/2015  05:50 AM    <DIR>          ..
#07/19/2015  05:59 AM           107,950 RTR-0719-0549.7037
#07/19/2015  06:09 AM           110,281 RTR-0719-0559.7038
#07/19/2015  06:19 AM           110,813 RTR-0719-0609.7039
#07/19/2015  06:29 AM            91,864 RTR-0719-0619.7040
#07/19/2015  06:39 AM           101,472 RTR-0719-0629.7041
#08/19/2015  05:00 AM           227,549 RTR-0819-0450.1495
#08/19/2015  05:10 AM           201,492 RTR-0819-0500.1496
#08/19/2015  05:20 AM           190,835 RTR-0819-0510.1497
#08/19/2015  05:30 AM           178,820 RTR-0819-0520.1498
#08/19/2015  05:40 AM           193,639 RTR-0819-0530.1499
#08/19/2015  05:50 AM           196,873 RTR-0819-0540.1500
#            4464 File(s)    614,975,232 bytes
#               2 Dir(s)  66,478,096,384 bytes free
def check_rtr_reported(input_str):
    output_str = ['#K:\\ACS\\data\\RTR\\CHS_CP0EX\\DATAFILES\\REPORTED: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"\.\.", input_str):
            input_str = strip(get_input()).split()
            output_str.append('\t' + input_str[4])
            output_str.append('\t...')

        elif re.search(r"bytes", input_str):
            output_str.append('\t' + last_input_str.split()[4])
            output_str[0] += state
            return output_str
        
        last_input_str = input_str
