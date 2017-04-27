# Aquila

### 准备工作
#### 1. 在 `C:\python35\Lib\site-packages\django\db\models\fields\fields.py` 中添加如下内容,用于支持无符号的整型
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
        return "int UNSIGNED"

class UnsignedSmallIntegerField(SmallIntegerField):
    def db_type(self, connection):
        return "smallint UNSIGNED"
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
    'PositiveTinyIntegerField','UnsignedIntegerField','UnTinyIntAuto','UnsignedSmallIntegerField',
)]
```

#### 2. 修改数据连接信息， 修改Aquila下的settions.py 文件内容
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
#### 3. 初始化数据
运行 scripts/init_data.py 文件， 默认的管理员账号和密码为: admin/123456


#### 4. 使用 inception 功能时，需要修改pymysql工具的源码， 修改如下：
C:\Python35\Lib\site-packages\pymysql\connections.py 在1071 行前面添加如下内容，
只要把第一个点前面改成 大于等于5就行,
```
self.server_version = '5.7.18-log'
```

#### 5. 通过 inception 工具执行语句时获取具体sql的语法错误内容
修改C:\python35\Lib\site-packages\pymysql\cursors.py 334行内容
```
        if self._result:
        #if self._result and (self._result.has_next or not self._result.warning_count):
```