const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

const main = document.getElementsByTagName('main')[0];
main.addEventListener('click',(event)=>{
    
    const target =  event.target;
    console.log(target);
    const favBtn = target.closest('.favBtn');
    const activityCard = target.closest(".activity_card");
    if (favBtn){
        console.log(favBtn, favBtn.dataset.activity_id);
        const activityId = favBtn.dataset.activity_id;

        fetch(`/toggleFavActivity/${activityId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                console.log(data.message);
                // icon toggle logic
                if(data.action === "added"){
                    console.log("added");
                    // target.classList.add("active"); 
                    favBtn.innerHTML = `<img src=${star_fill_Icon} alt="icon">`;
                } else {
                    console.log("remove");
                    favBtn.innerHTML = `<img src=${start_empty_Icon} alt="icon">`;
                }
            } else {
                console.error(data.message);
            }
        });
         
    }else if (activityCard){
        //  console.log(activityCard, activityCard.dataset.activity_id);
         window.location.href = activityCard.dataset.form_url;
    }   
});










// const favrateActivitys =  document.getElementById('favrateActivitys');
// const allActivitys =  document.getElementById('allActivitys');
// const userDefineActivitys =  document.getElementById('userDefineActivitys');

// // addExampleCard(favrateActivitys);
// // addExampleCard(allActivitys);
// // addExampleCard(userDefineActivitys);

// function addExampleCard(element){
//     let htmlText='';
//     for (let i=1; i<=9; i++){
//         htmlText+= `<div class="activity_card" data-activity-id="${i}">
//             <h1>Example</h1> 
//             <ul class="triger">
//                 <h3 >Triger/Cose</h3>
//                 <li>cose1</li>
//                 <li>cose1</li>
//                 <li>cose1</li>
//                 <li>cose1</li>
//             </ul>
            
//             <ul class="source">
//                 <h3>Source/Action</h3>
//                 <li>cose1</li>
//                 <li>cose1</li>
//                 <li>cose1</li>
//                 <li>cose1</li>
//             </ul>
//         </div>`;
//     }
//     element.innerHTML = htmlText;
// }