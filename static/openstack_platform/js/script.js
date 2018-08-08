$(document).ready(function($) {
    $('.style').each(function () {
        $(this).click(function () {
            $(this).addClass("active");
            $(this).siblings().removeClass('active');
        })
    });
    // $('.form-control').click(function () {
    //     $(".temp").toggle();
    // });
/*aa..start*/
//nav...start
//     $('.style_li>a').click(function(){
//        $('.dropdown_list').css('display', 'none');
//         $(this).next('.dropdown_list').css('display', 'block');
//         });
    // $('.nav>li').each(function () {
    //     $(this).click(function () {
    //         $(this).addClass("active1");
    //         $(this).siblings().removeClass('active1');
    //     })
    // });
//dropdown_list...start
//     $('.menu_li>a').hover(function(){
//         $(".box_right_content").css('display', 'block');
//     });
    // $('.dropdown_list>li').each(function () {
    //     $(this).click(function () {
    //         $(this).addClass("active2");
    //         $(this).siblings().removeClass('active2');
    //     })
    // });
//收藏
 $(".introduce>li>a").hover(function(){
     $(this).next(".shoucang").css('display', 'inline');
 }, function(){
     $(this).next(".shoucang").css('display', 'none');
 })
    $(".introduce_ex>li>a").hover(function(){
        $(this).next(".shoucang").css('display', 'inline');
    }, function(){
        $(this).next(".shoucang").css('display', 'none');
    });
/*点击 close 按钮*/
    // $('.btn').click(function(){
    //     $(".center2").hide();
    //     $('.iframe').css('display','block');
    //     $('.title').css('display','block');
    //     $('.footer').css('display','block');
    //     $('.line3').css('display','block');
    // });
    $('.exam').hover(function(){
        $(this).removeClass('ex');
    },function(){
        $(this).addClass('ex');
    });
/*aa...end*/
/*my_experiment...stsrt*/
    $('.style_li_ex>a').click(function(){
        $('.box_right_content_ex').css('display', 'none');
        $(this).next('.box_right_content_ex').css('display', 'block');
    });
// $('.nav_ex>li').each(function () {
//     $(this).click(function () {
//         $(this).addClass('active3');
//         $(this).siblings().removeClass('active3');
//     })
// });
/*my_experiment...end*/
     $('.style_li').each(function () {
         $(this).click(function () {
             $(this).addClass("type_active");
             $(this).siblings().removeClass('type_active');
         })
     });
     $('.degree_cont').each(function () {
         $(this).click(function () {
             $(this).addClass("type_active");
             $(this).siblings().removeClass('type_active');
         })
     });
     $('.fa-times,.shouye,.shiyanguanli,.wodeshiyantai,.kechengguanli,.wangluoyuxinxi').click(function(){
        $('.alert').css('display','block');
        $('.backdrop').css('display','block');
     })
     $('.time').click(function(){
        $('.alert').css('display','none');
     });
     $('.hide_bar').click(function(){
         $('.bar_all').css('display','none');
         $('.show_bar').css('display','block');
     });
     $('.show_bar').click(function(){
         $('.bar_all').css('display','block');
         $('.show_bar').css('display','none');
     });

     $('.btn-danger').click(function(){
         event.preventDefault();
        $('.over_shiyan').addClass('is-visible');
     });
     $('.over_shiyan').on('click', function(event){
        if( $(event.target).is('.over_back') || $(event.target).is('.cancel') || $(event.target).is('.cut') ) {
            event.preventDefault();
            $(this).removeClass('is-visible');
        }
    });

     $('.delay_shiyan').on('click', function(event){
        if( $(event.target).is('.delay_back') || $(event.target).is('.delay_sure') || $(event.target).is('.cut') ) {
            event.preventDefault();
            $(this).removeClass('is-visible');
        }
    });
     // $('.cancel').click(function(){
     //     $('.over_shiyan').css('display','none');
     // });
     // $('.cut').click(function(){
     //     $('.over_shiyan').css('display','none');
     //     $('.delay_shiyan').css('display','none');
     // });
     // $('.over_back').click(function(){
     //     $('.over_shiyan').css('display','none');
     // });

    // $('.btn-success').click(function(){
    //     $('.delay_shiyan').css('display','block');
    // });
    $('.delay_back').click(function () {
        event.preventDefault();
        $(this).removeClass('is-visible');
    });
    $('.delay_sure').click(function () {
        event.preventDefault();
        $(this).removeClass('is-visible');
    });
            $('.guide_book').click(function () {
                $('.course_content').css('display', 'block');
                $('.virtual_machine').css('display', 'block');
                $('.vmware').css('display', 'none');
                $('.guide_book').css('display', 'none');
                $('.course').css({'overflow-y': 'unset', 'height': 'auto', 'width': '70%'});
            });
            $('.virtual_machine').click(function () {
                $('.vmware').css('display', 'block');
                $('.guide_book').css('display', 'block');
                $('.course_content').css('display', 'none');
                $('.virtual_machine').css('display', 'none');
            });
    $(window).resize(function() {
        var winwidth = $(window).width();
        if (winwidth <= 1140) {
            // $('.left_bar').css('display', 'block');
            $('.course_content').css('display', 'none');
/*            $('.guide_book').click(function () {
                $('.course_content').css('display', 'block');
                $('.virtual_machine').css('display', 'block');
                $('.vmware').css('display', 'none');
                $('.guide_book').css('display', 'none');
                $('.course').css({'overflow-y': 'unset', 'height': 'auto', 'width': '70%'});
            });
            $('.virtual_machine').click(function () {
                $('.vmware').css('display', 'block');
                $('.guide_book').css('display', 'block');
                $('.course_content').css('display', 'none');
                $('.virtual_machine').css('display', 'none');
            });*/
        }else
            if(winwidth > 1140){
            // $('.left_bar').css('display', 'none');
            $('.course_content').css('display', 'block');
            $('.vmware').css('display', 'block');
            // $('.course_cont').css({'overflow-y': 'scroll', 'height': '840.5px', 'width': '100%'});
        }
    })

    $('.play').click(function(){
        $('.bg').css('display','block');
        $('.bg-videodiv').css('display','block');
    });
    $('.close').click(function(){
        $('.bg-videodiv').css('display','none');
        $('.bg').css('display','none');
    });
    $('.btn1').click(function(){
        $('.btn1').css('display','none');
        $('.btn2').css('display','block');
    });
    $('.go-top').hover(function(){
        $('.fa-angle-up,.re-top').toggle();
    });
    $('.collect').hover(function(){
        $('.collection').css('display','block');
    });
    $('.collect').click(function(){
        $('.coll-ing,.coll-ed').toggle();
    });
})