from django.db import models
# 备份恢复相关的表结构


class MysqlBackupSourceInfo(models.Model):
    id = models.AutoField(primary_key=True)
    generator_room_name = models.CharField(max_length=30)
    ipaddr = models.UnsignedIntegerField()
    port = models.UnsignedSmallIntegerField()
    service_level = models.TinyIntegerField()
    defaults_file = models.CharField(max_length=100)
    back_time = models.TimeField()
    transport_time = models.TimeField(default='1980-01-01 01:01:01')
    is_transport = models.SmallIntegerField(default=0)
    back_pool_id = models.ForeignKey('BackupPoolInfo', on_delete=models.CASCADE, db_constraint=False)
    r_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dbms_mysql_backup_source_info'
        unique_together = ('generator_room_name', 'ipaddr', 'port')


class BackupPoolInfo(models.Model):
    id = models.AutoField(primary_key=True)
    pool_name = models.CharField(max_length=50)
    ipaddr = models.IntegerField()
    port = models.UnsignedSmallIntegerField()
    passwd = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

    class Meta:
        db_table = 'dbms_mysql_backup_pool_source_info'


class BackupedBinlogInfo(models.Model):
    id = models.AutoField(primary_key=True)
    machine_id = models.ForeignKey('MysqlBackupSourceInfo', on_delete=models.CASCADE, db_constraint=False)
    binlog_name = models.CharField(max_length=50)
    binlog_create_time = models.DateTimeField()
    binlog_size = models.UnsignedSmallIntegerField()
    r_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dbms_mysql_backuped_binlog_info'
        index_together = ('machine_id', 'r_time')


class BackupedInfo(models.Model):
    id = models.AutoField(primary_key=True)
    machine_id = models.ForeignKey('MysqlBackupSourceInfo', on_delete=models.CASCADE, db_constraint=False)
    backup_name = models.CharField(max_length=100)
    backup_file_path = models.CharField(max_length=100)
    backup_druation = models.UnsignedSmallIntegerField()
    backup_status = models.TinyIntegerField()
    binlog_file_path = models.CharField(max_length=100)
    binlog_index = models.CharField(max_length=100)
    binlog_start = models.CharField(max_length=50)
    binlog_end = models.CharField(max_length=50)
    binlog_backup_status = models.TinyIntegerField(default=0)
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
    db_host = models.CharField(max_length=45)
    db_name = models.CharField(max_length=50, default='test_db')
    end_time = models.DateTimeField(default='1980-01-01 01:01:01')
    review_user = models.CharField(max_length=50)
    review_time = models.DateTimeField(default='1980-01-01 01:01:01')
    review_status = models.TinyIntegerField(default=10)    # 10表示未审核， 0 表示通过， 1表示驳回
    work_status = models.TinyIntegerField(default=10)      # 10表示未执行， 0 表示执行成功， 1表示执行失败, 2.进行执行队列， 3, 正在执行
    r_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dbms_ince_work_order_info'


class InceptionAuditDetail(models.Model):
    id = models.AutoField(primary_key=True)
    work_order = models.ForeignKey(to='InceptionWorkOrderInfo', on_delete=models.CASCADE, to_field='work_order_id', db_constraint=False)
    sql_sid = models.UnsignedSmallIntegerField()              # 工单中的sql序号
    status = models.UnsignedSmallIntegerField()               # RERUN,CHECKED, EXECUTED, None 0,1,2,3
    err_id = models.UnsignedSmallIntegerField()               # 0, 1, 2
    stage_status = models.UnsignedSmallIntegerField()         # Audit completed： 0，Execute failed：1，  Execute Successfully：2, Execute Successfully\nBackup successfully：3, Execute Successfully\nBackup filed ：4
    error_msg = models.TextField()             # None, str,
    sql_content = models.TextField()           # sql内容
    aff_row = models.IntegerField()              # 影响的行数
    rollback_id = models.CharField(max_length=50)             # rollback_id
    backup_dbname = models.CharField(max_length=100)          # 存放备份的库名
    execute_time = models.IntegerField()                      # sql 执行好时，*1000， 按毫秒存放
    sql_hash = models.CharField(max_length=50)                # 用于 使用pt-osc 工具时查看进度, None
    r_time = models.DateTimeField(auto_now_add=True)         # 记录生成时间

    class Meta:
        db_table = 'dbms_ince_audit_detail'


class InceptionWorkSQL(models.Model):
    id = models.AutoField(primary_key=True)
    work_order = models.ForeignKey('InceptionWorkOrderInfo', on_delete=models.CASCADE, to_field='work_order_id', db_constraint=False)
    sql_content = models.TextField()

    class Meta:
        db_table = 'dbms_ince_work_sql_content'


class WorkOrderTask(models.Model):
    host_ip = models.CharField(max_length=45)
    app_user = models.CharField(max_length=20)
    app_pass = models.CharField(max_length=30)
    app_port = models.SmallIntegerField()
    wid = models.BigIntegerField(unique=True)