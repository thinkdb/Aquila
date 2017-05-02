/**
 * Created by Administrator on 2017/5/2.
 */

$('#sql_commit').click(function () {
    $.ajax({
        url: '/dbms/inception/sql_reviews',
        type: 'POST',
        // data: {'groupname': $('#groupname').val(), 'groupdesc': $('#groupdesc').val()},
        data: {'dbhost': $('#dbhost').val(),
            'dbport': $('#dbport').val(),
            'dbname': $('#dbname').val(),
            'select_user': $('#select_user').val(),
            'sql_area': $('#sql_area').val(),
            'result_db': '1'},
        dataType: 'json',
        success: function (data) {
            flag = data.flag;
            msg_msg = data.msg;
            alert(msg_msg);
        }
    })
});
