/**
 * Created by Administrator on 2017/3/14.
 * <iframe src="demo_iframe.htm" width="200" height="200"></iframe>
 */

FLAG = 0
function checkALL(){
    if(FLAG){
    }else{
        $('#tb input[type="checkbox"]').prop('checked', true);
    }
}
function cancleALL(){
    if(FLAG){
        Save();
    }else{
        $('#tb input[type="checkbox"]').prop('checked', false);
    }
}
function reverseALL(){
    if(FLAG){
    }else{
        $('#tb input[type="checkbox"]').each(function(){
            if($(this).prop('checked')){
                $(this).prop('checked', false);
            }else{
                $(this).prop('checked', true);
            };
        });
    }
}
function Save(){
    $('#tb input[type="checkbox"]').each(function(){
        if($(this).prop('checked')){
            var edit_lab = $(this).parent().parent();
            // 获取父节点的父节点
            var edit_content = edit_lab.find('input');
            // 获取要编辑的标签
            edit_content.each(function(){
                var self = $(this);
                if($(this).prop('checked')){
                }else{
                    for(i=0;i<self.length;i++){
                    var self_span = $(this)[i]
                    var edit_value = self_span.value;
                    // 标签内的文本
                    var self_span_new = '<span>' + edit_value + '</span>'
                    $(self_span).replaceWith(self_span_new);
                    }

                }

            });
        };
    });
    FLAG = 0;
    cancleALL();
}
function Edit(){
    $('#tb input[type="checkbox"]').each(function(){
        if($(this).prop('checked')){
            var edit_lab = $(this).parent().parent();
            // 获取父节点的父节点
            var edit_content = edit_lab.find('span');
            // 获取要编辑的标签
            edit_content.each(function(){
                var self = $(this);
                for(i=0;i<self.length;i++){
                    var self_span = $(this)[i];
                    var edit_value = self_span.innerText;
                    // 标签内的文本
                    var self_span_new = '<input value=' + edit_value + ' />';
                    $(self_span).replaceWith(self_span_new);
                }
            });
        }
    });
    FLAG = 1;
}
function Del_tr(self){
   $(self).parent().parent().remove();
}
function Del_all_chose(){
    $('#tb input[type="checkbox"]').each(function(){
        if($(this).prop('checked')){
            Del_tr(this);
        }
    });
}
function show_hide(self){
    // debugger;
    // jquery 中的this等同于 python 中的  self， 所以这边用self表示
    $(self).next().removeClass('head');
    $(self).addClass('Highlight');
    $(self).parent().siblings().find('.title_body').addClass('head');
}