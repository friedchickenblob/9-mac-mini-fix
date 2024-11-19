import re #used for email validation during register part.
from getpass import getpass # to hide password at time of typing.

def register(c, conn):
        username = input("Enter your username: ")
        while True: #uses regex to check if email is of valid format i.e example@example.com
            email = input("Enter your email: ")
            email_regex = re.compile(r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$')
            if email_regex.match(email):
                break
            else:
                print("Invalid e-mail! Example of a valid e-mail: example@example.com")

        while True: #checks if phone number is an integer or not.
            phone = input("Enter your phone number: ")
            if (len(phone)==10): #checks if phone number is 10 characters
                try:
                    phone = int(phone) #checks if phone number only consists of numbers.
                    break
                except:
                    print("Invalid phone number! Phone number should only contain numbers.")
            else:
                print("Invalid phone number! Phone number should be 10 digits exactly.")
        
        password = getpass("Enter your password: ")

        #gets the most recent uid from the user table
        c.execute(''' SELECT usr FROM users ORDER BY usr DESC LIMIT 1; ''')
        result = c.fetchone()

        if result: 
            uid=result[0]+1
        else: #if the user table is empty and there is no users
            uid=1

        c.execute(''' INSERT INTO users (usr, name, email, phone, pwd) VALUES (:uid, :username, :email, :phone, :password);''',{
            'uid': uid, 'username': username, 'email': email, 'phone': phone, 'password': password
        })

        conn.commit()