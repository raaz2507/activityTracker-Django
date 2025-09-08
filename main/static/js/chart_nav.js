const navTogleBtn = document.getElementsByClassName('toggleNav_btn')[0];
const listItems = document.querySelectorAll('aside .chartsNav ul li .chart_name');
navTogleBtn.addEventListener('click', ()=>{
    console.log("click");
    listItems.forEach((item)=>{
        console.log(item);
        item.classList.toggle('hide');

    });
});