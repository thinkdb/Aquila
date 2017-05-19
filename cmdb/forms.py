from django import forms
from django.forms import widgets
from django.forms import fields

from cmdb import models as cmdb_models


class HostAppend(forms.Form):
    host_ip = fields.GenericIPAddressField(error_messages={'required': '主机地址不能为空', 'invalid': 'IP地址不合法'},
                                           protocol='ipv4',
                                           label='主机地址',
                                           widget=widgets.TextInput(attrs={'class': 'form-control'}),)

    host_user = fields.CharField(label='主机用户',
                                 widget=widgets.TextInput(attrs={'class': 'form-control'}))
    host_pass = fields.CharField(label='主机密码',
                                 widget=widgets.TextInput(attrs={'class': 'form-control'}))
    host_port = fields.CharField(label='主机端口',
                                 initial=22,
                                 widget=widgets.TextInput(attrs={'class': 'form-control'}))

    app_type = fields.CharField(
        initial=1,
        widget=widgets.Select(choices=((1, 'MySQL'), (2, 'JAVA')), ),
        label='应用类型'
    )
    host_group = fields.CharField(
        initial=0,
        widget=widgets.Select(choices=[]),
        label='主机组',

    )
    app_user = fields.CharField(required=False,
                                label='应用用户',
                                widget=widgets.TextInput(attrs={'class': 'form-control'}))
    app_pass = fields.CharField(required=False,
                                label='应用密码',
                                widget=widgets.TextInput(attrs={'class': 'form-control'}))
    app_port = fields.CharField(required=False,
                                label='应用端口',
                                widget=widgets.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(HostAppend, self).__init__(*args, **kwargs)
        self.fields['host_group'].widget.choices = cmdb_models.HostGroup.objects.values_list('id', 'host_group_jd')
