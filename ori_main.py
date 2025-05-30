
import string
import hashlib
import requests
import getpass

def check_hibp(password):
    """Check if password has been breached using HIBP API"""
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_password[:5]
    suffix = sha1_password[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    res = requests.get(url)

    #error handling
    try:
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data from HIBP API: {e}")
        return None

    #the script loops through the results and checks if the suffix is in the results
    hashes = (line.split(':') for line in res.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)
    return 0

def check_pwd():
    """Check password strength and security"""
    while True:
        password = getpass.getpass("Enter Your Password: ")
        if password.strip():
            break
        print("Error: Password cannot be empty. Please try again.")
    #checks the password strength and gives a score out of 5
    strength = 0
    remarks = ""
    lower_count = upper_count = num_count = wspace_count = special_count = 0

    for char in password:
        if char in string.ascii_lowercase:
            lower_count += 1
        elif char in string.ascii_uppercase:
            upper_count += 1
        elif char in string.digits:
            num_count += 1
        elif char.isspace():
            wspace_count += 1
        else:
            special_count += 1

    if lower_count >= 1:
        strength += 1
    if upper_count >= 1:
        strength += 1
    if num_count >= 1:
        strength += 1
    if special_count >= 1:
        strength += 1

    if len(password) >= 8:
        strength += 1
    else:
        remarks = "Consider using a longer password (at least 8 characters)."

    print(f"Password length: {len(password)}")
    print(f"Lowercase letters: {lower_count}")
    print(f"Uppercase letters: {upper_count}")
    print(f"Numbers: {num_count}")
    print(f"Special characters: {special_count}")
    print(f"Spaces: {wspace_count}")

    if strength == 1:
        print("Password strength: Very Weak (1/5)")
    elif strength == 2:
        print("Password strength: Weak (2/5)")
    elif strength == 3:
        print("Password strength: Okay (3/5)")
    elif strength == 4:
        print("Password strength: Good (4/5)")
    elif strength == 5:
        print("Password strength: Very Strong (5/5)")

    if remarks:
        print(f"Remarks: {remarks}")

    # Check against HIBP database
    print("\nChecking against known data breaches...")
    pwned_count = check_hibp(password)

    if pwned_count is None:
        print("Could not check against breach database due to network error.")
    elif pwned_count == 0:
        print("Good news! This password was not found in known data breaches.")
    else:
        print(f"Warning! This password has appeared in data breaches {pwned_count:,} times.")
        print("It's strongly recommended to use a different password.")

if __name__ == '__main__':
    print("=== Password Strength Checker ===")
    print("This tool will analyze your password strength and check if it has been compromised.")
    print()
    check_pwd()
