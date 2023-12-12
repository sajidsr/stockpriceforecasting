// Get the form element
const form = document.getElementById('register-form');

// Get the form fields
const fnameField = form.elements['fname'];
const lnameField = form.elements['lname'];
const usernameField = form.elements['username'];
const emailField = form.elements['email'];
const passwordField = form.elements['password'];
const confirmPasswordField = form.elements['confirm-password'];

// Get the error message elements for each field
const fnameError = document.getElementById('fname-error');
const lnameError = document.getElementById('lname-error');
const usernameError = document.getElementById('username-error');
const emailError = document.getElementById('email-error');
const passwordError = document.getElementById('password-error');
const confirmPasswordError = document.getElementById('confirm-password-error');

// Define regular expressions for email, password, and username validation
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).{8,}$/;
const usernameRegex = /^[a-zA-Z0-9!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]{6,}$/;

function validateForm(event) {
  // Prevent the form from submitting
  event.preventDefault();

  // Reset error messages and field styles
  fnameError.innerHTML = '';
  lnameError.innerHTML = '';
  usernameError.innerHTML = '';
  emailError.innerHTML = '';
  passwordError.innerHTML = '';
  confirmPasswordError.innerHTML = '';
  fnameField.classList.remove('error');
  lnameField.classList.remove('error');
  usernameField.classList.remove('error');
  emailField.classList.remove('error');
  passwordField.classList.remove('error');
  confirmPasswordField.classList.remove('error');

  // Validate the first name field
  if (fnameField.value.trim() === '') {
    fnameField.classList.add('error');
    fnameError.innerHTML = 'First name is required';
    return;
  } else if (/\d/.test(fnameField.value.trim()) || /[!@#$%^&*(),.?":{}|<>]/.test(fnameField.value.trim())) {
    fnameField.classList.add('error');
    fnameError.innerHTML = 'First name cannot contain digits or special characters';
    return;
  }

  // Validate the last name field
  if (lnameField.value.trim() === '') {
    lnameField.classList.add('error');
    lnameError.innerHTML = 'Last name is required';
    return;
  } else if (/\d/.test(lnameField.value.trim()) || /[!@#$%^&*(),.?":{}|<>]/.test(lnameField.value.trim())) {
    lnameField.classList.add('error');
    lnameError.innerHTML = 'Last name cannot contain digits or special characters';
    return;
  }

  // Validate the username field
  if (!usernameRegex.test(usernameField.value.trim())) {
    usernameField.classList.add('error');
    usernameError.innerHTML = 'Username must be at least 6 characters long and can contain letters, digits, and special characters !@#$%^&*()_+-=[]{};\\:\'",.<>/?';
    return;
  }

  // Validate the email field
  if (!emailRegex.test(emailField.value.trim())) {
    emailField.classList.add('error');
    emailError.innerHTML = 'Please enter a valid email address';
    return;
  }

  // Validate the password field
  if (!passwordRegex.test(passwordField.value.trim())) {
    passwordField.classList.add('error');
    passwordError.innerHTML = 'Please enter a password that contains at least one uppercase letter, one lowercase letter, one digit, and one special character, and is at least 8 characters long';
    return;
  }

  // Validate the confirm password field
  if (confirmPasswordField.value.trim() !== passwordField.value.trim()) {
    confirmPasswordField.classList.add('error');
    confirmPasswordError.innerHTML = 'Please make sure your passwords match';
    return;
  } 


  // If there are no errors, submit the form
 
    form.submit();
}

// Add an event listener to the form's submit button
form.addEventListener('submit', validateForm);