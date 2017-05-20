/**
 * Created by Administrator on 2017/4/26.
 */
/* 转换数字为ip地址 */
$(function () {
    $('td[id="num_to_ip"]').each(function () {
        var num_ip = $(this).text();
        if(num_ip < 0 || num_ip > 0xFFFFFFFF){
            throw ("The number is not normal!");
        }
        var new_ip = (num_ip>>>24) + "." + (num_ip>>16 & 0xFF) + "." + (num_ip>>8 & 0xFF) + "." + (num_ip & 0xFF);
        $(this).text(new_ip);
    });

});

$(function(){
    $.ajaxSetup({
            beforeSend:function (xhr, settings) {
                xhr.setRequestHeader('X-CSRFtoken', $.cookie('csrftoken'));
            }
        });

    $('#host_group_append').click(function () {
        $('.shade_layer').removeClass('check_dis_flag');
    });

    $('tbody').delegate("button", "click", function () {
        // 获取主机组的id
        var group_name = $(this).parent().parent().find('#group_name').text();
        var group_jd = $(this).parent().parent().find('#group_jd').text();
        var group_id = $(this).parent().parent().find('#hostgroup_id').text();

        // 获取主机的信息
        var host_id = $(this).parent().parent().find('#host_id').text();
        var num_to_ip = $(this).parent().parent().find('#num_to_ip').text();
        var app_type = $(this).parent().parent().find('#app_type').text();
        var host_group_id = $(this).parent().parent().find('#host_group_id').text();
        var host_user = $(this).parent().parent().find('#host_user').text();
        var host_pass = $(this).parent().parent().find('#host_pass').text();
        var host_port = $(this).parent().parent().find('#host_port').text();

        $('.shade_layer').removeClass('check_dis_flag');
        // 填充数据
        $('#groupname').val(group_name);
        $('#groupdesc').val(group_jd);
        $('#groupid').text(group_id);

        $('#id_host_id').val(host_id);
        $('#id_host_ip').val(num_to_ip);
        $('#id_app_type').val(app_type);
        $('#id_host_group').val(host_group_id);
        $('#id_host_user').val(host_user);
        $('#id_host_pass').val(host_pass);
        $('#id_host_port').val(host_port);



        // alert(a);
    });

    $('#host_group_delete').click(function () {
        // $('.shade_layer').removeClass('check_dis_flag');
    });
    $('#dataTables-example').DataTable({
        responsive: true
    });
});

$('#group_add_button').click(function () {
    $.ajax({
        url: '/backend/hostgroup_append.html',
        type: 'POST',
        data: {'groupname': $('#groupname').val(), 'groupdesc': $('#groupdesc').val(), 'groupid':$('#groupid').text()},
        dataType: 'json',
        headers: {'X-CSRFtoken': $.cookie('csrftoken')},
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

$('#host_update').click(function () {
    $.ajax({
        url: '/backend/host_append.html',
        type: 'POST',
        data: $('#form').serialize(),
        dataType: 'json',
        headers: {'X-CSRFtoken': $.cookie('csrftoken')},
        success: function (data) {
            flag = data.flag;
            msg_msg = data.msg;
            if (flag)
                location.reload();
            else
                $('#err_msg').text(msg_msg);
        }
    })
});

$('#exit_edit').click(function () {
    $('.shade_layer').addClass('check_dis_flag');
});


$('#host_append').click(function(){
    $.ajax({
        url: 'backend/host_manage.html',
        type: 'POST',
        data: $('#form').serialize(),
        dataType: 'json',
        headers: {'X-CSRFtoken': $.cookie('csrftoken')},
        success: function (data) {
            flag = data.flag;
            msg_msg = data.data;
            if (flag)
                location.reload();
            else
                $.each(msg_msg, function(key, value){
                    $('#err_msg').text(value);
                });

        }
    })
});



