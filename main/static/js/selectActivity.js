const favrateSection =  document.getElementById('favrateSection');
const allActivity =  document.getElementById('allActivity');
addExampleCard(favrateSection);
addExampleCard(allActivity);
function addExampleCard(element){
    let htmlText='';
    for (let i=1; i<=9; i++){
        htmlText+= `<div class="activity_card" data-activity-id="${i}">
            <h1>Example</h1> 
            <ul class="triger">
                <h3 >Triger/Cose</h3>
                <li>cose1</li>
                <li>cose1</li>
                <li>cose1</li>
                <li>cose1</li>
            </ul>
            
            <ul class="source">
                <h3>Source/Action</h3>
                <li>cose1</li>
                <li>cose1</li>
                <li>cose1</li>
                <li>cose1</li>
            </ul>
        </div>`;
    }
    element.innerHTML = htmlText;
}