//  console.log(`${document.forms['addRecordForm'].innerHTML}`);

const all_forms =  document.forms;

Array.from(all_forms).forEach(form=>{
    
    all_dates_input = form.querySelectorAll('input[type="date"]');
    Array.from(all_dates_input).forEach(date_input=>{
        const today_date_inputBtn = createElement('button' , 'Today');
        date_input.after(today_date_inputBtn);
        // console.log(date_input);
        today_date_inputBtn.addEventListener('click',(e)=>{
            e.preventDefault();
            date_input.value = getCurrentDate();
        });
    });
    
    all_time_input = form.querySelectorAll('input[type="time"]');
    Array.from(all_time_input).forEach(time_input =>{
        const now_time_inputBtn = createElement('button' , 'Now');
        time_input.after(now_time_inputBtn);
        // console.log(time_input);
        now_time_inputBtn.addEventListener('click', (e)=>{
            e.preventDefault();
            time_input.value = getCurrentTime(); 
        });
    });

    //adding clock widet
    Array.from(all_time_input).forEach(time_input =>{
        const clock_widget_btn = createElement('div' , '');
        clock_widget_btn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto;" viewBox="0 0 640 640">
                                        <path d="M528 320C528 434.9 434.9 528 320 528C205.1 528 112 434.9 112 320C112 205.1 205.1 112 320 112C434.9 112 528 205.1 528 320zM64 320C64 461.4 178.6 576 320 576C461.4 576 576 461.4 576 320C576 178.6 461.4 64 320 64C178.6 64 64 178.6 64 320zM296 184L296 320C296 328 300 335.5 306.7 340L402.7 404C413.7 411.4 428.6 408.4 436 397.3C443.4 386.2 440.4 371.4 429.3 364L344 307.2L344 184C344 170.7 333.3 160 320 160C306.7 160 296 170.7 296 184z"/>
                                        </svg>`; 
        time_input.after(clock_widget_btn);
        clock_widget_btn.style.width = '2rem';
        clock_widget_btn.addEventListener('click', ()=>{
            console.log('click');
        });
    });
    
})

function createElement(ele_type, inner_text){
    const newElemt =  document.createElement(ele_type);
    newElemt.innerText = inner_text;
    return newElemt;
}
function getCurrentDate(){
    return  new Date().toISOString().split('T')[0];
}
function getCurrentTime(){
    const currTime = new Date().toTimeString().split(' ')[0];
    
    timeArr = currTime.split(':');
    time = `${timeArr[0]}:${timeArr[1]}`;
    // console.log(time);
    return time;
}