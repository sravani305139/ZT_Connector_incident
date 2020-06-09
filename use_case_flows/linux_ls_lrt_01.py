#python D:\sravani_ps\testps_ver01.py IN40023355 Antivirus IssueInSendingMail test.ps1 52.187.165.166 Automation_Factory

import paramiko
import sys
import LogGenModule
import move_files
import getdata

Number = sys.argv[1]
Category = sys.argv[2]
Configuration_Item = sys.argv[3]
Escalation_Group = sys.argv[4]
short_description = sys.argv[5]
data = []

file = Number+'.txt'
sys.stdout = open('./Queue/executing_files/'+file, 'w')
tower = "linux"
data = getdata.cred(tower,Configuration_Item)
user = data[0]
passwrd = data[1]

def run_s():
    try :
        
        print(Number)
        print(Escalation_Group) #escalation group
        # Use paramiko for os command execution 
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #login to the router
        client.connect(hostname = Configuration_Item, username = user, password = passwrd )
        #executes the command and capures the output and input
        stdin, stdout, stderr = client.exec_command('ls -lrt')
        result=str(stdout.read())
        print(result) #importent to update notes
        client.close()
        print("executed") # this will resolve the ticket
                
    except Exception as e:
        print("result") #important to update notes
        print("reassign_group") # this will fail the ticket
        LogGenModule.Exception("Issue while running the wintel CPU utilization")
        LogGenModule.Exception(e)

        
run_s()
sys.stdout.close()
sys.stdout = sys.stdout   
move_files.move_file('./Queue/executing_files/','./Queue/processed_files/',file)
