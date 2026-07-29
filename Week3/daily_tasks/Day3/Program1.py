#logic authentication system
import random
import string


class LoginServer:

    def __init__(self):

        self.users = {
            "admin": "1234",

        }

    def generate_token(self):

        return "".join(
            random.choices(
                string.ascii_letters + string.digits,
                k=20
            )
        )

    def login(self, username, password):

        if username not in self.users:

            return {
                "status": 404,
                "message": "User Not Found"
            }

        if self.users[username] != password:

            return {
                "status": 401,
                "message": "Invalid Password"
            }

        token = self.generate_token()

        return {
            "status": 200,
            "message": "Login Successful",
            "token": token
        }


server = LoginServer()

username = input("Username : ")
password = input("Password : ")

response = server.login(username, password)

print(response)