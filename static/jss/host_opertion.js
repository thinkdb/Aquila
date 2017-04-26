/**
 * Created by Administrator on 2017/4/26.
 */
$(function(){
    $('#host_group_append').click(function () {
        $('.shade_layer').removeClass('check_dis_flag');
    });

    $('#host_group_update').click(function () {
        $('.shade_layer').removeClass('check_dis_flag');
    });

    $('#host_group_delete').click(function () {
        $('.shade_layer').removeClass('check_dis_flag');
    });
    $('#dataTables-example').DataTable({
        responsive: true
    });
});

$('#group_add_button').click(function () {
    $.ajax({
        url: '/cmdb/hostgroup_append',
        type: 'POST',
        data: {'groupname': $('#groupname').val(), 'groupdesc': $('#groupdesc').val()},
        dataType: 'json',
        success: function (data) {
            flag = data.flag;
            msg_msg = data.msg;
            if (flag)
                location.reload();
            else
                $('#groupadd_err_msg').text(msg_msg);
        }
    })
});