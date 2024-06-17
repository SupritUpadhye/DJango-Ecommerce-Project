// Form Validation for registration and login form
// Email Validation
function validateFirstName(){
    var inputgroup = document.getElementById("first-name").closest(".input-group");
    var firstName = document.getElementById("first-name").value;
    var firstNameError = inputgroup.querySelector("#first-name-error");
    var namepattern = /^[A-Za-z]+$/;

    if(firstName.match(namepattern) && firstName.length>=2){
        inputgroup.classList.add("success");
        inputgroup.classList.remove("error");
    }else if(firstName === ""){
        inputgroup.classList.remove("success");
        inputgroup.classList.add("error");
        firstNameError.innerHTML = "Name Cannot be Empty";
    }
    else{
        inputgroup.classList.remove("success");
        inputgroup.classList.add("error");
        firstNameError.innerHTML = "Please Enter valid Name";
    }
}

function validateLastName(){
    var inputgroup = document.getElementById("last-name").closest(".input-group");
    var lastName = document.getElementById("last-name").value;
    var lastNameError = inputgroup.querySelector("#last-name-error");
    var namepattern = /^[A-Za-z]+$/;

    if(lastName.match(namepattern) && lastName.length>2){
        inputgroup.classList.add("success");
        inputgroup.classList.remove("error");
    }else if(lastName === ""){
        inputgroup.classList.remove("success");
        inputgroup.classList.add("error");
        lastNameError.innerHTML = "Name Cannot be Empty";
    }
    else{
        inputgroup.classList.remove("success");
        inputgroup.classList.add("error");
        lastNameError.innerHTML = "Please Enter valid Name";
    }
}

function validateMobN0(){
    var inputgroup = document.getElementById("mob-no").closest(".input-group");
    var mobNo = document.getElementById("mob-no").value;
    var mobNoError = inputgroup.querySelector("#mob-no-error");
    var mobNoStr = mobNo.toString();
    var mobNoPattern = mobNoStr.length;

    if(mobNoPattern == 10 ){
        inputgroup.classList.add("success");
        inputgroup.classList.remove("error");
    }else{
        inputgroup.classList.remove("success");
        inputgroup.classList.add("error");
        mobNoError.innerHTML = "Please Enter Valid Mobile No.";
    }

}

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
    else if(email === ""){
        inputgroup.classList.remove("success");
        inputgroup.classList.add("error");
        emailerror.innerHTML = "Email Cannot be Empty";
    }
    else if(dot <= atSymbol + 2){
        inputgroup.classList.remove("success");
        inputgroup.classList.add("error");
        emailerror.innerHTML = "Please Enter valid Email";
    }
    else if (email.match(pattern)) {
        inputgroup.classList.add("success");
        inputgroup.classList.remove("error");
    } else {
        inputgroup.classList.remove("success");
        inputgroup.classList.add("error");
        emailerror.innerHTML = "Please Enter valid Email";
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
        passworderror.innerHTML = "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, and one special character";
    }
}
// Confirm Password Validation
function validateCpassword(){
    var password = document.getElementById("password").value;
    var inputgroup = document.getElementById("Cpassword").closest(".input-group");
    var Cpassword = document.getElementById("Cpassword").value;
    var Cpassworderror = inputgroup.querySelector("#Cpassword-error");

    if (password === Cpassword && password.length>=8) {
            inputgroup.classList.add("success");
            inputgroup.classList.remove("error");
        }
        else if(Cpassword === ""){
            inputgroup.classList.remove("success");
            inputgroup.classList.add("error");
            Cpassworderror.innerHTML = "Password Cannot be Empty";
        }
        else {
            inputgroup.classList.remove("success");
            inputgroup.classList.add("error");
            Cpassworderror.innerHTML = "Passwords did not match";
        }

}

// Add event listeners to trigger validation on input change
document.getElementById("first-name").addEventListener("input", validateFirstName);
document.getElementById("last-name").addEventListener("input", validateLastName);
document.getElementById("email").addEventListener("input", validateEmail);
document.getElementById("mob-no").addEventListener("input", validateMobN0);
document.getElementById("password").addEventListener("input", validatePassword);
document.getElementById("Cpassword").addEventListener("input", validateCpassword);

// Add event listeners to trigger label movement on input focus and content
document.getElementById("first-name").addEventListener("focus", moveLabel);
document.getElementById("first-name").addEventListener("input", moveLabel);
document.getElementById("last-name").addEventListener("focus", moveLabel);
document.getElementById("last-name").addEventListener("input", moveLabel);
document.getElementById("email").addEventListener("focus", moveLabel);
document.getElementById("email").addEventListener("input", moveLabel);
document.getElementById("mob-no").addEventListener("focus", moveLabel);
document.getElementById("mob-no").addEventListener("input", moveLabel);
document.getElementById("password").addEventListener("focus", moveLabel);
document.getElementById("password").addEventListener("input", moveLabel);
document.getElementById("Cpassword").addEventListener("focus", moveLabel);
document.getElementById("Cpassword").addEventListener("input", moveLabel);


function moveLabel() {
    var input = this;
    var label = input.nextElementSibling;

    if (input.value.trim() !== "") {
        label.style.top = "-4rem"; // Move label up if input has content
    } else {
        label.style.top = "0"; // Move label down if input is empty
    }
}



// Sweetalert for Messages

