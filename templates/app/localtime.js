function upd_localtime() {
    setTimeout(upd_localtime, 60e3/20);
    $('#localtime')
                .css('background','#F004');
    $.get('/ajax/app/localtime')
        .done(function(data) {
            $('#localtime')
                .text(data)
                .css('background','#0F82')
            });
}
$(upd_localtime);
