import encryption
import csv
import LogGenModule

def cred(tower,context):
    try:
        file_csv = open('./text.csv','r')
        user = "user not found"
        password = "password not found"
        for line in file_csv:
            row = line.split("::!::")
            if ((str(tower).lower()) == row[2]):
                data = row[3].split(",")
                print(data)
                for i in data:
                    i = i.replace("\n","")
                    if (str(i) == str(context)):
                        print(i)
                        user = encryption.decrypt("AutoFact", row[0])
                        password = encryption.decrypt("AutoFact", row[1])
                    
        op_data =[user,password]
        return op_data
    except Exception as e:
        LogGenModule.Exception("Issue while fetching the data for given context and tower")
        LogGenModule.Exception(e) 
                    
op = cred("Automation_Factory","qw-qaz-qw")
print(op)
