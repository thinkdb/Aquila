/**
 * Created by Administrator on 2017/4/26.
 */
$(function(){
    $('#host_group_append').click(function () {
        $('.shade_layer').removeClass('check_dis_flag');
        $.ajax({
            url: '/cmdb/hostgroup_manage',
            type: 'POST',
            data: {'host_edit': "{% include 'hostgroup_append.html' %}"},
            dataType: 'json'
        })

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


$('#exit_edit').click(function () {
    $('.shade_layer').addClass('check_dis_flag');
});

// 动态添加 模态对话框
