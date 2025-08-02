const openEyeFile = document.getElementById("openEyeFile").src;
const closeEyeFile = document.getElementById("closeEyeFile").src;

const loginForm =  document.forms["loginForm"];

const pwdField = loginForm["pwd"];
const eye_icon=  document.getElementById('eyeIcon');


eye_icon.addEventListener("click", ()=> togglePassword());


function togglePassword() {
    pwdField.type === "password" ? openEye() : closeEye();
}

function openEye(){
    pwdField.type = "text";
    eye_icon.src = openEyeFile;
}
function closeEye(){
    pwdField.type = "password";
    eye_icon.src= closeEyeFile;
}



