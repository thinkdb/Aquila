from django.db import models
# 备份恢复相关的表结构


class MysqlBackupSourceInfo(models.Model):
    id = models.AutoField(primary_key=True)
    generator_room_name = models.CharField(max_length=30)
    ipaddr = models.IntegerField()
    port = models.SmallIntegerField()
    service_level = models.SmallIntegerField()
    defaults_file = models.CharField(max_length=100)
    back_time = models.TimeField()
    transport_time = models.TimeField(default='1980-01-01 01:01:01')
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


# sql发布相关表结构
class InceptionWorkOrderInfo(models.Model):
    id = models.AutoField(primary_key=True)
    work_order_id = models.BigIntegerField(unique=True)
    work_user = models.CharField(max_length=50)
    db_host = models.UnsignedIntegerField(default='1000000')
    db_name = models.CharField(max_length=50, default='test_db')
    end_time = models.DateTimeField(default='1980-01-01 01:01:01')
    review_user = models.CharField(max_length=50)
    review_time = models.DateTimeField(default='1980-01-01 01:01:01')
    review_status = models.SmallIntegerField(default=10)
    work_status = models.SmallIntegerField(default=10)
    r_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dbms_ince_work_order_info'


class InceptionAuditDetail(models.Model):
    id = models.AutoField(primary_key=True)
    work_order = models.ForeignKey('InceptionWorkOrderInfo', on_delete=models.CASCADE, to_field='work_order_id')
    sql_sid = models.SmallIntegerField()
    status = models.SmallIntegerField()
    err_id = models.SmallIntegerField()
    stage_status = models.SmallIntegerField()
    error_msg = models.CharField(max_length=1000)
    sql_conten = models.CharField(max_length=1000)
    aff_row = models.SmallIntegerField()
    rollback_id = models.CharField(max_length=50)
    backup_dbname = models.CharField(max_length=100)
    execute_time = models.IntegerField()
    sql_hash = models.CharField(max_length=50)
    r_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dbms_ince_audit_detail'


class InceptionWorkSQL(models.Model):
    id = models.AutoField(primary_key=True)
    work_order = models.ForeignKey('InceptionWorkOrderInfo', on_delete=models.CASCADE, to_field='work_order_id')
    sql_content = models.TextField()

    class Meta:
        db_table = 'dbms_ince_work_sql_content'


