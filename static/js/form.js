function togglePassword() {
    const passwordInput = document.querySelector('input[name="password"]');
    if (passwordInput) {
      passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
    }
  }
  function togglePassword2() {
    const passwordInput = document.querySelector('input[name="password_confirm"]');
    if (passwordInput) {
      passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
    }
  }