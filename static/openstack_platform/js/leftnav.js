$(function() {
    $('.link').next().slideToggle();
    $('.link').parent().toggleClass('open');
    var Accordion = function(el, multiple) {
        this.el = el || {};
        this.multiple = multiple || false;

        // Variables privadas
        var links = this.el.find('.link');
        // Evento
        links.on('click', {el: this.el, multiple: this.multiple}, this.dropdown)
    };

    Accordion.prototype.dropdown = function(e) {
        var $el = e.data.el;
        $this = $(this);
        $next = $this.next();

        $next.slideToggle();
        $this.parent().toggleClass('open');
    };

    var accordion = new Accordion($('#accordion'), false);
    $('.submenu li').click(function () {
        $('.submenu li').removeClass('current');
        $(this).addClass('current');
    });
});