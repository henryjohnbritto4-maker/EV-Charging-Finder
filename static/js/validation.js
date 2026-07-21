document.addEventListener("DOMContentLoaded", function () {

    // ---------- Register form: password match check ----------
    const registerForm = document.getElementById("registerForm");

    if (registerForm) {
        const password = document.getElementById("password");
        const confirmPassword = document.getElementById("confirmPassword");

        registerForm.addEventListener("submit", function (e) {
            let valid = true;

            clearError(password);
            clearError(confirmPassword);

            if (password.value.length < 6) {
                showError(password, "Password must be at least 6 characters.");
                valid = false;
            }

            if (password.value !== confirmPassword.value) {
                showError(confirmPassword, "Passwords do not match.");
                valid = false;
            }

            if (!valid) {
                e.preventDefault();
            }
        });

        // Live feedback as user types
        confirmPassword.addEventListener("input", function () {
            if (confirmPassword.value && confirmPassword.value !== password.value) {
                showError(confirmPassword, "Passwords do not match.");
            } else {
                clearError(confirmPassword);
            }
        });
    }

    // ---------- Generic email format check ----------
    const emailInputs = document.querySelectorAll('input[type="email"], input[name="email"]');
    emailInputs.forEach(function (input) {
        input.addEventListener("blur", function () {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (input.value && !emailPattern.test(input.value)) {
                showError(input, "Please enter a valid email address.");
            } else {
                clearError(input);
            }
        });
    });

    // ---------- Helper functions ----------
    function showError(inputEl, message) {
        clearError(inputEl);
        const error = document.createElement("span");
        error.className = "form-error js-error";
        error.textContent = message;
        inputEl.parentElement.appendChild(error);
        inputEl.style.borderColor = "#d9302f";
    }

    function clearError(inputEl) {
        const existing = inputEl.parentElement.querySelector(".js-error");
        if (existing) existing.remove();
        inputEl.style.borderColor = "";
    }

});