document.addEventListener("DOMContentLoaded", ()=>{
    const calObj = new calendar();
});
class calendar{
    #elements={};
    #currentYear;
    #days={};
    constructor(){
        this.#currentYear = new Date().getFullYear();
        this.#getElemets();
        this.#setEvents();
        // this.#generateMonthCalender(currentYear, currentMonth, elemts );
        this.#generateYearCalender(this.#currentYear);
    }
    async updateDateMarks(){
        // const {calenderContainer} = this.#elements;
        // this.#currentYear
        // console.log(JSON.stringify(this.#days));
        const data = await this.#get_calender_data();
        data.forEach((record)=>{
            const dateObj = new Date(record.date);
            const year= dateObj.getFullYear();
            const month = dateObj.getMonth();
            const date= dateObj.getDate();
            console.log(year, month, date);
            if (this.#days[year] && this.#days[year][month] && this.#days[year][month][date]){
                const calender_dateObj = this.#days[year][month][date];
                pop_up_data(calender_dateObj, record);
            }
        });
        function pop_up_data(calender_dateObj, record){
    calender_dateObj.classList.add('mark');
    calender_dateObj.style.position ="relative";

    // पहले से मौजूद wrapper check करो
    let wrapper = calender_dateObj.querySelector(".popup_data_block");
    if(!wrapper){
        wrapper = document.createElement('div');
        wrapper.classList.add("popup_data_block" ,"hidden");
        calender_dateObj.appendChild(wrapper);

        calender_dateObj.addEventListener('mouseover',()=>{
            wrapper.classList.remove("hidden");
        });
        calender_dateObj.addEventListener('mouseout',()=>{
            wrapper.classList.add("hidden");
        });
    }

    // हर record के लिए नया item बनाओ
    const item = document.createElement("div");
    item.innerHTML = `
        <div style="color: #ff4d4d;">Start Time: ${record.start_time}</div>
        <div style="color: #4da6ff;">End Time: ${record.end_time}</div>
        <div style="color: #33cc33;">Activity Name: ${record.activity_name}</div>
        <div style="color: #ffcc00;">Source: ${get_only_true(record.source)}</div>
        <div style="color: #ff66cc;">Trigger: ${get_only_true(record.trigger)}</div>
        <div style="color: #9966ff;">Extra: ${get_only_true(record.extra)}</div>
        <hr style="border:0.5px solid #555;">
    `;
    wrapper.appendChild(item);

    function get_only_true(obj){
        return Object.entries(obj)
            .filter(([_, value]) => value === true)
            .map(([key]) => key)
            .join(", ");
    }
}
        function pop_up_data_OLD(calender_dateObj, record){
                calender_dateObj.classList.add('mark');
                calender_dateObj.style.position ="relative";

                const dataContaner =  document.createElement('div');
                dataContaner.classList.add("popup_data_block" ,"hidden");
                dataContaner.innerHTML = `
                        <div style="color: #ff4d4d;">Start Time: ${record.start_time}</div>
                        <div style="color: #4da6ff;">End Time: ${record.end_time}</div>
                        <div style="color: #33cc33;">Activity Name: ${record.activity_name}</div>
                        <div style="color: #ffcc00;">Source: ${get_only_true(record.source)}</div>
                        <div style="color: #ff66cc;">Trigger: ${get_only_true(record.trigger)}</div>
                        <div style="color: #9966ff;">Extra: ${get_only_true(record.extra)}</div>
                        `;
                calender_dateObj.appendChild(dataContaner);

                calender_dateObj.addEventListener('mouseover',()=>{
                    // console.log('mouein');
                    dataContaner.classList.remove("hidden");
                });
                calender_dateObj.addEventListener('mouseout',()=>{
                    // console.log('moueout');
                    dataContaner.classList.add("hidden");
                });

                function get_only_true(obj){
                    // console.log(obj);
                    const filtered_Data = Object.entries(obj)
                    .filter(([key, value]) => value === true)  // filter only true
                    .map(([key, value]) => key)
                    .join(", ");              // extract keys
                    return filtered_Data;
                }
        }
    }

