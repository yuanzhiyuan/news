(function(){
    var liList=$('#navigation li');
    for(var i=0;i<liList.length;i++){
        if(liList.eq(i).attr('data-topid') == topid){
            liList.eq(i).css('background-color','#00b2ec');
            $(liList.eq(i)).find('a').css('color','#ffffff');
        }
    }
    $('#navigation li').hover(function(){
        $(this).css('background-color','#00b2ec');
        $('a',this).css('color','#ffffff');
    },function(){
        if($(this).attr('data-topid')!=topid) {
            $(this).css('background-color', '#ffffff');
            $('a', this).css('color', '#403f3f');
        }
    });

})();
