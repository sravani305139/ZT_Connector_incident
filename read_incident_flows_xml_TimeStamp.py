import pysnow
import json
import LogGenModule
from dicttoxml import dicttoxml
import Keys_Flows
import Escalation_Reassign
import datetime
from pathlib import Path
import parse_xml
import base64

def decrypt(encryped):
    try :
        key = "AutoFactCIS1569"
        msg = []
        for i, c in enumerate(encryped):
            key_c = ord(key[i % len(key)])
            enc_c = ord(c)
            msg.append(chr((enc_c - key_c) % 127))
        encoded = ''.join(msg)
        encoded = encoded.replace("b'","")
        encoded = encoded.encode('utf-8')
        #print(encoded)
        data =  base64.b64decode(encoded.decode('utf-8'))
        #print(data)
        return data.decode('utf-8')
    except Exception as e:
        print(str(e))
def to_xml(data,name_of_file):#creates the XML files
    try:
        xml = dicttoxml(data, custom_root='test', attr_type=False)                                                                     #converts the dictonary data into XML
        filename = "./Queue/InputFiles/"+name_of_file+".xml"
        file = open(filename,"w")
        xml = str(xml).replace("b'","")
        xml = str(xml).replace("'","")
        file.write(str(xml)+"\n")
        file.close()
    except Exception as e:
        LogGenModule.Exception("Not able to create XML File")
        LogGenModule.Exception(e)

def capture_scripts(data):
    file = open(scriptfilename,"a")
    file.write(data+"\n")

