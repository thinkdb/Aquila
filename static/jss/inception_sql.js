/**
 * Created by Administrator on 2017/5/2.
 */

$('#sql_commit').click(function () {

    $.ajax({
        url: '/dbms/inception/sql_reviews',
        type: 'POST',
        data: $('#form').serialize(),
        dataType: 'json',
        success: function (data) {
            console.log(data);
            flag = data.flag;
            msg_msg = data.msg;
            alert(msg_msg);
        },
        error:function (data) {
            console.log(data);
        }
    })
});
