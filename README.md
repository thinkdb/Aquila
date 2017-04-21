# Aquila

1. 在 `C:\python35\Lib\site-packages\django\db\models\fields\fields.py` 中添加如下内容,用于支持无符号的整型
```
class TinyIntegerField(SmallIntegerField, Field):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint"
        else:
            return super(TinyIntegerField, self).db_type(connection)

class PositiveTinyIntegerField(PositiveSmallIntegerField, Field):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint UNSIGNED"
        else:
            return super(PositiveTinyIntegerField, self).db_type(connection)


class UnTinyIntAuto(PositiveTinyIntegerField):
    def db_type(self, connection):
        return "tinyint UNSIGNED AUTO_INCREMENT"


class UnsignedIntegerField(IntegerField):
    def db_type(self, connection):
        return "integer UNSIGNED"
```
同时替换如下内容：
```
__all__ = [str(x) for x in (
    'AutoField', 'BLANK_CHOICE_DASH', 'BigAutoField', 'BigIntegerField',
    'BinaryField', 'BooleanField', 'CharField', 'CommaSeparatedIntegerField',
    'DateField', 'DateTimeField', 'DecimalField', 'DurationField',
    'EmailField', 'Empty', 'Field', 'FieldDoesNotExist', 'FilePathField',
    'FloatField', 'GenericIPAddressField', 'IPAddressField', 'IntegerField',
    'NOT_PROVIDED', 'NullBooleanField', 'PositiveIntegerField',
    'PositiveSmallIntegerField', 'SlugField', 'SmallIntegerField', 'TextField',
    'TimeField', 'URLField', 'UUIDField','UnsignedIntegerField','TinyIntegerField',
    'PositiveTinyIntegerField','UnsignedIntegerField','UnTinyIntAuto',
)]
```
2. 修改数据连接信息， 修改Aquila下的settions.py 文件内容
根据你的实际地址修改
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aquila',
        'USER': 'think',
        'PASSWORD': '123456',
        'HOST': '192.168.1.6',
    }
}
```
