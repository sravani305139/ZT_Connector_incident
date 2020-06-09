import base64
import logging

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
        logging.exception("error occured")


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
        logging.exception("error occured")

'''user = "Basu"
user_en = encrypt_password("AutoFact",user)
print(user_en)
dec_user = decrypt("AutoFact", user_en)
print(dec_user)'''