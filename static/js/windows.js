$(function () {
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

    $("select#memberreport").change(function () {
        var dev_id = $(this).val();
        if (dev_id !== "") {
            $.ajax({
                url: '/report/',
                type: 'POST',
                data: {
                    'dev_id': dev_id
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    $table = $("table.dataTable > tbody");
                    var html = '';
                    for (var i in data.message) {
                        html += '<tr>';
                        html += '<td>' + data.message[i].date + '</td>';
                        html += '<td>' + data.message[i].general.replace(/\r?\n/g, '<br />') + '</td>';
                        html += '<td>' + data.message[i].achievement.replace(/\r?\n/g, '<br />') + '</td>';
                        html += '<td>' + data.message[i].planning.replace(/\r?\n/g, '<br />') + '</td>';
                        html += '<td>' + data.message[i].trouble.replace(/\r?\n/g, '<br />') + '</td>';
                        html += '</tr>';
                    }
                    $table.html(html);
                },
                error: function (data) {

                }
            });
        }
        else {
            $("table.dataTable > tbody tr").remove();
        }
    });

    $("select#teamreport").change(function () {
        var team_id = $(this).val();
        if (team_id !== "") {
            $.ajax({
                url: '/report/',
                type: 'POST',
                data: {
                    'team_id': team_id
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    $table = $("table.dataTable > tbody");
                    var html = '';
                    for (var i in data.message) {
                        html += '<tr>';
                        html += '<td>' + data.message[i].dev + '</td>';
                        html += '<td>' + data.message[i].general.replace(/\r?\n/g, '<br />') + '</td>';
                        html += '<td>' + data.message[i].achievement.replace(/\r?\n/g, '<br />') + '</td>';
                        html += '<td>' + data.message[i].planning.replace(/\r?\n/g, '<br />') + '</td>';
                        html += '<td>' + data.message[i].trouble.replace(/\r?\n/g, '<br />') + '</td>';
                        html += '</tr>';
                    }
                    $table.html(html);
                },
                error: function (data) {

                }
            });
        }
        else {
            $("table.dataTable > tbody tr").remove();
        }
    });

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});
