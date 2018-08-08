jQuery(document).ready(function($){
    //open popup
    $('#test_jiaojuan').on('click', function(event){
        event.preventDefault();
        $('.cd-popup').addClass('is-visible');
    });
    $('#returnindex').on('click', function(event){
        event.preventDefault();
        $('.index').addClass('is-visible');
    });
        $('#returnmyexam').on('click', function(event){
        event.preventDefault();
        $('.exam').addClass('is-visible');
    });
    //close popup
    $('.cd-popup').on('click', function(event){
        if( $(event.target).is('.cd-popup-close') || $(event.target).is('.cd-popup') ) {
            event.preventDefault();
            $(this).removeClass('is-visible');
        }
    });
        $('.cd-popup').on('click', function(event){
        if( $(event.target).is('.close') || $(event.target).is('.cd-popup') ) {
            event.preventDefault();
            $(this).removeClass('is-visible');
        }
    });
    //close popup when clicking the esc keyboard button
    $(document).keyup(function(event){
        if(event.which=='27'){
            $('.cd-popup').removeClass('is-visible');
        }
    });
    $('.exam-end-sure').click(function(){
        event.preventDefault();
        $(this).removeClass('is-visible');
    });
});