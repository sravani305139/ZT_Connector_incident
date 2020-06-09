# ----------------------------Modules-------------------------------
from datetime import datetime
import paramiko
import sys
import LogGenModule
import re
import move_files

# ----------------------------Processing Input-------------------------------

Number = sys.argv[1]
Category = sys.argv[2]
Switch_IP = sys.argv[3]
Escalation_Group = sys.argv[4]
short_description = sys.argv[5]
print(short_description)
interface = short_description.strip().split("interface")[1]
print(interface)
file = Number+'.txt'
tower = "Network"
Login_ID = sys.argv[6]
Password = sys.argv[7]
sys.stdout = open('./Queue/executing_files/'+file, 'w')
print(Number)
print(Escalation_Group)


# -----------------------------Main function--------------------------------
try:
    
    command = "show interface " + interface
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    LogGenModule.info("connecting")
    ssh.connect(hostname=Switch_IP, username=Login_ID, password=Password)
    LogGenModule.info("connected..."+Switch_IP+"....interface.."+interface)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    ssh_error = list(ssh_stderr.readlines()) # converting to list because sometimes std_error shows up even when empty

    flag_as = 0
    flag_lp = 0
    flag_tod = 0
    flag_ie = 0
    flag_crc = 0
    flag_oe = 0

    

    
    if ssh_error:
        for line in ssh_error: print(line)
    else:
        for line in ssh_stdout.readlines():
            if re.search("line protocol",line,re.I):
                admin_status = line.split("line protocol")[0]
                line_protocol = line.split("line protocol")[1]
                if re.search("up",admin_status,re.I):
                    LogGenModule.info("admin status is up.")
                else:
                    flag_as=1
                    LogGenModule.info("admin status is down.")

                if re.search("up", line_protocol, re.I) and re.search("connected", line_protocol, re.I):
                    LogGenModule.info("line protocol is up and connected.")
                else:
                    flag_lp = 1
                    LogGenModule.info("line protocol is down.")
            elif re.search("total output drops",line,re.I):
                drop_count=int(line.split("output drops:")[1])
                if drop_count==0:
                    LogGenModule.info("total ouput drops is 0.")
                else:
                    flag_tod=1
                    LogGenModule.info("total output drops is "+str(drop_count)+".")
            elif re.search("input errors",line,re.I) or re.search("crc",line,re.I):
                input_error=int(line.split("input")[0])
                crc=int(line.split("CRC")[0].split(",")[1].strip())
                if input_error==0:
                    LogGenModule.info("input errors is 0.")
                else:
                    flag_ie=1
                    LogGenModule.info("input errors is "+str(input_error)+".")
                if crc==0:
                    LogGenModule.info("CRC is 0. (no cable issue)")
                else:
                    flag_crc=1
                    LogGenModule.info("CRC is "+str(crc)+".")
            elif re.search("output errors",line,re.I):
                output_error=int(line.split("output")[0].strip())
                if output_error==0:
                    LogGenModule.info("output errors is 0.")
                else:
                    flag_oe=1
                    LogGenModule.info("output errors is "+str(output_error)+".")
            else:
                continue

    if flag_as==1 or flag_lp==1 or flag_tod==1 or flag_ie==1 or flag_crc==1 or flag_oe==1:
        print("reassign_group") # this will fail the ticket
    else:
        LogGenModule.info("no issues with the interface...")
        print("executed")

except Exception as e:
    print("reassign_group") # this will fail the ticke
    LogGenModule.Exception(str(e))

sys.stdout.close()
sys.stdout = sys.stdout
move_files.move_file('./Queue/executing_files/', './Queue/processed_files/', file)
