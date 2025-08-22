const userAccountTable_tbody = document.querySelector("#userAccountTable tbody");
const userDataTable = document.getElementById("userDataTable");
const userDataTable_tbody = userDataTable.querySelector('tbody');
const messageBlock =document.getElementById("messageBlock");


userAccountTable_tbody.addEventListener('click',async (event)=>{
    const target = event.target;
    // console.log(target);
    const row = target.closest('tr');
    if (!row) return ;

    const userid = row.dataset.id;
    // console.log(userid);
    
    // event.target.parentElement.classList.contains('deleteBtn')
    
    if (event.target.closest('.deleteBtn')){
        // console.log(event.target.closest('.deleteBtn'));
        try{
            const res =  await fetch(`/usr_acc_man/delete/${userid}/`);
            const resData = await res.json();
            
            const tbodyFrag = document.createDocumentFragment();
            resData.userAccData.forEach(data=>{
                const tr = document.createElement('tr');
                tr.innerHTML = `
                <td>${ data.usr_id }</td>
                <td>${ data.user_name }</td>
                <td>${ data.pwd }</td>
                <td><input type="checkbox" name="active" id="active" value="True"></td>
                <td> 
                    <button class="deleteBtn">
                        <img src="/static/img/trash-can.svg"  alt="Delete" title="delete record" style="width:.9rem;">
                    </button>
                </td>`;
                tr.dataset.id = data.usr_id;
                tbodyFrag.appendChild(tr);
            });
            userAccountTable_tbody.innerHTML="";
            userAccountTable_tbody.appendChild(tbodyFrag);
            
            // messages
            messageBlock.className = resData.messages.tag;
            messageBlock.innerHTML = resData.messages.msg;
            setTimeout(() => {
                messageBlock.className = "hidden";
            }, 3000);

            }catch(error){ console.log("get an error ", error);};
            
        }
    
    else if (target.tagName === "TD"){
        // const trow = event.target.closest('tr');
        // const userid = trow.dataset.id;
        // console.log(userid);
        fetch(`/usr_acc_man/${userid}/`)
        .then(response => response.json())
        .then(user_data =>{
            
            const caption = userDataTable.querySelector('caption');
            userDataTable_tbody.innerHTML = ""; //clear privues 
            const tbodyFrag = document.createDocumentFragment();
            user_data.forEach( data =>{
                const tr = document.createElement("tr");
                caption.innerHTML = `id= ${data.usr_id}`;
                tr.innerHTML = `
                <td>${ data.date }</td>
                <td>${ data.start_time }</td>
                <td>${ data.end_time }</td>
                <td>${ data.source }</td>
                <td>${ data.trigger_reason }</td>
                <td>${ data.timesCount }</td>
                `
                tbodyFrag.appendChild(tr);
            });
            userDataTable_tbody.append(tbodyFrag);
        })
        .catch(error =>{ console.error("Error getting user Data.", error) });
    }
});