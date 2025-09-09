

export class PasswordToggler{
    constructor(document){
        // this.#getElemts();
        // this.#setEvents();
        this.#togglePwd(document);
    }
    // #getElemts(){}
    // #setEvents(){}
    #togglePwd(document){
        const openEyeIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640">
                        <path d="M320 96C239.2 96 174.5 132.8 127.4 176.6C80.6 220.1 49.3 272 34.4 307.7C31.1 315.6 31.1 324.4 34.4 332.3C49.3 368 80.6 420 127.4 463.4C174.5 507.1 239.2 544 320 544C400.8 544 465.5 507.2 512.6 463.4C559.4 419.9 590.7 368 605.6 332.3C608.9 324.4 608.9 315.6 605.6 307.7C590.7 272 559.4 220 512.6 176.6C465.5 132.9 400.8 96 320 96zM176 320C176 240.5 240.5 176 320 176C399.5 176 464 240.5 464 320C464 399.5 399.5 464 320 464C240.5 464 176 399.5 176 320zM320 256C320 291.3 291.3 320 256 320C244.5 320 233.7 317 224.3 311.6C223.3 322.5 224.2 333.7 227.2 344.8C240.9 396 293.6 426.4 344.8 412.7C396 399 426.4 346.3 412.7 295.1C400.5 249.4 357.2 220.3 311.6 224.3C316.9 233.6 320 244.4 320 256z"/>
                    </svg>`;
        const closeEyeIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640">
                        <path d="M73 39.1C63.6 29.7 48.4 29.7 39.1 39.1C29.8 48.5 29.7 63.7 39 73.1L567 601.1C576.4 610.5 591.6 610.5 600.9 601.1C610.2 591.7 610.3 576.5 600.9 567.2L504.5 470.8C507.2 468.4 509.9 466 512.5 463.6C559.3 420.1 590.6 368.2 605.5 332.5C608.8 324.6 608.8 315.8 605.5 307.9C590.6 272.2 559.3 220.2 512.5 176.8C465.4 133.1 400.7 96.2 319.9 96.2C263.1 96.2 214.3 114.4 173.9 140.4L73 39.1zM236.5 202.7C260 185.9 288.9 176 320 176C399.5 176 464 240.5 464 320C464 351.1 454.1 379.9 437.3 403.5L402.6 368.8C415.3 347.4 419.6 321.1 412.7 295.1C399 243.9 346.3 213.5 295.1 227.2C286.5 229.5 278.4 232.9 271.1 237.2L236.4 202.5zM120 221.9C110.6 212.5 95.4 212.5 86.1 221.9C76.8 231.3 76.7 246.5 86.1 255.8L360.2 530C369.6 539.4 384.8 539.4 394.1 530C403.4 520.6 403.5 505.4 394.1 496.1L120 221.9zM77.7 315.3C68.3 305.9 53.1 305.9 43.8 315.3C34.5 324.7 34.4 339.9 43.8 349.2L213.9 519.5C223.3 528.9 238.5 528.9 247.8 519.5C257.1 510.1 257.2 494.9 247.8 485.6L77.7 315.3z"/>
                    </svg>`;
        // const loginForm =  document.forms["loginForm"];
        Array.from(document.forms).forEach(form=>{
            const pwdFields = form.querySelectorAll('input[type="password"]');
            pwdFields.forEach(fild=>{
                const parentElement = fild.parentElement;
                // console.log(parentElement);
                
                const pwdInputContainer = document.createElement('div');
                pwdInputContainer.classList.add("pwdinputContainer");

                const eyeBox = document.createElement('div');
                eyeBox.innerHTML = closeEyeIcon;
                eyeBox.classList.add('eyeIcon');
                eyeBox.addEventListener('click', ()=>{togglePassword(fild, eyeBox)});

                parentElement.replaceChild(pwdInputContainer, fild);
                pwdInputContainer.appendChild(fild);
                pwdInputContainer.appendChild(eyeBox);
                
            });
        });

        function togglePassword(pwdField, eyeBox) {
            if (pwdField.type === "password"){
                pwdField.type = "text";
                eyeBox.innerHTML = openEyeIcon;
            } else{
                pwdField.type = "password";
                eyeBox.innerHTML = closeEyeIcon;
            }
        }
    }
}