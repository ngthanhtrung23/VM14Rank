"use strict";
$(document).ready(function () {
    load_data();

    var current_tab = "total";

    $(".toggle").click(function (event) {
        var node = $(event.target);
        var new_id = node.attr("show"), old_tab = current_tab;
        if (new_id === current_tab) {
            return ;
        }
        current_tab = new_id;
        $("#" + old_tab + "-toggle").parent().toggleClass("active");
        $("#" + old_tab).hide(function () {
            $("#" + new_id).show();
            $('#' + new_id + "-toggle").parent().toggleClass("active");
        });
    })
    if ( ($(window).height() + 100) < $(document).height() ) {
        $('#top-link-block').removeClass('hidden').affix({
            // how far to scroll down before link "slides" into view
            offset: {top:100}
        });
    }
});

var cmp_total = function (x, y) {
    return y[1]['total'] - x[1]['total'];
}

function load_data() {
    var round, i, html, cur_users, j;
    for(round in rounds)
        if (rounds.hasOwnProperty(round)) {

            html = '<tr><th>#</th><th>Thành viên</th>';
            for(i = 0; i < rounds[round].length; ++i) {
                if (round === 'total') {
                    html += '<th>' + rounds[round][i] + '</th>'
                } else {
                    html += '<th><a href="http://vn.spoj.com/VM14/problems/' + rounds[round][i] + '">' + rounds[round][i] + '</a></th>'
                }
            }
            html += '<th>Tổng điểm</th></tr>'

            cur_users = users[round];
            cur_users.sort(cmp_total);

            for(j = 0; j < cur_users.length; ++j) {
                html += '<tr>'
                        + '<td>' + (j+1) + '</td>'
                        + '<td><a href="http://vn.spoj.com/VM14/users/' + cur_users[j][0] + '">' + cur_users[j][0] + '</a></td>';

                for(i = 0; i < rounds[round].length; ++i) {
                    var tmp = cur_users[j][1][rounds[round][i]];
                    html += '<td>' + ((tmp) ? parseFloat(tmp).toFixed(2) : '-') + '</td>';
                }
                html += '<td>' + parseFloat(cur_users[j][1]['total']).toFixed(2) + '</td></tr>';
            }

            $("#" + round + "-table").append(html);
        }
}
