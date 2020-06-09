import encryption
import getpass
import csv
import os, shutil
    
def to_csv(user,passpharse,Tower,context):
    write_CSV = open('./text.csv','a') 
    write_CSV.write(str(user)+"::!::"+str(passpharse)+"::!::"+str(Tower)+"::!::"+str(context)+"\n")
    write_CSV.close()
    

def mod_csv(user):
    
    rnum = user
    file1 = open('qwe.csv', 'r')
    file2 = open('file11.csv', 'a')
    for line in file1:
        print(line)
        row = line.split("::!::")
        if row[0] == rnum:
            row[2] = "sravani"
            continue
        else :
            file2.write(str(row[0])+"::!::"+str(row[1])+"::!::"+str(row[2]))
    file1.close()
    file2.close()
    shutil.move("./file11.csv","./qwe.csv")

if __name__=='__main__':
    
    user = input("enter username : ")
    password = getpass.getpass("enter old password : ")
    #new password = getpass.getpass("enter new password : ")
    Tower = input("enter tower : ")
    context = input("enter the context : ")
    user_en = encryption.encrypt_password("AutoFact", user)
    pass_en = encryption.encrypt_password("AutoFact", password)
    to_csv(user_en,pass_en,Tower,context)
    #mod_csv(user)
