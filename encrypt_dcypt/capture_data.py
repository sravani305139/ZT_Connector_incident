from flask import Flask,request
from flask import render_template
import encryption
import getpass
import shutil
import LogGenModule

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/add_user.html', methods=['GET', 'POST'])
def add_user():
    return render_template('add_user.html')

@app.route('/upl_user.html', methods=['GET', 'POST'])
def upl_user():
    return render_template('upl_user.html')

@app.route('/delete.html', methods=['GET', 'POST'])
def delete():
    return render_template('delete.html')

@app.route('/listuser', methods=['GET', 'POST'])
def list_user():
    return listuser()

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    try :
        user = request.form['UID']
        password = request.form['pass']
        conpass = request.form['conpass']
        Tower = request.form['tower'].lower()
        context = request.form['context'].lower()
        user_en = encryption.encrypt_password("AutoFact", user)
        pass_en = encryption.encrypt_password("AutoFact", password)
        
        #to_csv(user_en,pass_en,Tower,context)
        if(password == conpass):
            write_CSV = open('./text.csv','a')
            check = exists(user_en,Tower)
            if(check == "notexists"):
                write_CSV.write(str(user_en)+"::!::"+str(pass_en)+"::!::"+str(Tower)+"::!::"+str(context)+"\n")
                write_CSV.close()
                return 'Hello   User {} is created for {} Sucessfully...!!!'.format(user,Tower)
            else:
                write_CSV.close()
                return 'Hello   User {} for {} already exists...!!!'.format(user,Tower)
        else:
            return 'Please enter same value for password and confirm password...!!!'
        return listuser()
    except Exception as e:
        LogGenModule.exception(e)


@app.route('/edituser', methods=['GET', 'POST'])
def edituser():
    try:
        user = request.args.get('UID')
        Tow = request.args.get('tower')
        Tower = Tow.lower()
        cont = request.args.get('context')
        context = cont.lower()
        user_en = encryption.encrypt_password("AutoFact", user)
        result = []
        result.append(user+"!"+Tower+"!"+context)
        results = result
        return render_template('mod_user.html', results=results)
    except Exception as e:
        LogGenModule.exception(e)


@app.route('/deleteuser', methods=['GET', 'POST'])
def deleteuser():
    try:
        user = request.args.get('UID')
        Tow = request.args.get('tower')
        Tower = Tow.lower()
        cont = request.args.get('context')
        context = cont.lower()
        user_en = encryption.encrypt_password("AutoFact", user)
        result = []
        result.append(user+"!"+Tower+"!"+context)
        results = result
        return render_template('del_user.html', results=results)
    except Exception as e:
        LogGenModule.exception(e)


@app.route('/upuser', methods=['GET', 'POST'])
def upuser():
    try:
        user = request.form['UID']
        expass = request.form['oldspass']
        password = request.form['pass']
        conpass = request.form['conpass']
        Tower = request.form['tower'].lower()
        context = request.form['context'].lower()
        user_en = encryption.encrypt_password("AutoFact", user)
        pass_en = encryption.encrypt_password("AutoFact", expass)
        verification = verify_pass(user_en,Tower,pass_en)
        if(verification == "success"):
            if(len(conpass) > 0):
                if(password == conpass):
                    newpass_en = encryption.encrypt_password("AutoFact", conpass)
                    res = mod_csv(user_en,newpass_en,Tower,context)
                else :
                    return "Please enter same vale for password and confirm password"
            else :
                res = mod_csv(user_en,pass_en,Tower,context)
        else:
            return "correct value for old password"
        #return render_template('listuser')
        return listuser()
    except Exception as e:
        LogGenModule.exception(e)


@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    try:
        user = request.form['UID']
        expass = request.form['oldspass']
        Tower = request.form['tower'].lower()
        context = request.form['context'].lower()
        user_en = encryption.encrypt_password("AutoFact", user)
        pass_en = encryption.encrypt_password("AutoFact", expass)
        verification = verify_pass(user_en,Tower,pass_en)
        if(verification == "success"):
            res = del_csv(user_en,pass_en,Tower,context)     
        else:
            return "provide correct value for password"
        #return render_template('listuser')
        return listuser()
    except Exception as e:
        LogGenModule.exception(e)


@app.route('/moduser', methods=['GET', 'POST'])
def moduser():
    return render_template('upl_user.html')


def del_csv(user,passw,tow,context):
    try:
        file1 = open('text.csv', 'r')
        file2 = open('filedel.csv', 'a')
        for line in file1:
            #print(line)
            row = line.split("::!::")
            if (row[0] == user):
                if (row[2] == tow):
                    continue
                    sol = "Sucessfully Updated the User Data...!!!!!!!"
            else :
                sol = "not able to find the user..!!!"
            file2.write(str(row[0])+"::!::"+str(row[1])+"::!::"+str(row[2])+"::!::"+str(row[3]))
        file1.close()
        file2.close()
        shutil.move("./filedel.csv","./text.csv")
        return sol
    except Exception as e:
        LogGenModule.exception(e)

def mod_csv(user,passw,tow,context):
    try: 
        file1 = open('text.csv', 'r')
        file2 = open('filemod.csv', 'a')
        for line in file1:
            #print(line)
            row = line.split("::!::")
            if (row[0] == user):
                if(row[2] == tow):
                    row[1] = passw           
                    row[3] = context+"\n"
                    sol = "Sucessfully Updated the User Data...!!!!!!!"
            else :
                sol = "not able to find the user..!!!"
            file2.write(str(row[0])+"::!::"+str(row[1])+"::!::"+str(row[2])+"::!::"+str(row[3]))
        file1.close()
        file2.close()
        shutil.move("./filemod.csv","./text.csv")
        return sol
    except Exception as e:
        LogGenModule.exception(e)




def exists(user_en,Tower):
    try:
        file_csv = open('./text.csv','r')
        flag = "notexists"
        for line in file_csv:
            row = line.split("::!::")
            if (str(user_en) == row[0]):
                if (str(Tower) == row[2].lower()):
                    flag = "exists"
        return flag
    except Exception as e:
        LogGenModule.exception(e)

def verify_pass(user_en,Tower,passphrase):
    try:
        file_csv = open('./text.csv','r')
        flag = "failed"
        for line in file_csv:
            row = line.split("::!::")
            if (str(user_en) == row[0]):
                if (str(Tower) == row[2].lower()):
                    if (str(passphrase) == row[1]):
                        flag = "success"
        return flag
    except Exception as e:
        LogGenModule.exception(e)

def listuser():
    try:
        dic=[]
        file_csv = open('./text.csv','r')
        for line in file_csv:
            row = line.split("::!::")
            user = encryption.decrypt("AutoFact", row[0])
            row[3] = row[3].replace("\n","")
            dic.append(user+"!"+row[2]+"!"+row[3]) 
            #print(dic)
        #(dic)
        results = dic
        return render_template('list.html', results=results)
    except Exception as e:
        LogGenModule.exception(e)

@app.route('/images')
def image():
    filename = request.args.get('name')

if __name__=='__main__':
    app.run("localhost",int(8020))
    
    #to_csv(user_en,pass_en,Tower,context)
