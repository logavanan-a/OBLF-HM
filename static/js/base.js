// function validateStartDate() {
//      var starttime = document.querySelector('#event-start-date-time')
//      var endtime = document.querySelector('#event-end-date-time')
//      if(starttime < endtime){
         
//      }
//  }  
(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
  
          form.classList.add('was-validated')
        }, false)
      })
  })()


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
  var minDate = year + '-' + month + '-' + day;    
  document.getElementById("event-start-date").setAttribute('min' , minDate)

});

// $(function(){
//   var strStartTime = document.getElementById("event-start-date-time").value;
//   var strEndTime = document.getElementById("event-end-date-time").value;
//   if (strStartTime > strEndTime) {
//     return false;
//   }
// }
// function start_date_validayion(this){
//   console.log(start_date)
//   if 
// }


// var x = document.getElementById("event-start-date-time").min = minTime;
// document.getElementById("event-start-date-time").innerHTML = x;

// $('#starttime,#endtime').datetimepicker({
//   format: 'HH:mm'
// });

// var start_time = $('#event-start-date-time').val();

// var end_time = $('#event-end-date-time').val();

// if (start_time < end_time) {
//   alert('start time should be smaller');
//   return false.valueOf
// }

  // $(function(){
  //   var currentTime = new Date();
  //   var hours = currentTime.getHours();
  //   var minutes = currentTime.getMinutes(); 
  //   if(hours < 10)
  //     hours = '0' + hours.toString();
  //   if(minutes < 10)
  //     minutes = '0' + minutes.toString();
  //   var maxDate = hours + '-' + minutes;     
  //   $('#event-start-date-time').attr('min', maxDate); 
  // });
  