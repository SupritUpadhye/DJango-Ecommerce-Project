// Login Form Validation for email and Password

function validateEmail() {
    var inputgroup = document.getElementById("email").closest(".input-group");
    var email = document.getElementById("email").value;
    var emailerror = inputgroup.querySelector("#email-error");
    var pattern = /^[A-Za-z\._\-0-9]*[@][A-Za-z]*[\.][a-z]{2,4}$/;
    var atSymbol = email.indexOf('@');  
    var dot= email.lastIndexOf('.')

    if(atSymbol < 1){
        inputgroup.classList.remove("success");
        inputgroup.classList.add("error");
        emailerror.innerHTML = "Please Enter valid Email";
    }
    else if(dot <= atSymbol + 2){
        inputgroup.classList.remove("success");
        inputgroup.classList.add("error");
        emailerror.innerHTML = "Please Enter valid Email";
    }
    else if(email === ""){
        inputgroup.classList.remove("success");
        inputgroup.classList.add("error");
        emailerror.innerHTML = "Email Cannot be Empty";
    }
    else if (email.match(pattern)) {
        inputgroup.classList.add("success");
        inputgroup.classList.remove("error");
    }
}


// Password Validation 
function validatePassword() {
    var inputgroup = document.getElementById("password").closest(".input-group");
    var password = document.getElementById("password").value;
    var passworderror = inputgroup.querySelector("#password-error");

    // Define regex patterns for each requirement
    var lengthPattern = /.{8,}/;
    var uppercasePattern = /[A-Z]/;
    var lowercasePattern = /[a-z]/;
    var numberPattern = /[1-9]/;
    var specialCharPattern = /[^A-Za-z0-9]/;

    // Check if all patterns are satisfied
    if (lengthPattern.test(password) &&
        uppercasePattern.test(password) &&
        lowercasePattern.test(password) &&
        numberPattern.test(password) &&
        specialCharPattern.test(password)) {
        inputgroup.classList.add("success");
        inputgroup.classList.remove("error");
    }
    else if(password === ""){
        inputgroup.classList.remove("success");
        inputgroup.classList.add("error");
        passworderror.innerHTML = "Password Cannot be Empty";
    } 
    else {
        inputgroup.classList.remove("success");
        inputgroup.classList.add("error");
    }
}

// Add event listeners to trigger validation on input change
document.getElementById("email").addEventListener("input", validateEmail);
document.getElementById("password").addEventListener("input", validatePassword);

// Add event listeners to trigger label movement on input focus and content
document.getElementById("email").addEventListener("focus", moveLabel);
document.getElementById("email").addEventListener("input", moveLabel);
document.getElementById("password").addEventListener("focus", moveLabel);
document.getElementById("password").addEventListener("input", moveLabel);


function moveLabel() {
    var input = this;
    var label = input.nextElementSibling;

    if (input.value.trim() !== "") {
        label.style.top = "-4rem"; // Move label up if input has content
    } else {
        label.style.top = "0"; // Move label down if input is empty
    }
}
