  function toggleForm(formId) {
    // Hide both forms
    document.getElementById('student').classList.add('hidden');
    document.getElementById('signup').classList.add('hidden');

    // Show requested form
    document.getElementById(formId).classList.remove('hidden');
  }

function togglePassword(id) {
    const passwordInput = document.getElementById(id);

 passwordInput.type = passwordInput.type === "password" ? "text" : "password";
}

  // Default form on page load
  toggleForm('student');
