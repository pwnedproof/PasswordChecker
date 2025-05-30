from flask import Flask, render_template, request, jsonify
import string
import hashlib
import requests

app = Flask(__name__)

def check_hibp(password):
    """Check if password has been breached using HIBP API"""
    try:
        sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1_password[:5]
        suffix = sha1_password[5:]

        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()

        hashes = (line.split(':') for line in res.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return int(count)
        return 0
    except requests.RequestException:
        return None

def analyze_password(password):
    """Analyze password strength and characteristics"""
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

    # Determine strength description and CSS class
    if strength == 1:
        strength_desc = "Very Weak"
        strength_class = "very-weak"
    elif strength == 2:
        strength_desc = "Weak"
        strength_class = "weak"
    elif strength == 3:
        strength_desc = "Okay"
        strength_class = "okay"
    elif strength == 4:
        strength_desc = "Good"
        strength_class = "good"
    elif strength == 5:
        strength_desc = "Very Strong"
        strength_class = "very-strong"

    pwned_count = check_hibp(password)

    return {
        'strength': strength,
        'strength_desc': strength_desc,
        'strength_class': strength_class,
        'length': len(password),
        'lower_count': lower_count,
        'upper_count': upper_count,
        'num_count': num_count,
        'wspace_count': wspace_count,
        'special_count': special_count,
        'pwned_count': pwned_count,
        'remarks': remarks
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    try:
        data = request.get_json()
        password = data.get('password', '')

        if not password:
            return jsonify({'error': 'Password cannot be empty'}), 400

        if len(password) > 128:
            return jsonify({'error': 'Password is too long'}), 400

        analysis = analyze_password(password)
        return jsonify(analysis)

    except Exception as e:
        return jsonify({'error': 'An error occurred while checking the password'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)