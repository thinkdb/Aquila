# Aquila

在 `C:\python35\Lib\site-packages\django\db\models\fields\fields.py` 中添加如下内容,用于支持无符号的整型
```
class UnsignedIntegerField(IntegerField):
    def db_type(self, connection):
        return 'integer UNSIGNED'
```

同时修改如下内容：
```
__all__ = [str(x) for x in (
    'AutoField', 'BLANK_CHOICE_DASH', 'BigAutoField', 'BigIntegerField',
    'BinaryField', 'BooleanField', 'CharField', 'CommaSeparatedIntegerField',
    'DateField', 'DateTimeField', 'DecimalField', 'DurationField',
    'EmailField', 'Empty', 'Field', 'FieldDoesNotExist', 'FilePathField',
    'FloatField', 'GenericIPAddressField', 'IPAddressField', 'IntegerField',
    'NOT_PROVIDED', 'NullBooleanField', 'PositiveIntegerField',
    'PositiveSmallIntegerField', 'SlugField', 'SmallIntegerField', 'TextField',
    'TimeField', 'URLField', 'UUIDField','UnsignedIntegerField',
)]
```
