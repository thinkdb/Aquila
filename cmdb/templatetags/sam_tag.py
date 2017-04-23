#!/bin/env python3
# _*_ coding:utf8 _*_

from django import template
register = template.Library()

@register.simple_tag
def help(arg1, arg2):
    return arg1 + arg2


@register.filter
def help_filter(arg1, arg2):
    return arg1 + arg2