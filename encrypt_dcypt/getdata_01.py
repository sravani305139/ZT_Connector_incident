import encryption
import csv
import LogGenModule

def cred(tower,context):
    try:
        file_csv = open('./text.csv','r')
        user = "user not found"
        password = "password not found"
        flag = 0
        for line in file_csv:
            row = line.split("::!::")
            if ((str(tower).lower()) == row[2]):
                row[3] = row[3].replace("\n","")
                data = row[3].split(",")
                #print(data)
                if(row[3] == "*"):
                    user = encryption.decrypt("AutoFact", row[0])
                    password = encryption.decrypt("AutoFact", row[1])
                for i in data:  
                    if (str(i) == str(context)):
                        #print(i)
                        user = encryption.decrypt("AutoFact", row[0])
                        password = encryption.decrypt("AutoFact", row[1])
                        flag = 1
                        break
                if(flag == 1):
                    break
                    
        op_data =[user,password]
        return op_data

    except Exception as e:
        LogGenModule.Exception("Issue while fetching the data for given context and tower")
        LogGenModule.Exception(e) 
                    
op = cred("linux","10.181.11.31")
print(op)
