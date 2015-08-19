function start_timer(){
  var myVar=setInterval(function(){myTimer()},1000);

  var myTime  = new Date();
  var foo = true;
  function myTimer() {
    var d = new Date();
    if (foo){
    	myTime.setSeconds(d.getSeconds() + 10);
	foo = false;
    }
    var h = Math.floor(((myTime - d)/1000) / 3600);
    var m = Math.floor(((myTime - d)/(1000 * 60)) % 60);
    var s = Math.floor(((myTime - d)/1000) % 60);

    $("#clock").text(h+':'+m+':'+s);

    if (h <= 0 && m <= 0 && s <= 0){
      clearInterval(myVar);
      $('#clock').text('00:00:00');
      $('#phone-container h1').removeClass('mdi-communication-call');
      $('#phone-container h1').addClass('mdi-notification-phone-in-talk');
      $.get('/make_call',function(data){
	//$( "#status" )
	   //.append(item)
	});
    }

  }
}

$(document).ready(function(){
  // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
  $('.modal-trigger').leanModal({
    dismissible: false, // Modal can be dismissed by clicking outside of the modal
    opacity: .5, // Opacity of modal background
    in_duration: 300, // Transition in duration
    complete: function() { start_timer(); } // Callback for Modal close
  });
});

function cancel_page() {
    $('#modal1').closeModal();
}

