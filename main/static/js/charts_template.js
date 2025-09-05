document.addEventListener("DOMContentLoaded", ()=>{
    new myChartDashbod();
});

class myChartDashbod{
    #canvas={};
    #charts = {}; // chart instances
    #chartsState={};
    #DurationSelector = {};
    #dateSelector ={};
    #charTypeChoice ={};

    constructor(){
        this.#getElemets();
        this.#defultChartState();
        this.#cretaeChartTypeSelector();
        this.#setEvent();
        this.#printFirstChart(); // पहला चार्ट auto select
    }
    
    #getElemets(){
        const ids = {
            TriggerCanvas: 'TriggersChart',
            SourceCanvas: 'SourceChart',
            TimeDurationCanvas: 'TimeDurationChart'
        };
        for (let key in ids) {
            this.#canvas[key] = document.getElementById(ids[key]);
        }
        // console.log(this.#canvas);
        
        const ElemtMap = {
            TriggersDurationSelector :'TriggersDurationSelector',
            SourceDurationSelector :'SourceDurationSelector',
            TimeChartDurationSelector :'TimeChartDurationSelector',
        }
        for (let key in ElemtMap) {
            this.#DurationSelector[key] = document.getElementById(ElemtMap[key]);
        }
        const charChoiceMap={
            SourceChartChoice : "SourceChartChoice",
            TriggerChartChoice : "TriggerChartChoice",
            TimeDurationChartChoice : "TimeDurationChartChoice",
        }
        for (let key in charChoiceMap){
            this.#charTypeChoice[key] = document.getElementById(charChoiceMap[key]);
        }

