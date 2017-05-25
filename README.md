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

#### 2. 修改数据库连接信息，修改Aquila下的settions.py 文件内容
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
#### 3. 修改 Inception 信息
修改Aquila下的settions.py 文件内容, 根据你的实际地址修改
```
INCEPTION = {
    'default': {
        'INCEPTION_HOST': '192.168.1.6',
        'INCEPTION_PORT': 6669,
    },
    'backup': {
        'BACKUP_USER': 'root',
        'BACKUP_PASSWORD': '123456',
        'BACKUP_PORT': 3306,
        'BACKUP_HOST': '192.168.1.6',
    },
}
```

#### 4. 修改用户密码加密 KEY, 根据自己爱好设置
修改Aquila下的settions.py 文件内容
```
USER_ENCRYPT_KEY = '3df6a1341e8b'
```


#### 5. 使用 inception 功能时，需要修改pymysql工具的源码， 修改如下：
C:\Python35\Lib\site-packages\pymysql\connections.py 在1071 行前面添加如下内容，
只要把第一个点前面改成 大于等于5就行,
```
self.server_version = '5.7.18-log'
```

#### 6. 通过 inception 工具执行语句时获取具体sql的语法错误内容
修改C:\python35\Lib\site-packages\pymysql\cursors.py 334行内容
```
        if self._result:
        #if self._result and (self._result.has_next or not self._result.warning_count):
```

#### 7. 自行安装 Inception

http://bac10bd3.wiz03.com/share/s/2WMgLj32GQP92KUCZP2YLIKi0BXq6M3N6QBP2ChQ7O0CHqdo


#### 8. 自行安装 pymysql


## 使用 Aquila 审核平台
#### 1. 运行环境准备
python 3+, django 10+
django 安装文档：http://bac10bd3.wiz03.com/share/s/2WMgLj32GQP92KUCZP2YLIKi2otYZ005t4wx20WMeg2WU1fs

#### 2. 创建数据库
在配置的 数据库 里面创建 aquila 数据库， 库名根据你的配置来

#### 3. 创建库表
进入到项目目录执行：
1. python3 manage.py makemigrations
2. python3 manage.py migrate

#### 4. 初始化数据
运行 scripts/init_data.py 文件， 默认的管理员账号和密码为: admin/123456

#### 5. 启动 Aquila
python3 manage.py runserver 0.0.0.0:80

#### 5. 登录
http:ip/login

ip 为启动 Aquila 审核平台的主机地址

初始化时只给了管理账号， 其他用户账号自行注册


## 注意事项：
#### 1. 工单执行时，当前页面不能离开，等到 “已经执行结束, 请移步到《工单查询》中查看执行结果!!!!!!” 出现后，才能刷新页面，不然执行结果不会记录到数据库中，在工单查询页面看到这个工单一直是执行状态， 所以这点得注意下

#### 2. 工单的回滚 和 工单执行进度 目前还没有，后面添加
