from django.db import models


# 用户
class user(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=48, null=False, blank=True)
    user_url = models.CharField(max_length=150, null=True, blank=True)
    user_sex = models.CharField(max_length=16, null=True, blank=True)
    user_address = models.CharField(max_length=40, null=True, blank=True)
    user_hometown = models.CharField(max_length=40, null=True, blank=True)
    user_birth = models.CharField(max_length=40, null=True, blank=True)
    user_status = models.CharField(max_length=16, null=True, blank=True)
    user_star = models.CharField(max_length=16, null=True, blank=True)
    user_blood = models.CharField(max_length=16, null=True, blank=True)
    user_height = models.IntegerField(null=True, blank=True)
    user_shape = models.CharField(max_length=16, null=True, blank=True)
    user_aim = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return self.user_name


# 文章
class blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    blog_title = models.CharField(max_length=80, null=False, db_index=True)
    blog_url = models.CharField(max_length=150, null=True)
    blog_content = models.TextField(null=False)
    blog_date_time = models.DateTimeField(auto_now=True)
    blog_view = models.IntegerField(default=0)
    blog_comment = models.IntegerField(default=0)
    blog_user = models.ForeignKey(user, null=True, blank=True, default=None, on_delete=models.CASCADE)
    blog_category = models.CharField(max_length=48, null=False, db_index=True)