from django.db import models
from django.core.validators import URLValidator
from django import forms
# Create your models here.

class User(models.Model):
    u_id = models.CharField(max_length=100,default="", null=False,primary_key = True)
    name = models.CharField(max_length=10)
    gender = models.CharField(max_length=5)
    birth_date = models.DateField(null=True) # associated age
    height = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return self.name

class Blood(models.Model):
    u_id = models.ForeignKey(User,on_delete=models.CASCADE)
    bld_time = models.DateTimeField()
    bld_data = models.FloatField()

    class Meta:
        unique_together = (("u_id","bld_time"),)

class Food(models.Model):
    f_id = models.AutoField(primary_key=True)
    f_type = models.CharField(max_length=40)
    f_name = models.CharField(max_length=60)
    f_sz = models.FloatField()
    f_kal = models.FloatField()
    f_car = models.FloatField() # 탄수화물(g)
    f_pro = models.FloatField() # 단백질(g)
    f_fat = models.FloatField() # 지방(g)
    f_dang = models.FloatField() # 당(g)
    f_ntr = models.FloatField() # 나트륨(mg)
    f_chol = models.FloatField() # 콜레스테롤(mg)

class Meal(models.Model):
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    f_id = models.ForeignKey(Food, on_delete=models.CASCADE)
    f_time = models.DateTimeField()

    class Meta:
        unique_together = (("u_id","f_id","f_time"),)


class Weight(models.Model):
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    kg_date = models.DateField()
    kg_value = models.FloatField()

    class Meta:
        unique_together = (("u_id","kg_date"),)

class Medicine(models.Model):
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    med_name = models.CharField(max_length=40)
    med_time = models.TimeField()

    class Meta:
        unique_together = (("u_id","med_name"),)

class Hospital(models.Model):
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    hos_name = models.CharField(max_length=40)
    hos_date = models.DateField()

    class Meta:
        unique_together = (("u_id","hos_name"),)


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    news_name = models.CharField(max_length=100)
    news_url = models.TextField(validators=[URLValidator])
    news_date = models.DateTimeField()

