function toggleFullScreen() {
  if ((document.fullScreenElement && document.fullScreenElement !== null) ||    
  (!document.mozFullScreen && !document.webkitIsFullScreen)) {
      if (document.documentElement.requestFullScreen) {  
      document.documentElement.requestFullScreen();  
      } else if (document.documentElement.mozRequestFullScreen) {  
      document.documentElement.mozRequestFullScreen();  
      } else if (document.documentElement.webkitRequestFullScreen) {  
      document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);  
      }  
  } else {  
      if (document.cancelFullScreen) {  
      document.cancelFullScreen();  
      } else if (document.mozCancelFullScreen) {  
      document.mozCancelFullScreen();  
      } else if (document.webkitCancelFullScreen) {  
      document.webkitCancelFullScreen();  
      }  
  }  
}

$("#zerar_reator1").click(function(){
  var nm = "zerar_reator_1"
  $.post('http://127.0.0.1:5000/_zerar_reator1',{
  nome:nm
  }, function(data) {
  });
});

$("#zerar_reator2").click(function(){
  var nm = "zerar_reator_2"
  $.post('http://127.0.0.1:5000/_zerar_reator2',{
  nome:nm
  }, function(data) {
  });
});
