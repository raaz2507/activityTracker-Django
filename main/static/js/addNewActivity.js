const source_filds = document.getElementById('source_filds');
const triger_filds = document.getElementById('triger_filds');
const extra_filds = document.getElementById('extra_filds');

const addNewActivtyForm = document.forms["addNewActivtyForm"];

addNewActivtyForm.addEventListener("submit", ()=>{
     // hidden input elements
    // e.preventDefault();
    const sourceInput = document.getElementById('id_source');
    const triggerInput = document.getElementById('id_trigger');
    const extraInput = document.getElementById('id_extra');

    function collectFieldData(filed){
        const inputs = filed.querySelectorAll('input[type="text"]');

        let data={};
        inputs.forEach( input=>{
            const value = input.value.trim();
            if (value !== ""){
                data[value]= "";
            }
        });
        console.log(data);
        return data;
    }
    console.log(JSON.stringify(collectFieldData(source_filds)));
    sourceInput.value = JSON.stringify(collectFieldData(source_filds));
    triggerInput.value = JSON.stringify(collectFieldData(triger_filds));
    extraInput.value = JSON.stringify(collectFieldData(extra_filds));
});


// document.addEventListener("DOMContentLoaded", ()=>{
//     source_filds.append(addInputBlock(source_filds, "source_fild[]"));
//     triger_filds.append(addInputBlock(triger_filds, "trigger_fild[]" ));
//     extra_filds.append(addInputBlock(extra_filds, "extra_fild[]"));
// });


document.addEventListener("DOMContentLoaded", ()=>{
    // Convert JSON string from hidden inputs to object
    const sourceData = JSON.parse(document.getElementById('id_source').value || "{}");
    const triggerData = JSON.parse(document.getElementById('id_trigger').value || "{}");
    const extraData = JSON.parse(document.getElementById('id_extra').value || "{}");

    // Populate inputs dynamically
    for(const key in sourceData){
        source_filds.append(addInputBlock(source_filds, "source_fild[]", key));
    }
    for(const key in triggerData){
        triger_filds.append(addInputBlock(triger_filds, "trigger_fild[]", key));
    }
    for(const key in extraData){
        extra_filds.append(addInputBlock(extra_filds, "extra_fild[]", key));
    }

    // अगर data empty हो, तो कम से कम एक input field डाल दें
    if(Object.keys(sourceData).length === 0) source_filds.append(addInputBlock(source_filds, "source_fild[]"));
    if(Object.keys(triggerData).length === 0) triger_filds.append(addInputBlock(triger_filds, "trigger_fild[]"));
    if(Object.keys(extraData).length === 0) extra_filds.append(addInputBlock(extra_filds, "extra_fild[]"));
});


function addInputBlock(parent_fild, inputName, value=""){
    const inputContainer =  document.createElement('div');
    inputContainer.classList.add("inputContainer");
    
    const input = document.createElement('input');
    input.style.padding = "10px 1rem";
    input.type= 'text';
    input.name= inputName;
    input.placeholder = "Enter Source";
    input.value = value;  // ← prefill value


    const addBtn =  document.createElement('button');
    addBtn.classList.add('btn', 'addBtn');
    addBtn.type = "button";
    addBtn.textContent = "+";
    // addBtn.style.fontSize = "1rem";
    // addBtn.style.color = "#fff";
    // addBtn.style.width =  "2rem";
    // addBtn.style.height =  "2rem";
    // addBtn.style.borderRadius = "50%";
    // addBtn.style.background = "green";
    addBtn.addEventListener('click', ()=>{ 
    parent_fild.insertBefore(addInputBlock(parent_fild, inputName), inputContainer.nextSibling);
    });


    const rmBtn =  document.createElement('button');
    rmBtn.classList.add('btn', 'removeBtn');
    rmBtn.type = "button";
    rmBtn.textContent = "—";
    // rmBtn.style.color = "#fff";
    // rmBtn.style.width =  "2rem";
    // rmBtn.style.height =  "2rem";
    // rmBtn.style.borderRadius = "50%";
    // rmBtn.style.background = "red";
    rmBtn.addEventListener('click', ()=>{ inputContainer.remove()});

    
    // inputContainer.style.width = "100%";
    // inputContainer.style.display = "flex";
    // inputContainer.style.alignItems = "center";
    // inputContainer.style.gap = "10px";
    // inputContainer.style.flex = "1";

    inputContainer.appendChild(rmBtn);
    inputContainer.appendChild(input);
    inputContainer.appendChild(addBtn);
    return inputContainer;
}


// imgae preview ke liye 


document.addEventListener("DOMContentLoaded", ()=>{
    const aTag = addNewActivtyForm.querySelectorAll('a')[0];
    aTag.style.display = "none";
    console.log(aTag);
    
    const imgPreviewBox =  document.createElement('div');
    imgPreviewBox.style.width = "120px";   // preview box size
    imgPreviewBox.style.height = "120px";
    imgPreviewBox.style.overflow = "hidden";
    imgPreviewBox.style.border = "1px solid #ccc";
    imgPreviewBox.style.borderRadius = "10px";
    imgPreviewBox.style.marginTop = "10px";
    
    const img =  document.createElement("img");
    img.src = aTag.href;
    img.style.width = "100%";
    img.style.height = "100%";
    img.style.objectFit = "cover";  // 👈 main property

    imgPreviewBox.append(img);
    aTag.after(imgPreviewBox);
    const input = document.getElementById("id_icon");
    input.addEventListener('change', ()=>{
        // this event show the preview img before uplaad
        const file = input.files[0];
        if (file){
            const reader =  new FileReader();
            reader.addEventListener('load', (e)=>{
                img.src = e.target.result;
            });
            reader.readAsDataURL(file); // file को base64 में convert करके img src में डाल देगा
        }
       
    });

});