$(function(){

  var dtToday = new Date();
  var day = dtToday.getDate();
  var month = dtToday.getMonth() + 1;

  if(month < 10){
    month = '0' + month.toString();
  }
  if(day < 10){
    day = '0' + day.toString();
  }

  var year = dtToday.getFullYear();
  var maxDate = year + '-' + month + '-' + day;  
  if (document.getElementById("previous_data") != null)  {
    document.getElementById("previous_data").setAttribute('max' , maxDate) 
  }

});

