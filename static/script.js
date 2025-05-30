document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('passwordInput');
    const toggleButton = document.getElementById('togglePassword');
    const checkButton = document.getElementById('checkButton');
    const resultsSection = document.getElementById('results');
    const loadingSection = document.getElementById('loading');

    // Toggle password visibility
    toggleButton.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        toggleButton.textContent = type === 'password' ? '👁️' : '🙈';
    });

    // Check password on button click
    checkButton.addEventListener('click', checkPassword);

    // Check password on Enter key
    passwordInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            checkPassword();
        }
    });

    // Real-time input validation
    passwordInput.addEventListener('input', function() {
        checkButton.disabled = this.value.trim() === '';
    });

    async function checkPassword() {
        const password = passwordInput.value.trim();

        if (!password) {
            alert('Please enter a password');
            return;
        }

        // Show loading
        resultsSection.style.display = 'none';
        loadingSection.style.display = 'block';
        checkButton.disabled = true;

        try {
            const response = await fetch('/check_password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ password: password })
            });

            const data = await response.json();

            if (response.ok) {
                displayResults(data);
            } else {
                alert(data.error || 'An error occurred');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Network error. Please try again.');
        } finally {
            loadingSection.style.display = 'none';
            checkButton.disabled = false;
        }
    }

    function displayResults(data) {
        // Update strength indicator
        const strengthFill = document.getElementById('strengthFill');
        const strengthText = document.getElementById('strengthText');

        const strengthPercentage = (data.strength / 5) * 100;
        strengthFill.style.width = strengthPercentage + '%';
        strengthFill.className = `strength-fill ${data.strength_class}`;
        strengthText.textContent = `${data.strength_desc} (${data.strength}/5)`;
        strengthText.className = `strength-text ${data.strength_class}`;

        // Update password details
        document.getElementById('lengthCount').textContent = data.length;
        document.getElementById('lowerCount').textContent = data.lower_count;
        document.getElementById('upperCount').textContent = data.upper_count;
        document.getElementById('numCount').textContent = data.num_count;
        document.getElementById('specialCount').textContent = data.special_count;
        document.getElementById('spaceCount').textContent = data.wspace_count;

        // Update HIBP results
        const hibpSection = document.getElementById('hibpResults');
        if (data.pwned_count === null) {
            hibpSection.innerHTML = '<p>⚠️ Could not check breach database</p>';
            hibpSection.className = 'hibp-section hibp-warning';
        } else if (data.pwned_count === 0) {
            hibpSection.innerHTML = '<p>✅ Good news! This password was not found in known data breaches.</p>';
            hibpSection.className = 'hibp-section hibp-safe';
        } else {
            hibpSection.innerHTML = `<p>⚠️ Warning! This password has appeared in data breaches <strong>${data.pwned_count.toLocaleString()}</strong> times.<br>It's strongly recommended to use a different password.</p>`;
            hibpSection.className = 'hibp-section hibp-warning';
        }

        // Update remarks
        const remarksSection = document.getElementById('remarks');
        if (data.remarks) {
            remarksSection.innerHTML = `<p><strong>💡 Hint:</strong> ${data.remarks}</p>`;
            remarksSection.style.display = 'block';
        } else {
            remarksSection.style.display = 'none';
        }

        // Show results
        resultsSection.style.display = 'block';
    }
});
