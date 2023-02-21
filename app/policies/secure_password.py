import bcrypt

class PasswordHasherPolicy:
    @staticmethod
    def generate(password: str):
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed_password.decode()

    @staticmethod
    def verify(password: str, hashed_password: str):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
