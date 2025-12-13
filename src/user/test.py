from email_validator import validate_email, EmailNotValidError

email = input("Введите email:  ")

def check(email: str):
    try:
        v = validate_email(email) 
        print("Valid Email")
    except EmailNotValidError as e:
        print(str(e))

check(email)

