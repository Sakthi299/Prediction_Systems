from cryptography.fernet import Fernet
key=Fernet.generate_key()
k=key.decode('utf8')
print(k)
salt=k.encode()
crypter=Fernet(salt)
message="ajayabi"
obj=message.encode()
pw=crypter.encrypt(obj)
k=str(pw,'utf8')
s=k.encode()
decryptpw=crypter.decrypt(s)
returned=decryptpw.decode('utf8')
print(message)
print(key)
print(returned)
"""
input[type="text"], input[type="password"]
{
    border: none;
    border-bottom: 1px solid #fff;
    background: transparent;
    outline: none;
    height: 40px;
    color: #FFD700;
    font-size: 16px;
}"""