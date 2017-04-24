/**
 * Created by Administrator on 2017/3/11.
 */
function close_error(argsss){
    $('.'+argsss).removeClass('check_dis_flag');
}
function add_error(argsss){
	$('.'+argsss).addClass('check_dis_flag');
}

function auth_account(argsss){
    var username = $('#user').val();
    var passwd = $('#passwd').val();
	if(username.length && passwd.length){
		add_error();
		
	}else{
		close_error(argsss);
	}
}

function check_focus(){
	var user_flag = check_user();
	var email_flag = check_email();
	var f_passwd_flag = check_pass();
	if(user_flag && email_flag && f_passwd_flag){
		check_disabled();
	}
}

function check_useremail(){
    // 检测邮箱
    var email = $("#check_email").val();
    if(email){
		var mailreg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/
		var error_status = mailreg.test(email);
		if(error_status){
			// 邮箱格式正确
			// alert('邮箱格式正确');
			add_error('prompt_email');
			return 1;
		}else{
			// 显示错误信息
			close_error('prompt_email');
		}
		close_error('prompt_email');
	}else{
		close_error('prompt_email');
	}
}

function check_username(){
	// 检测用户是否合法
    var username = $("#check_user").val();
    var namereg = /^[a-zA-Z]*([a-zA-Z0-9]|[_]){6,19}$/;
    var a = namereg.test(username);
    if(a){
    	add_error('prompt_user');
    	return 1;
	}else{
		close_error('prompt_user');
	}
}

function check_userpass(){
	// 检测密码合法性
	// 长度为 8 到 16 个字符
	var username = $("#check_user").val();
	var passwd = $("#check_user_pass").val();
	if(passwd){
		var pass_len=/^(\w){8,16}$/;
		var pass_number = /^[\d]*$/;
		var pass_char = /^[A-Za-z]*$/;
		var pass_len_flag = pass_len.test(passwd); // 判断长度 t
		var pass_no_num_flag = pass_number.test(passwd); //不能全为数字 f
		var pass_no_char_flag = pass_char.test(passwd); // 不能全为字母 f
		if(username == passwd){
			close_error('prompt_pass');
		}else if(pass_len_flag){
			if(pass_no_num_flag==false && pass_no_char_flag==false){
				add_error('prompt_pass');
				var email_status = check_useremail();
				if (email_status){
					$('#check_register_val').removeClass('disabled');
					$('#check_register_val').removeAttr('onclick');
				}
			}else{
				close_error('prompt_pass');
			}
		}
		else{
			close_error('prompt_pass');
		}
	}else{
		close_error('prompt_pass');
	}

}

function check_repass(){
	// 校验两次密码是否一致
	var passwd = $("#password").val();
    var repasswd = $("#repass").val();
	var first_pass_flag = check_pass();
	if(first_pass_flag){
		if(passwd == repasswd){
			add_error('prompt_repass');
		    check_focus();
        }else{
            close_error('prompt_repass');
        }
	}else{
		close_error('prompt_repass');
	}
}

function check_disabled(){
	$("#check_button").removeClass('sign_button_disabled');
}

function check_commit(){
	alert("succ");
}

function dis_submit(){
	return false;
}
