(function($) {

    'use strict';
    $('button.glyphicon-thumbs-up, button.glyphicon-thumbs-down').click(function(){
        var $this = $(this);
        var like = $this.attr('id').search('dis') == -1;
        var id = $this.data('questionid');

        $.ajax({
            url: '/like/',
            type: 'POST',
            data: {
                'id': id,
                'like': like
            },
            dataType: 'json',
            cache: false,
            success: function (data) {
                $('#like'+id+'-bs3').html(data.likes);
                $('#dislike'+id+'-bs3').html(data.dislikes);
            },
            error: function (data) {
                // Fail message
            }
        });
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

})(jQuery);
