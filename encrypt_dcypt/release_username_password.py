import encryption
import csv

def from_csv(user_en):
    dic=[]
    file_csv = open('./text.csv','r')
    for line in file_csv:
        print(line)
        row = line.split("::!::")
        if (str(user_en) == row[0]):
            user = encryption.decrypt("AutoFact", row[0])
            row[3] = row[3].replace("\n","")
            print("user : "+str(user))
            #print("password : "+str(password))
            data = user+row[2]+row[3]
            dic.append(data)
    print(dic)
    '''
        if (str(user_en) == row[0]):
            user = encryption.decrypt("AutoFact", row[0])
            #password = encryption.decrypt("AutoFact", row[1])
            print("user : "+str(user))
            print("password : "+str(password))'''

def listuser():
    dic=[]
    file_csv = open('./text.csv','r')
    for line in file_csv:
        row = line.split("::!::")
        #if (str(user_en) == row[0]):
        user = encryption.decrypt("AutoFact", row[0])
        print(user)
        row[3] = row[3].replace("\n","")
        dic.append(user+"!"+row[2]+"!"+row[3]) 
        #print(dat)
        #a = dat
        #dic.append(dat)
        #print(dic)
        #del dat[:]
        print(dic)
    print(dic)

if __name__=='__main__':
    listuser()
    #user = input("enter context : ")
    #user_en = encryption.encrypt_password("AutoFact",user)
    #print(user_en)
    #from_csv(user_en)
    
    

