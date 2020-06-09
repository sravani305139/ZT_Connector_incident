import base64
import LogGenModule
import csv

def encrypt_password(key, msg):
    try :

        encryped = []
        encoded = base64.b64encode((msg).encode('utf-8'))
        #print(encoded)
        #print(str(encoded.decode('ascii')))
        for i, c in enumerate(str(encoded.decode('ascii'))):
            key_c = ord(key[i % len(key)])
            msg_c = ord(c)
            encryped.append(chr((msg_c + key_c) % 127))
        #print(''.join(encryped).encode('utf-8')) 
        return ''.join(encryped)
    except Exception as e:
        LogGenModule.Exception("error occured")


def decrypt(key, encryped):
    try :
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
        LogGenModule.Exception("error occured")

def cred(tower, context):
    try:
        print("in getdata")
        LogGenModule.info("Issue while fetching the data for given context and tower")
        file_csv = open('../encrypt_dcypt/text.csv','r')
        print("in getdata2")
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
                    user = decrypt("AutoFact", row[0])
                    password = decrypt("AutoFact", row[1])
                for i in data:  
                    if (str(i) == str(context)):
                        #print(i)
                        user = decrypt("AutoFact", row[0])
                        password = decrypt("AutoFact", row[1])
                        flag = 1
                        break
                if(flag == 1):
                    break
                    
        op_data =[user,password]
        print(op_data)
        return op_data

    except Exception as e:
        LogGenModule.Exception("Issue while fetching the data for given context and tower")
        LogGenModule.Exception(e) 
                    
'''user = "Basu"
user_en = encrypt_password("AutoFact",user)
print(user_en)
dec_user = decrypt("AutoFact", user_en)
print(dec_user)'''