def read_ticket(groupname,status):
    try:
        
        total = 0
        count = 0
        esc = 0
        found = 0

        LogGenModule.info("reading the data for the given Assignment group and status...")
        tname = snow_client.resource(api_path='/table/incident')
        response = tname.get(query={'assignment_group': groupname,'state':status})

        for result in response.all():
            total +=1
            if ((result['sys_updated_on']) > prvtime):                               # compares with previous time
                if((result['sys_updated_on']) <= curr_time) :                        # compares with the captured current time                                                                                               #reads the result for the provided attributes
                    #print(result['assignment_group']['value'])
                    if len(str(result['assignment_group']))==0:                                                                                #checks the length of the assignment_group
                        group = result['assignment_group']
                    else:    
                        inval = result['assignment_group']['value']
                        group = fetch_details("/table/sys_user_group","sys_id",inval,"name")                                                   #triggers the fetch details function and gets the group name


                    if len(str(result['cmdb_ci']))==0:                                                                                         #checks the length of the CI
                        CI = result['cmdb_ci']
                        CI_sys_id = result['cmdb_ci']
                    else:
                        CI_sys_id = result['cmdb_ci']['value']
                        CI = fetch_details("/table/cmdb_ci","sys_id",CI_sys_id,"name")

                    if len(str(result['caller_id']))==0:                                                                                         #checks the length of the CI
                        user_name = "NA"
                        Loc = "NA"
                        dep = "NA"
                    else:
                        Uid = result['caller_id']['value']
                        user_name = fetch_details("/table/sys_user","sys_id",Uid,"user_name")

                        location_Data = fetch_details("/table/sys_user","sys_id",Uid,"location")
                        #print(type(location_Data))
                        #print(location_Data)
                        if len(str(location_Data))!=0:
                            Locat = location_Data['value']
                            #print(type(Locat))
                            Loc = fetch_details("/table/cmn_location","sys_id",Locat,"name")
                        else:
                            Loc = "Not Found"

                        depart_data = fetch_details("/table/sys_user","sys_id",Uid,"department")
                        if len(str(depart_data))!=0:
                            depart = depart_data['value']
                            dep = fetch_details("/table/cmn_department","sys_id",depart,"name")
                        else:
                            dep = ""

                    if len(str(result['assigned_to']))==0:                                                                                     #checks the length of the assigned_to
                        assigneduser = result['assigned_to']
                    else:
                        inuser = result['assigned_to']['value']
                        assigneduser = fetch_details("/table/sys_user","sys_id",inuser,"name")                                                #triggers the fetch details function and gets the user name

                    status = result['state']
                    statusval = StatusValuetoString(status) # gets the string for the status value

                    LogGenModule.info(("\n***Details fetched for the Incident : {}***\n Status : {}\n Summary : {}\n Description : {}\n Category : {}\n Sub-Category : {}\n Assigned Group : {}\n Assignee : {}".format(result['number'],statusval,result['short_description'],result['description'],result['category'],result['subcategory'],group,assigneduser)))
                    
                    #print("number of the Incident : {}\n Status : {}\n Summary : {}\n Description : {}\n Category : {}\n Sub-Category : {}\n Assigned Group : {}\n Assignee : {}".format(result['number'],statusval,result['short_description'],result['description'],result['category'],result['subcategory'],group,assigneduser))

                    Flow_name = Keys_Flows.find_flow(result['short_description'])[0]
                    E_G = Keys_Flows.find_flow(result['short_description'])[1]
                    tower_name = Keys_Flows.find_flow(result['short_description'])[2]
                    #print(len(Flow_name))
                    #if len(Flow_name)==0:
                        #Escalation_Reassign.re_assignto_none(tname,result['number'])
                    name_of_file = result['number'] #name of the xml file to be created
                    #name_of_file = result['number'] 
                    
                    if Flow_name=="NF":
                        Flow_Result = "No Flow Found"
                        Flowname = "No Flow Identified"
                        remarks = "Escalated"
                        Escalation_Group = "Notfound"
                        if(EscalateTo == 'NONE'):
                            continue
                        else:
                            Escalation_Reassign.reassign_group(tname,result['number'],EscalateTo)
                        esc +=1
                    else:
                        Flow_Result = "Sent to Orchestrator"
                        remarks = "UID from orchestrator"
                        Flowname = Flow_name
                        Escalation_Group = E_G
                        found +=1
                                                                                                                     
                        dic ={
                            "Incident":{
                                'Sys_ID' : result['sys_id'],
                                'Number' : result['number'],
                                'Status' : result['state'],
                                'Assigned Group' : group,
                                'Assignee' : assigneduser,
                                'Category' : result['category'],
                                'Sub-Category' : result['subcategory'],
                                'Summary' : result['short_description'],
                                'Description' : result['description'],
                                'Flow' : Flow_name,
                                'Configuration Item' : CI,
                                'Sys_ID_CI' : CI_sys_id,
                                'Escalation_Group' : Escalation_Group,
                                'Tower' : tower_name,
                                'User_ID' : user_name,
                                'user_location' : Loc,
                                'user_department' : dep
                            }
                        }
                        #dictionary.append(dic)
                        #print(dictionary)    
                        Xml_data = to_xml(dic,name_of_file)# calls the function to convert data into XML format
                        capture_scripts(Flow_name)

                    send_data = "<tr><td>"+datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')+"</td><td>"+result['number']+"</td><td>"+Flow_Result+"</td><td>"+Flowname+"</td><td>"+remarks+"</td></tr>"
                    create_log_html(send_data)
        replace = open("./Time_Stamps/pre_time.txt","w")
        replace.write(str(curr_time))         #replaces the previous time 
        replace.close()
        count = (total-(found+esc))
        log=open("./Time_Stamps/time_reference.txt","a")
        log.write(" Total : "+str(total)+" FWD = "+str(found)+" ESC : "+str(esc)+" FLTR : "+str(count)+"\n")# logs the executed time frame
        log.close()
        parse_xml.exec_xml()

    except Exception as e:

        LogGenModule.Exception("Issue while fetching the Ticket data")
        LogGenModule.Exception(e)

def create_log_html(data):
    #logtime =  datetime.datetime.now().strftime('%d-%m-%y')
    log_file = open('./Fetched_Ticket_logs/Incident_login_'+logtime+'.html','a')
    log_file.write(data)
    log_file.close()


