import re

pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,12}$'
password = "Iam1@good "  # Example password

if re.match(pattern, password):
    print("Password is valid.")
else:
    print("Password is invalid.")
