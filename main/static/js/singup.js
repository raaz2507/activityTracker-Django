document.addEventListener("DOMContentLoaded", ()=>{
    new sinupDashbord();
});

class sinupDashbord{
    #elemts={};
    #file={};
    constructor(){
        this.#getElements();
        this.#setEvents();
    }
    
    #getElements(){
       
        this.#file["openEyeFile"] = document.getElementById("openEyeFile").src;
        this.#file["closeEyeFile"] = document.getElementById("closeEyeFile").src;

        this.#elemts["pwdEyeIcon"] = document.getElementById("pwdEyeIcon");
        this.#elemts["cpwdEyeIcon"] = document.getElementById("cpwdEyeIcon");

        this.#elemts["form"] = document.forms["singupForm"];
        this.#elemts["pwdInput"] = this.#elemts["form"]["pwd"];
        this.#elemts["cpwdInput"] = this.#elemts["form"]["cpwd"];
        this.#elemts["submit_btn"] = this.#elemts["form"].querySelector('[type="submit"]');
        this.#elemts[ "pwdMsg" ] = document.getElementById("pwdMsg");
        this.#elemts[ "cpwdMsg" ] = document.getElementById("cpwdMsg");
    }
    #setEvents(){
        const {pwdEyeIcon, cpwdEyeIcon, pwdInput, cpwdInput , submit_btn}=this.#elemts;
        //password view eye related event
        pwdEyeIcon.addEventListener('click', ()=> this.#toggleIcon(pwdEyeIcon, pwdInput));
        cpwdEyeIcon.addEventListener('click', ()=> this.#toggleIcon(cpwdEyeIcon, cpwdInput));

        pwdInput.addEventListener('input', (event)=>{
            const {pwdMsg} =this.#elemts;
            pwd = event.target.value;
            const valid = pwd.length>=4 && pwd.length<=6 ;
            pwdMsg.innerHTML =  valid ? "password proside..": "password allow only 4 to 6 length";
            pwdMsg.style.color = valid ? "green": "red";
            console.log(pwd, valid)
        });
        //password check releted revents
        cpwdInput.addEventListener("input", ()=>this.#checkPassword());

    }

    #toggleIcon(icon, pinput){
        const {openEyeFile, closeEyeFile}=this.#file;

        pinput.type == "password" ? openEye(icon, pinput) : closeEye(icon, pinput);

        function openEye(icon, pinput){
            pinput.type= "text";
            icon.src = openEyeFile;//`static/img/eyeOpen.svg`;
        }

        function closeEye(icon, pinput){
            pinput.type="password";
            icon.src = closeEyeFile;//`static/img/eyeClose.svg`;
        }

    }
    #checkPassword(){
        const { pwdInput, cpwdInput, submit_btn , cpwdMsg} = this.#elemts;

        const match = pwdInput.value === cpwdInput.value;
        submit_btn.disabled = !match;
        cpwdMsg.textContent = match ? "Password Matched ✅" : "Passwords don't match ❌";
        cpwdMsg.style.color = match ? "green" : "red";
    }

    // #checkPassword(){
    //     const { pwdInput, cpwdInput, submit_btn}= this.#elemts;
    //     submit_btn.disabled = pwdInput.value ===  cpwdInput.value ?  false : true;
    //     console.log(submit_btn.disabled);
    //     return submit_btn.disabled;
    // }
}