def fetch_details(tablepath,attribute,value,outval): # fetches the data from the given table for mentioned attribute and provides the result for desired attribute
    try:
        LogGenModule.info("Fetching the details from : {}".format(tablepath))
        respond = snow_client.resource(api_path=tablepath)
        groupname = respond.get(query={attribute : value})
        for res in groupname.all():
            #print(res[outval])
            return res[outval]

    except Exception as e:
        LogGenModule.Exception("Issue while fetching the Ticket data from table : "+tablepath+"\natrribute : "+attribute)
        LogGenModule.Exception(e)



def StatusValuetoString(Value):# converts the status value from integer to string
    try:
        LogGenModule.info("converting the status value to string...")
        status = {'1' : 'New' , '2' : 'In Progress', '3' : 'Pending', '4' : 'Resolved', '5' : 'Closed'}
        return status[Value]
    except Exception as e:
                LogGenModule.Exception("Issue in converting status value to string"+e)



if __name__ == "__main__":
    scriptfilename = "scripts_to_execute"+datetime.datetime.now().strftime('%d_%m_%Y')+".txt"

    start_tags='<html><table  border="1" bordercolor=000000 cellspacing="0" cellpadding="1" style="table-layout:fixed;vertical-align:bottom;font-size:10px;font-family:verdana,sans,sans-serif;border-collapse:collapse;border:1px solid rgb(130,130,130)" >'
    end_tags="</table></html><br><br>"
    Heading_tags ="<tr style='background-color:DodgerBlue; color:White;'><th>Captured Time</th><th> Incident Number </th><th> Status </th><th>Identified Flow</th><th>Remarks</th>"
    logtime =  datetime.datetime.now().strftime('%d-%m-%y')



    my_file = Path("./Time_Stamps/pre_time.txt")
    if my_file.is_file():                                                        # checks if prev_time file exists or not
        print("privous time exists")
        f = open('./Time_Stamps/pre_time.txt')
        time = f.read()
        f.close()                                                   # if exists time = previous captured timebreak;
    else:
        time = "1994-04-04 06:45:20"                                             # if not exists hardcodes the value to the previous time

    #print(time)
    curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')            # captures current time
    data1 = datetime.datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
    prvtime = datetime.datetime.strftime(data1,'%Y-%m-%d %H:%M:%S')
    log=open("./Time_Stamps/time_reference.txt","a")
    log.write(" > "+str(prvtime)+" <= "+str(curr_time))
    log.close()

    LogGenModule.info("=============================")

    try:
            LogGenModule.info("*******Fetching the Instance Details*******")

            with open('./json_files/snow_login.json') as json_data:                                                                                     #collects the data from the input file
                    data = json.load(json_data)
                    instancename = data["Instance Details"][0]["instance"]
                    username = decrypt(data["Instance Details"][0]["user"])
                    paswd = decrypt(data["Instance Details"][0]["password"])
            LogGenModule.info("*******Fetching the Ticket Data*******")
            with open('./json_files/snow_read_ticket.json') as json_ticket:
                    ticket = json.load(json_ticket) 
                    Assigned_Group = ticket["Ticket Details"][0]["Assigned_Group"]
                    status = ticket["Ticket Details"][0]["status"]
                    EscalateTo = ticket["Ticket Details"][0]["EscalateTo"]
                    

            LogGenModule.info("Logging into ServiceNow Client of instance.."+instancename)
            #Logs in to the ServiceNow instance 
            snow_client = pysnow.Client(instance=instancename, user=username, password=paswd)

    except Exception as e:
            LogGenModule.Exception("Not able to connect/login")
            LogGenModule.Exception(e)
    logfile = Path("Incident_login_"+logtime+".html")
    if logfile.is_file():
        print('log file exists')
    else:
        create_log_html(start_tags)
        create_log_html(Heading_tags)

    assignedgroupid = fetch_details("/table/sys_user_group","name",Assigned_Group,"sys_id") #fetches the sys_id of provided group
    
    dictionary = []

    #>= 2018-04-24 09:33:09 < 2018-04-24 09:38:09	Total: 20  FWD: 10 ESC: 5 FLTR : 5
    
    read_ticket(assignedgroupid,status) # triggers the read function
    print("previous time ="+str(prvtime)+" Current time = "+str(curr_time))