        const dateSelectorMap={
            "Dateset4TriggersDuration": "Dateset4TriggersDuration",
            "Dateset4SourceDuration": "Dateset4SourceDuration",
            "Dateset4TimeChartDuration": "Dateset4TimeChartDuration",
        }
        for (let key in dateSelectorMap){
            this.#dateSelector[key] = document.getElementById(dateSelectorMap[key]);
            this.#dateSelector[key].value = new Date().toISOString().split('T')[0]; //set today date
        }
        

    }
    #cretaeChartTypeSelector(){
        const { TriggerChartChoice, SourceChartChoice, TimeDurationChartChoice } = this.#charTypeChoice;

        const radioBtnList = ["bar", "line", "pie", "doughnut", "radar", "polarArea", "bubble", "scatter"];
        function buildRadioOptions(container, RadioName){
            let innerHtml = ''; 
            radioBtnList.forEach((value)=>{
            innerHtml+=`<span>
                            <label for="bubbleType">${value}</label>
                            <input type="radio" name="${RadioName}" data-value="${value}" value="${value}"> 
                        </span>`;
            });
            container.innerHTML = innerHtml;
        }
        /* Radio button ka sturcer create karna */ 
        buildRadioOptions(TriggerChartChoice, "chartTriggerType");
        buildRadioOptions(SourceChartChoice, "sourceChartType");
        buildRadioOptions(TimeDurationChartChoice, "chartTimeDurationType");

        /* Radio button ka defult state set karna */ 
        function setRadioFromState(container, chartState){
            const radio = container.querySelector(`input[value="${chartState}"]`);
            if(radio) radio.checked = true;
        }

        setRadioFromState(TriggerChartChoice, this.#chartsState.triggerChart.type);
        setRadioFromState(SourceChartChoice, this.#chartsState.sourceChart.type);
        setRadioFromState(TimeDurationChartChoice, this.#chartsState.timeDurationChart.type);
    }

    #setEvent(){
        const chartsNav = document.querySelector('.chartsNav');
        chartsNav.addEventListener('click', (event)=>{
            const target = event.target;
            const li =  target.closest('li');
            
            if (li){ this.#highlightChartAndLoad(li);}
        });


        const {TriggersDurationSelector, SourceDurationSelector, TimeChartDurationSelector}=this.#DurationSelector;
        TriggersDurationSelector.addEventListener('click', (event)=>{
            const button = event.target;
            if ( button.tagName === "BUTTON"){
                this.#chartsState.triggerChart.period.limit = button.dataset.period;
                this.#refreshTriggerChart("full");
                setClass_selectedDuration(button);
            }
            
        });
        
        SourceDurationSelector.addEventListener('click', (event)=>{
            const button = event.target;
            if ( button.tagName === "BUTTON"){
                this.#chartsState.sourceChart.period.limit = button.dataset.period;
                this.#refreshSourceChart("full");
                setClass_selectedDuration(button);
            }
            
        });
        TimeChartDurationSelector.addEventListener('click', (event)=>{
            const button = event.target;
            if ( button.tagName === "BUTTON"){
                this.#chartsState.timeDurationChart.period.limit = button.dataset.period;
                this.#refreshTimeDurationChart("full");
                setClass_selectedDuration(button);
            }
            
        });

        function setClass_selectedDuration(button){
             // Remove 'selected-duration' from all buttons
            Array.from(button.parentElement.children).forEach(btn=>{
            btn.classList.remove("selected-duration");
            });
            button.classList.add("selected-duration");
        }


        const { TriggerChartChoice, SourceChartChoice, TimeDurationChartChoice } = this.#charTypeChoice;
        TriggerChartChoice.addEventListener('change', (event)=>{
            const target = event.target;
            if (target.name === "chartTriggerType"){
                    // console.log(target.value);
                    this.#chartsState.triggerChart.type = target.value;
                    this.#refreshTriggerChart();
                    // console.log("1", target.value);
            }
        });
        SourceChartChoice.addEventListener('change', (event)=>{
            const target = event.target;
            if (target.name === 'sourceChartType'){
                this.#chartsState.sourceChart.type = target.value;
                this.#refreshSourceChart();
            }
        });
        TimeDurationChartChoice.addEventListener('change', (event)=>{
            const target = event.target;
            if(target.name === "chartTimeDurationType"){
                // console.log(target.value);
                this.#chartsState.timeDurationChart.type = target.value;
                this.#refreshTimeDurationChart();
                // console.log("3", target.value);
            }
        });

        const {Dateset4TriggersDuration, Dateset4SourceDuration, Dateset4TimeChartDuration}= this.#dateSelector;
        const {triggerChart, sourceChart, timeDurationChart} = this.#chartsState;
        /* set  vlaue to chart State Object*/
        setDate2chartsStateObj(sourceChart.period.date, Dateset4TriggersDuration);
        setDate2chartsStateObj(triggerChart.period.date, Dateset4SourceDuration);
        setDate2chartsStateObj(timeDurationChart.period.date, Dateset4TimeChartDuration);
        
        function setDate2chartsStateObj( DateObj, dateInput){
            const date = dateInput.value.split('-');
            DateObj.year = date[0];
            DateObj.month = date[1];
            DateObj.day = date[2];
        }
        console.log(this.#chartsState);
        Dateset4TriggersDuration.addEventListener('change', ()=>{
            setDate2chartsStateObj(triggerChart.period.date, Dateset4TriggersDuration);
        });
        Dateset4SourceDuration.addEventListener('change', ()=>{
            setDate2chartsStateObj(sourceChart.period.date, Dateset4SourceDuration);
        });
        Dateset4TimeChartDuration.addEventListener('change', ()=>{
            setDate2chartsStateObj(timeDurationChart.period.date, Dateset4TimeChartDuration);
        });
    }

    #printFirstChart(){
        // this function select forst li and print therre chart)
        const li = document.querySelector('.chartsNav ul li');
        if (li){
            this.#highlightChartAndLoad(li);
        }
    }

    #highlightChartAndLoad(li){
        li.parentElement.querySelectorAll('li').forEach(elemt => {
            elemt.classList.remove('selected');
        });
        li.classList.add('selected');
        // const chartId = li.dataset.activity_id;
        
        this.#defultChartState();
        this.#chartsState.chartId = li.dataset.activity_id; 
        //creating charts 
        this.#refreshTriggerChart("full");
        this.#refreshSourceChart( "full" );
        this.#refreshTimeDurationChart("full");
    }
    #defultChartState(){
        this.#chartsState = {}
        this.#chartsState ={
            chartId : "",
            sourceChart : {
                type: "line",
                period:{
                    limit: "all",
                    date : {
                        year : '',
                        month: '',
                        day: '',
                    }
                },
                ChartData: {},
            },
            triggerChart : {
                type: "bar",
                period:{
                    limit: "all",
                    date : {
                        year : '',
                        month: '',
                        day: '',
                    }
                },
                ChartData: {},
            },
            timeDurationChart : {
                type: "pie",
                period:{
                    limit: "all",
                    date : {
                        year : '',
                        month: '',
                        day: '',
                    }
                },
                ChartData: {},
            },
        }
    }
    async #fecthDataformServer(prefix, period){
        const {chartId} = this.#chartsState;
        const {limit, date} = period;

        let response;
        if (limit === 'all'){
            response = await fetch(`/${prefix}/${chartId}/`);
        }else if(limit === 'year'){
            response = await fetch(`/${prefix}/${chartId}/${date.year}/`);
        }else if (limit === 'month'){
            response = await fetch(`/${prefix}/${chartId}/${date.year}/${date.month}/`);
        }else if (limit === 'day'){
            response = await fetch(`/${prefix}/${chartId}/${date.year}/${date.month}/${date.day}`);
        }
        // console.log(response);
        return await response.json();
    }
    async #getSourceChartData(){
        const {period} =  this.#chartsState.sourceChart;
        const data = await this.#fecthDataformServer('SourceChartData', period);
         // console.log(data);
        return data;
    }
    async #getTriggerChartData(){
        const {period} =  this.#chartsState.triggerChart;
        const data = await this.#fecthDataformServer('TriggerChartData', period);
         // console.log(data);
        return data;
    }

    async #getTimeDurationChartData(){

        const {period} =  this.#chartsState.timeDurationChart;
        const data = await this.#fecthDataformServer('time_duration_chart', period);
        return data;
    }

    async #refreshTriggerChart(refreshType=""){
        if (refreshType.toLowerCase() === "full"){
           this.#chartsState.triggerChart.ChartData = await this.#getTriggerChartData();
        }
        if (!this.#chartsState.triggerChart.ChartData){
            this.#chartsState.triggerChart.ChartData = await this.#getTriggerChartData();
        }
        const ChartData = this.#chartsState.triggerChart.ChartData.trigger;
        // console.log(ChartData);
        
        // अगर पहले से chart है तो destroy करो
        if (this.#charts['TriggersChart']) {
            this.#charts['TriggersChart'].destroy();
        }
        this.#charts['TriggersChart'] = this.#createBarChart(
            this.#canvas.TriggerCanvas, 
            "Trigger's Chart",
            this.#chartsState.triggerChart.type, 
            ChartData );
    }

    async #refreshSourceChart(refreshType="" ){
        if (refreshType.toLowerCase() === "full"){
           this.#chartsState.sourceChart.ChartData = await this.#getSourceChartData();;
        }
        if (!this.#chartsState.sourceChart.ChartData){
            this.#chartsState.sourceChart.ChartData = await this.#getSourceChartData();
        }
        const ChartData = this.#chartsState.sourceChart.ChartData.source;
        console.log(ChartData);
        
        // अगर पहले से chart है तो destroy करो
        if (this.#charts['sourceChart']) {
            this.#charts['sourceChart'].destroy();
        }
        this.#charts['sourceChart'] = this.#createBarChart(
            this.#canvas.SourceCanvas, 
            "Source's Chart", 
            this.#chartsState.sourceChart.type, 
            ChartData );
    }

    async #refreshTimeDurationChart(refreshType=""){
        // this statemet consider get data form server or not
        if (refreshType.toLowerCase() === "full"){
           this.#chartsState.timeDurationChart.ChartData = await this.#getTimeDurationChartData();
        }
        if (!this.#chartsState.timeDurationChart.ChartData){
            this.#chartsState.timeDurationChart.ChartData = await this.#getTimeDurationChartData();
        }

        const ChartData = this.#chartsState.timeDurationChart.ChartData;
        
        
        // Totla minutas calculation 
        let totoalMinutInDay = 0;
        if (this.#chartsState.timeDurationChart.period.limit == 'year' ){
            totoalMinutInDay = 60*24*365;
        }else if(this.#chartsState.timeDurationChart.period.limit === 'month'){
            // इस महीने के last day का पता
            const today = new Date();
            const year = today.getFullYear();
            const month = today.getMonth(); // 0 से 11 तक (0=January)
            const lastDayOfMonth = new Date(year, month + 1, 0).getDate();
            totoalMinutInDay = 60*24*lastDayOfMonth;
        }
        else if(this.#chartsState.timeDurationChart.period.limit === 'day'|| this.#chartsState.timeDurationChart.period.limit == 'all'){
            totoalMinutInDay = 60*24;
        }
        
        ChartData['totoalMinutsInDay'] = totoalMinutInDay;
        console.log(ChartData);
        
        if (this.#charts['timeDuractionChart']) {
            // अगर पहले से chart है तो destroy करो
            this.#charts['timeDuractionChart'].destroy();
        }

        //cretating chart
        this.#charts['timeDuractionChart'] = this.#createBarChart(
            this.#canvas.TimeDurationCanvas, 
            "TimeDuration Chart", 
            this.#chartsState.timeDurationChart.type, 
            ChartData 
        )
    }

    #createBarChart(canvas, chartLabel, ChartType, ChartData  ){
        // console.log(ChartData);
        const ctx = canvas.getContext('2d');
        const chatObj = new Chart(ctx, {
            type: ChartType,
            data: {
            labels: Object.keys(ChartData),
            datasets: [{
                label: chartLabel,  
                data: Object.values(ChartData),
                backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 205, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(201, 203, 207, 0.2)'
                ],
                borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
                'rgb(153, 102, 255)',
                'rgb(201, 203, 207)'
                ],
                borderWidth: 1
            }]
            },
            options: {
            scales: {
                y: {
                beginAtZero: true
                }
            }
            }
        });
        return chatObj;
    } 
}


/*
#createChart(){
        const {chart_canvas}=this.#elemts;
        const ctx = chart_canvas.getContext('2d');
        const { default_type}=this.#chartData;
        if (this.#myChart) {
            this.#myChart.destroy();
        }

        const data = {
            type: this.#chartType,
            data: {
            labels: this.#chartData.labels,
            datasets: [{
                label: this.#chartData.chartTitle,
                data: this.#chartData.data,
                backgroundColor:[
                    'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                ],
                borderWidth: 1,
                borderColor:[
                    'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
                ],
            }]
            },
            options: {
            responsive: false,
            layout: {
                padding: {
                left: 10,
                right: 10,
                top: 10,
                bottom: 10
                }
            },
            plugins: {
                title: {
                display: true,
                text: this.#chartData.chartTitle,
                font: {
                    size: 18
                }
                },
                legend: {
                display: true,
                position: 'top'
                }
            },
            scales: (this.#chartType === 'bar' || this.#chartType === 'line' || this.#chartType === 'radar') ? {
                y: {
                beginAtZero: true
                }
            } : {}
            }
        }

        this.#myChart = new Chart(ctx, data );
    }

*/ 