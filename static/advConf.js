function validate_and_submit (){
   
    var num = document.advancedForm.numProblems.value;
  
    if  ( num > 0 ) {
        document.advancedForm.submit();
    }
    else{
        alert("You need to specify atleast one reason for the meeting. Please do not waste the time of your colleagues");
    }
}

function add_input()  
{  
    var div1 = document.createElement('div');  
  
    // Get template data  
    div1.innerHTML = document.getElementById('newInputtpl').innerHTML;  
  
    // append to our form, so that template data  
    //become part of form  
    document.getElementById('newInput').appendChild(div1);  
    
    //document.getElementById('numProblems').value += 1;
    document.forms.advancedForm.numProblems.value = parseInt(document.forms.advancedForm.numProblems.value) + 1;    
}  

function add_input_mult(num)  
{  
    var div1 = document.createElement('div');  

    if (isdefined('totalSolutions')){
        totalSolutions = totalSolutions + 1;
    }
    else {
        totalSolutions = 1;
    }
   
    div1.innerHTML = document.getElementById('newInputtpl').innerHTML;  
    alert(totalSolutions);   
    document.getElementById('newInput'+num).appendChild(div1);  

    //document.forms.results.ofReason.value = num;    
}  


function isdefined( variable)
{
    return (typeof(window[variable]) == "undefined")?  false: true;
}


function add_input_reason()  
{  
    
    var div1 = document.createElement('div');  
    div1.innerHTML = document.getElementById('newInputtpl').innerHTML;  
    document.getElementById('newInput').appendChild(div1);  
    
    document.forms.generateReport.numSolutions.value += 1;
    
}  

function add_input_minutes(){
    var div1 = document.createElement('div');  
    div1.innerHTML = document.getElementById('newInputtpl').innerHTML;  
    document.getElementById('newInput').appendChild(div1);  
    
    document.forms.counterForm.minutesExists = 1;
    document.getElementById('minutesButton').style.display='none';
}

function validate_counterForm_submit(){
    alert(1);
    if (document.forms.counterForm.minutesExists == 0){
        document.forms.counterForm.meetingMinutes = 'Meeting Minutes';
        alert(2);
        document.forms.counterForm.submit();
    }
    else {
        alert(2);
        document.forms.counterForm.submit();
    }
}


function validate_generatereport_submit(){

    if (document.forms.generateReport.numSolutions.value > 0){
        document.forms.generateReport.submit();
    }
    else {
        alert('You need to have atleast one action item from this meeting.');
    }
}

    
