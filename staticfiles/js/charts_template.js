document.addEventListener("DOMContentLoaded", ()=>{
    new myChartDashbod(allChartData);
});


class myChartDashbod{
    #elemts={};

    constructor(allChatData){
        // this.#getElements();
        // this.#setEvents();
        this.#createCharts(allChatData);
    }
    #getElements(){
        
    }
    #createCharts(allChartData){
        const main =document.querySelector('main');
        const fragment = document.createDocumentFragment();
        for (const [key, chatData] of Object.entries(allChartData)){
            console.log(chatData);
            const ChatObj=  new create_Chart(chatData)
            fragment.append(ChatObj.getChart());
        }
        main.appendChild(fragment);
    }
    #setEvents(){

    }
}
class create_Chart{
    static count=0;
    #elemts={};
    #chartData={};
    #myChart= null;
    #chartType;
    constructor(chartdata){
        create_Chart.count++;
        this.#getElements();
        this.#chartData =  chartdata;
        this.#chartType= this.#chartData.default_type ;
        
        this.#setEvents();
        this.#createChart();
        
    }
    getChart(){
        return this.#elemts.container;
    }
    #getElements(){
        
        const elemtsMap={
            'container': {type: 'div', id:'', classList:['container']},
            'chart_canvas': {type: 'canvas', id:'', classList:[]},
            'chartArea':{type: 'div', id:'', classList:['chartArea'], name: ''},
            'buttonArea':{type: 'div', id:'chartChoice', classList:['buttonArea']},
        }
        Object.freeze(elemtsMap);
        for (const [key, value] of Object.entries(elemtsMap)){
            const newElemnt = document.createElement(value.type);
            if (value.id){
                newElemnt.id=  value.id;
            }
            value.classList.forEach(cls=>{
                newElemnt.classList.add(cls);
            })
            this.#elemts[key] =  newElemnt;
        }
        setStrucher(this.#elemts);

        function setStrucher(elemts){
            const {container, chartArea,chart_canvas, buttonArea}=elemts;
            // canvas id="myChart2" height="500" width="500"
            chart_canvas.width = 500;
            chart_canvas.height = 500;
            
            chartArea.appendChild(chart_canvas);
            const count =create_Chart.count;
            buttonArea.innerHTML = `<span>
                                        <label for="barType">Bars</label>
                                        <input type="radio" name="chartType${count}" id="barType" value="bar">
                                    </span>
                                    <span>
                                        <label for="lineType">Lines</label>
                                        <input type="radio" name="chartType${count}" id="lineType" value="line">
                                    </span>
                                    <span>
                                        <label for="pieType">pie</label>
                                        <input type="radio" name="chartType${count}" id="pieType" value="pie"> 
                                    </span>
                                    <span>
                                        <label for="doughuntType">doughunt</label>
                                        <input type="radio" name="chartType${count}" id="doughuntType" value="doughnut"> 
                                    </span>
                                    <span>
                                        <label for="radarType">radar</label>
                                        <input type="radio" name="chartType${count}" id="radarType" value="radar"> 
                                    </span>
                                    <span>
                                        <label for="polarAreaType">polarArea</label>
                                        <input type="radio" name="chartType${count}" id="polarAreaType" value="polarArea"> 
                                    </span>
                                    <span>
                                        <label for="bubbleType">bubble</label>
                                        <input type="radio" name="chartType${count}" id="bubbleType" value="bubble"> 
                                    </span>
                                    <span>
                                        <label for="scatterType">scatter</label>
                                        <input type="radio" name="chartType${count}" id="scatterType" value="scatter"> 
                                    </span>`;
            container.append(chartArea, buttonArea);
        }
    }
    #setEvents(){
        const {buttonArea}=this.#elemts;
        const self = this;
        (function defaultRadioBtnSet(){
            // const selectedRadio = document.querySelector('input[name="chartType"]:checked');
            // let chartType = selectedRadio ? selectedRadio.value : 'bar';
            const radioToSelect = buttonArea.querySelector(`input[name="chartType${create_Chart.count}"][value="${self.#chartType}"]`);
            if (radioToSelect) {
                radioToSelect.checked = true;
            }
        })();

        buttonArea.addEventListener('change', (event)=>{
            const value= event.target.value;
            // console.log(this.#chartType, chartData);
            this.#chartType = value;
            this.#createChart();
        });
    }

    #createChart(){
        const {chart_canvas}=this.#elemts;
        const ctx = chart_canvas.getContext('2d');
        const {data: chartData, labels:chartLabels, default_type, chartTitle}=this.#chartData;
        if (this.#myChart) {
            this.#myChart.destroy();
        }

        this.#myChart = new Chart(ctx, {
            type: this.#chartType,
            data: {
            labels: chartLabels,
            datasets: [{
                label: "chartTitle",
                data: chartData,
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
        });
    }
}