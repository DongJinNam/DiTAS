from django.db import models
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
    f_bs = models.FloatField()
    f_ntr = models.FloatField()
    f_fat = models.FloatField()
    f_chol = models.FloatField()

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

