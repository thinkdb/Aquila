from django.db import models

# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=40)
    emails = models.CharField(max_length=100)


class MysqlBackupSourceInfo(models.Model):
    id = models.AutoField(primary_key=True)
    generator_room_name = models.CharField(max_length=30)
    ipaddr = models.IntegerField()
    port = models.SmallIntegerField()
    service_level = models.SmallIntegerField()
    defaults_file = models.CharField(max_length=100)
    back_time = models.TimeField()
    transport_time = models.TimeField(default='1970-01-01 01:01:01')
    is_transport = models.SmallIntegerField(default=0)
    back_pool_id = models.ForeignKey('BackupPoolInfo', on_delete=models.CASCADE)
    r_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dbms_mysql_backup_source_info'
        unique_together = ('generator_room_name', 'ipaddr', 'port')


class BackupPoolInfo(models.Model):
    id = models.AutoField(primary_key=True)
    pool_name = models.CharField(max_length=50)
    ipaddr = models.IntegerField()
    port = models.SmallIntegerField()
    passwd = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

    class Meta:
        db_table = 'dbms_mysql_backup_pool_source_info'


class BackupedBinlogInfo(models.Model):
    id = models.AutoField(primary_key=True)
    machine_id = models.ForeignKey('MysqlBackupSourceInfo', on_delete=models.CASCADE)
    binlog_name = models.CharField(max_length=50)
    binlog_create_time = models.DateTimeField()
    binlog_size = models.SmallIntegerField()
    r_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dbms_mysql_backuped_binlog_info'
        index_together = ('machine_id', 'r_time')


class BackupedInfo(models.Model):
    id = models.AutoField(primary_key=True)
    machine_id = models.ForeignKey('MysqlBackupSourceInfo', on_delete=models.CASCADE)
    backup_name = models.CharField(max_length=100)
    backup_file_path = models.CharField(max_length=100)
    backup_druation = models.SmallIntegerField()
    backup_status = models.SmallIntegerField()
    binlog_file_path = models.CharField(max_length=100)
    binlog_index = models.CharField(max_length=100)
    binlog_start = models.CharField(max_length=50)
    binlog_end = models.CharField(max_length=50)
    binlog_backup_status = models.SmallIntegerField(default=0)
    binlog_backup_piece = models.CharField(max_length=50)
    r_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dbms_mysql_backuped_info'
        index_together = ('machine_id', 'r_time', 'backup_status')