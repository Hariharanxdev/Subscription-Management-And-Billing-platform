from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "Hari123"

try:
    hashed = pwd_context.hash(password)
    print("Hash:", hashed)
    print("Verify:", pwd_context.verify(password, hashed))
except Exception as e:
    print("ERROR:", e)