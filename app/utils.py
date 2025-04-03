from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

#Define a function verify that takes a plain text password and a
# hashed password, and returns True if they match, otherwise False.