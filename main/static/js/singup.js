document.addEventListener("DOMContentLoaded", () => {
    const pwd1 = document.getElementById("id_password1");
    const pwd2 = document.getElementById("id_password2");
    const msg = document.createElement("small");
    msg.style.color = "red";
    pwd2.parentElement.appendChild(msg);

    pwd2.addEventListener("input", () => {
        if (pwd2.value !== pwd1.value) {
            msg.textContent = "Passwords do not match!";
        } else {
            msg.textContent = "";
        }
    });
});