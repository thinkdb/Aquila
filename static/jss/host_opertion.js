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
    $('#host_group_append').click(function () {
        $('.shade_layer').removeClass('check_dis_flag');
    });

    $('tbody').delegate("button", "click", function () {
        // 获取主机组的id
        var group_name = $(this).parent().parent().find('#group_name').text();
        var group_jd = $(this).parent().parent().find('#group_jd').text();
        var group_id = $(this).parent().parent().find('#hostgroup_id').text();
        $('.shade_layer').removeClass('check_dis_flag');
        // 填充数据
        $('#groupname').val(group_name);
        $('#groupdesc').val(group_jd);
        $('#groupid').text(group_id);

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


$('#exit_edit').click(function () {
    $('.shade_layer').addClass('check_dis_flag');
});






