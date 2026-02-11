  function toggleForm(formId) {
    // Hide both forms
    document.getElementById('student').classList.add('hidden');
    document.getElementById('signup').classList.add('hidden');

    // Show requested form
    document.getElementById(formId).classList.remove('hidden');
  }

function togglePassword() {
    const passwordInput = document.getElementById("password");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}

  // Default form on page load
  toggleForm('student');
