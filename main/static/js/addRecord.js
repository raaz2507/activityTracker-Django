//  console.log(`${document.forms['addRecordForm'].innerHTML}`);

const addRecordForm= document.forms["addRecordForm"];
const dataType = addRecordForm['date'];
const startTime = addRecordForm['start_time'];
const endTime = addRecordForm['end_time'];
console.log(dataType, startTime, endTime);

document.addEventListener('DOMContentLoaded', ()=>{
    const TodayElem = createElement('button' , 'Today');
    dataType.after(TodayElem);
    TodayElem.addEventListener('click',(e)=>{
        e.preventDefault();
        dataType.value = getCurrentDate();
    });

    const startTimeElemt = createElement('button' , 'Now');
    startTime.after(startTimeElemt);
    startTimeElemt.addEventListener('click', (e)=>{
        e.preventDefault();
        startTime.value = getCurrentTime(); 
    });

    const endTimeElemt = createElement('button', 'Now');
    endTime.after(endTimeElemt);
    endTimeElemt.addEventListener('click', (e)=>{
        e.preventDefault();
        endTime.value =  getCurrentTime();
    });
});

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
    console.log(time);
    return time;
}