    async #get_calender_data(){
        const response = await fetch(`/calendar_data/${this.#currentYear}/`);
        const data = await response.json();
        return data;
    }
    #getElemets(){
        let calenderContainer= document.getElementById('calenderContainer');
        if (!calenderContainer){
            calenderContainer = document.createElement('div');
            calenderContainer.id = 'calenderContainer';
            document.querySelector('main').appendChild(calenderContainer);
        }
        this.#elements['calenderContainer'] = calenderContainer;
        // this.#elements['monthYear'] = document.getElementById('monthYear');
        this.#elements['year_display'] = document.getElementById('year_display');
        this.#elements['prevBtn'] = document.getElementById('prevBtn');
        this.#elements['nextBtn'] = document.getElementById('nextBtn');
    }

    #setEvents(){
        const {prevBtn, nextBtn, year_display}=this.#elements;
        year_display.value = this.#currentYear;

        year_display.addEventListener("change", (event)=>{
            const value = event.target.value;
            if (value>2000 && value<2050){
                this.#currentYear = value;
                    this.#generateYearCalender(this.#currentYear);
            }
            // console.log(event.target.value);
            
        });

        prevBtn.addEventListener('click', ()=>{
            // const curDte = this.#currentDate.setYear(2025 - 1);
            console.log('click');
            this.#currentYear -=1;
            year_display.value = this.#currentYear;
            this.#generateYearCalender(this.#currentYear);
            
        });
        nextBtn.addEventListener('click', ()=>{
            console.log('click');
            this.#currentYear +=1;
            year_display.value = this.#currentYear;
            // const curDte = this.#currentDate.setYear(2025 + 1);
            this.#generateYearCalender(this.#currentYear);
        });
    }

    async #generateYearCalender(year){
        const {calenderContainer} = this.#elements;
        this.#days={};
        const self = this;
        
        const fregmentContaner = document.createDocumentFragment();
        const mark_data =new Date(2025, 6,2);

        for(let i=0; i<12; i++){
            fregmentContaner.appendChild(create(year, i, mark_data));
        }
        calenderContainer.innerHTML="";
        calenderContainer.appendChild(fregmentContaner);
        function create(year, month, mark_data){
            const elemtMap ={
                "calendar" :{type:'div', clsList:["calendar"]},
                "cal_header" :{type:'div', clsList:["cal_header"]},
                "monthYear" :{type:'div', clsList:["monthYear"]},
                "days" :{type:'div', clsList:["days"]},
                "dates" :{type:'div', clsList:["dates"]},
            }
            const elemts={}
            for (const [nme, value] of Object.entries(elemtMap)){
                const newElemt =  document.createElement(value.type);
                value.clsList.forEach( (cls)=>{
                    newElemt.classList.add(cls);
                });
                elemts[nme]= newElemt;
            }
            (function createStrucher(){
                const {calendar, cal_header, monthYear, days, dates} = elemts;
                    cal_header.appendChild(monthYear);

                    days.innerHTML = `<div class="day">Mon</div>
                                    <div class="day">Tue</div>
                                    <div class="day">Wed</div>
                                    <div class="day">Thu</div>
                                    <div class="day">Fri</div>
                                    <div class="day">Sat</div>
                                    <div class="day">Sun</div>`;

                    calendar.append(cal_header, days, dates);
            })()
            
            self.#generateMonthCalender(year, month, elemts);
            return elemts.calendar
        }
        await this.updateDateMarks();
    }

    #generateMonthCalender(currentYear, currentMonth, elemts){
        
        const {monthYear: monthYearElement, dates: datesElement}=elemts;
        // const currentYear = currentDate.getFullYear();
        // const currentMonth = currentDate.getMonth();
        const currentDate = new Date(currentYear,currentMonth);
        // console.log(currentDate);

        const firstDay = new Date(currentYear, currentMonth, 0);
        const lastDay = new Date(currentYear, currentMonth + 1, 0);
        const totalDays = lastDay.getDate();
        const firstDayIndex = firstDay.getDay();
        const lastDayIndex =  lastDay.getDay();

        const monthYearString = currentDate.toLocaleString('default', {month: 'long', year:'numeric'});
        monthYearElement.textContent = monthYearString;

        // let datesHTML = '';
        const datesFregment = document.createDocumentFragment();

        for (let i= firstDayIndex; i>0 ; i--){
            const preDate =  new Date(currentYear, currentMonth, 0 - i + 1);
            // datesHTML += `<div class="date inactive"> ${preDate.getDate()}</div>`;
            let date = preDate.getDate(); 
            datesFregment.appendChild( add_element(date , 'inactive') );
        }
        for (let i = 1; i<= totalDays; i++){
            const date = new Date(currentYear, currentMonth, i);
            const activeClass =  date.toDateString() === new Date().toDateString() ? 'active' : '';
            
            // let dateElement = `<div class="date ${activeClass}"> ${i}</div>`;
            // datesHTML += dateElement;
            const dateElemt = add_element(i, activeClass);
            datesFregment.appendChild( dateElemt );
            collectDateObj(this, currentYear, currentMonth, i, dateElemt);
        }
        
        for (let i =1 ; (i<= 7-lastDayIndex) && (lastDayIndex>0); i++){
            const nextDate = new Date(currentYear, currentMonth+1, i);
            // datesHTML += `<div class="date inactive">${nextDate.getDate()}</div>`;
            let date = nextDate.getDate();
            datesFregment.appendChild( add_element(date, 'inactive') );
        }
        
        // datesElement.innerHTML = datesHTML;
        datesElement.appendChild(datesFregment);

        function add_element(date, clsName){
            const newElemt = document.createElement('div');
            newElemt.classList.add('date');
            if (clsName){
                newElemt.classList.add( clsName );
            }
            newElemt.innerHTML = date;
            return newElemt;
        }
        function collectDateObj(self, currentYear, currentMonth, i, date){
            if (!self.#days[currentYear]){
                self.#days[currentYear]={};
            }
            if (!self.#days[currentYear][currentMonth]){
                self.#days[currentYear][currentMonth]={};
            }
            if (!self.#days[currentYear][currentMonth][i]){
                self.#days[currentYear][currentMonth][i]={};
            }
            self.#days[currentYear][currentMonth][i] = date;
        }
    }
}
