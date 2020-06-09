import getpass
import sys
import telnetlib


HOST = "10.181.11.15"
user = "root"
password = "wipro@123"

tn = telnetlib.Telnet(HOST,22,timeout=120)

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write(b"ls\n")
tn.write(b"exit\n")

print(tn.read_all().decode('ascii'))