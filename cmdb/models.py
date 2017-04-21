from django.db import models

# Create your models here.


class UserRole(models.Model):
    user_role_name = models.CharField(max_length=50)
    user_role_jd = models.CharField(max_length=50)

    class Meta:
        db_table = 'cmdb_user_role'
        unique_together = ('user_role_name', 'user_role_jd')


class UserGroup(models.Model):
    user_group_name = models.CharField(max_length=50)
    user_group_jd = models.CharField(max_length=50)

    class Meta:
        db_table = 'cmdb_user_group'
        unique_together = ('user_group_name', 'user_group_jd')


class UserInfo(models.Model):
    user_name = models.CharField(max_length=40, unique=True)
    user_pass = models.CharField(max_length=40)
    user_emails = models.CharField(max_length=100)
    permission = models.ForeignKey('AuthPermissions')
    role = models.ForeignKey('UserRole')
    user_group = models.ForeignKey('UserGroup')

    class Meta:
        db_table = 'cmdb_user_info'


class HostGroup(models.Model):
    host_group_name = models.CharField(max_length=50)
    host_group_jd = models.CharField(max_length=50)

    class Meta:
        db_table = 'cmdb_host_group'
        unique_together = ('host_group_name', 'host_group_jd')


class UserHostRelationship(models.Model):
    user_group = models.ForeignKey('UserGroup', rel='id')
    host_group = models.ForeignKey('HostGroup', rel='id')
    lifetime = models.SmallIntegerField()
    expired = models.TinyIntegerField()

    class Meta:
        db_table = 'cmdb_user_host_relationship'
        unique_together = ('user_group', 'host_group')


class HostInfo(models.Model):
    host_ip = models.UnsignedIntegerField()
    app_type = models.CharField(max_length=20)
    app_user = models.CharField(max_length=20)
    app_pass = models.CharField(max_length=30)
    app_port = models.SmallIntegerField()
    host_group = models.ForeignKey('HostGroup', rel='id')

    class Meta:
        db_table = 'cmdb_host_info'
        index_together = ('host_ip', 'app_type', 'app_port',)


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