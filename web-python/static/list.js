function onReady(){
  // add handler
  $("#add").click(function() {
    window.location = "edit";
  });
  // changelog handler
  $("#changelog").click(function() {
    $.get('static/changelog.txt', function(data){
      alert(data);
    });
  });
  // todo handler
  $("#todo").click(function() {
    $.get('static/todo.txt', function(data){
      alert(data);
    });
  });
  // delete handler
  $(".delete").click(function(obj) {
    var filename = $(this).attr('filename');
    var result = confirm("确定删除文件\""+filename+"\"?");
    if (!result) return;
    $.post('delete?name='+filename, function(data){
      alert(data);
      window.location = "list";
    });
  });
  // help handler
  $("#help").click(function() {
    $.get('static/help.txt', function(data){
      alert(data);
    });
  });
}

$(document).ready(onReady);
