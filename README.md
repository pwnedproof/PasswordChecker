# Password Strength Checker created by Ilyssa Y (@pwnedproof)
A web application designed with cybersecurity best practices in mind to help users create stronger, safer passwords. 
It not only analyzes password complexity but also checks if the password has been exposed in data breaches using the trusted [Have I Been Pwned (HIBP) API].

## Cybersecurity 
Passwords remain the frontline defense against unauthorized access. Weak or reused passwords are a major security vulnerability that cyber attackers exploit.
This tool empowers users to understand the strength of their passwords and warns them if their passwords have appeared in known breaches which are critical steps toward improving personal and organizational cybersecurity.

## Features

- **Password Strength Analysis:** Evaluates password based on length, use of lowercase, uppercase, numbers, special characters, and spaces.
- **Breach Check:** Uses HIBP API to determine if your password has been compromised in any known data breaches.
- **User-friendly Interface:** Responsive and interactive frontend with clear visual indicators.
- **Privacy-first:** Passwords are never sent to the server in plain text; only hashed prefixes are used when querying the breach database.

## Technologies Used

- Python
- Flask (Backend web framework)
- HTML, CSS, JavaScript (Frontend)
- Have I Been Pwned API (for password breach checks)
