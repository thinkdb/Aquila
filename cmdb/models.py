from django.db import models

# Create your models here.
# host_group = models.ForeignKey('HostGroup'， to_field='nid)
# 与 HostGroup 中的 nid 相关键


class UserRole(models.Model):
    user_role_name = models.CharField(max_length=50, unique=True)
    user_role_jd = models.CharField(max_length=50)

    class Meta:
        db_table = 'cmdb_user_role'


class UserGroup(models.Model):
    user_group_name = models.CharField(max_length=50, unique=True)
    user_group_jd = models.CharField(max_length=50)

    class Meta:
        db_table = 'cmdb_user_group'


class UserInfo(models.Model):
    user_name = models.CharField(max_length=40, unique=True)
    user_pass = models.CharField(max_length=96)
    user_emails = models.CharField(max_length=100)
    permission = models.ForeignKey('AuthPermissions')
    role = models.ForeignKey('UserRole')
    user_group = models.ForeignKey('UserGroup')

    class Meta:
        db_table = 'cmdb_user_info'


class HostGroup(models.Model):
    host_group_name = models.CharField(max_length=50, unique=True)
    host_group_jd = models.CharField(max_length=50)

    class Meta:
        db_table = 'cmdb_host_group'

    def __str__(self):
        return self.host_group_name


class UserHostRelationship(models.Model):
    user_group = models.ForeignKey('UserGroup')
    host_group = models.ForeignKey('HostGroup')
    lifetime = models.SmallIntegerField()
    expired = models.TinyIntegerField()

    class Meta:
        db_table = 'cmdb_user_host_relationship'
        unique_together = ('user_group', 'host_group')


class HostInfo(models.Model):
    host_ip = models.UnsignedIntegerField(unique=True)
    app_type = models.CharField(max_length=20)
    host_user = models.CharField(max_length=20)
    host_pass = models.CharField(max_length=30)
    host_port = models.SmallIntegerField()
    host_group = models.ForeignKey(to='HostGroup', to_field='id', db_constraint=False)

    class Meta:
        db_table = 'cmdb_host_info'


class HostInfoAuth(models.Model):
    host = models.ForeignKey(to='HostInfo', to_field='id', db_constraint=False)
    app_user = models.CharField(max_length=20)
    app_pass = models.CharField(max_length=30)
    app_port = models.SmallIntegerField()

    class Meta:
        db_table = 'cmdb_host_auth'


class AuthPermissions(models.Model):
    select_host = models.TinyIntegerField()
    update_host = models.TinyIntegerField()
    insert_host = models.TinyIntegerField()
    delete_host = models.TinyIntegerField()
    select_user = models.TinyIntegerField()
    update_user = models.TinyIntegerField()
    delete_user = models.TinyIntegerField()
    insert_user = models.TinyIntegerField()

    class Meta:
        db_table = 'cmdb_auth_permissions'


class AuthGroupPermissions(models.Model):
    user_group = models.ForeignKey('UserGroup')
    permission = models.ForeignKey('AuthPermissions')

    class Meta:
        db_table = 'cmdb_auth_group_permissions'