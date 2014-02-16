function onReady(){
  code_modified = false;
  // key press
  $("#code").keypress(function(){
    code_modified = true;
    var obj = $('#header');
    var hstr = obj.html();
    if (hstr[hstr.length-1]!='*') obj.html(obj.html()+'*');
  });
  // new handler
  $("#new").click(function() {
    window.location = "edit";
  });
  // open handler
  $("#open").click(function() {
    window.location = "list";
  });
  // save handler
  $("#save").click(function() {
    var name = $('#name').val();
    var default_name = $("#defaultname").val();
    if (!name) name = prompt('请输入要保存的文件名', default_name);
    if (!name) return;
    $.post('save', {code: $('#code').val(), name: name}, function(data){
      $('#name').val(name);
      $('#header').html(name);
      code_modified = false;
      alert(data);
    });
  });
  // save as handler
  $("#saveas").click(function() {
    var name = prompt('请输入要另存的文件名', $('#name').val());
    if (!name) return;
    $.post('save', {code: $('#code').val(), name: name}, function(data){
      alert(data);
      window.location = "edit?name="+name;
    });
  });
  // run handler
  $("#run").click(function() {
    $.post('run', {code: $('#code').val()}, function(data){
      alert(data);
    });
  });
  // delete handler
  $("#delete").click(function() {
    var result = confirm("确定删除此文件?");
    if (!result) return;
    $.post('delete', {name: $('#name').val()}, function(data){
      alert(data);
      window.location = "list";
    });
  });
}

$(document).ready(onReady);
$(window).bind("beforeunload", function(){
  if (code_modified) return "文件尚未保存";
});
