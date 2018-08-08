$(document).ready(function(){
    $(".js_li li").click(function(){
        var order = $(".js_li li ").index(this);
        $(".con" + order).show().siblings("div").hide();
    })

})