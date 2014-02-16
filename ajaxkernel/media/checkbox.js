function setRemoveMethod(){
    Array.prototype.remove = function(value){
      this.splice( $.inArray(value, this), 1 );
    };
}
function bindCheckBox(){
    $("[name='choices']").bind('change', function(){
        if (this.checked) regList.push(this.value);
        else regList.remove(this.value);
        var orderObj = $('#order')[0];
        $(orderObj).html('');
        $(regList).each(function(index){
            $(orderObj).append( index + 1 + ". " +this + "<br>");
        });
    });
}
function onLoadCallBack(){
    setRemoveMethod();
    regList = [];
    bindCheckBox();
}
$(onLoadCallBack);
