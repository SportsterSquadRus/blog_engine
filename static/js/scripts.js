function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}


$(document).ready(function(){
  $('.likin').click(function(){
    $.ajax({
              type: "POST",
              url: $(this).attr('id'),
              data: {'content_id': $(this).attr('name'),'operation':'like_submit','csrfmiddlewaretoken': getCookie('csrftoken')},
              dataType: "json",
              success: function(response) {
              selector = document.getElementsByName(response.content_id);
                    if(response.liked==true){
                      $(selector).css("color","blue");
                      $(selector).attr('title', 'Всего лайков: ' + response.likes_count);
                    }
                    else if(response.liked==false){
                      $(selector).css("color","black");
                      $(selector).attr('title', 'Всего лайков: ' + response.likes_count);
                    }
  
  
              }
  
        });
  
  });

});


$(document).ready(function(){
  $('.complaint').click(function(){
    $.ajax({
              type: "POST",
              url: $(this).attr('id'),
              data: {'content_id': $(this).attr('name'),'operation':'complaint_submit','csrfmiddlewaretoken': getCookie('csrftoken')},
              dataType: "json",
              success: function(response) {
              selector = document.getElementsByName(response.content_id);
                    if(response.complaint==true){
                      $(selector).css("color","blue");
                    }
                    else if(response.complaint==false){
                      $(selector).css("color","black");
                    }
  
  
              }
  
        });
  
  });

});
