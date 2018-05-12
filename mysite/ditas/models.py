from django.db import models
from django import forms
# Create your models here.

class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    kakao_id = models.CharField(max_length=100,help_text="kakaotalk id")
    u_name = models.CharField(max_length=20)
    gender = models.IntegerField(default=0) # 0 : man, 1 : woman
    age = models.IntegerField(default=0) # age
    height = models.FloatField(null=True, blank=True, default=None)
    weight = models.FloatField(null=True, blank=True, default=None)
    canReceive = models.IntegerField(default=0) # 0 : no, 1 : yes
    logURL = models.URLField(max_length=200,default='http://localhost')

class Inform(models.Model):
    address = models.CharField(max_length=200, help_text="news address", primary_key=True)
    dateTime = models.DateTimeField()

class InformCall(models.Model):
    u_id = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.ForeignKey(Inform,on_delete=models.CASCADE)
    time = models.TimeField((u"Information Addressing Time"), blank=True)

class BloodSugar(models.Model):
    u_id = models.ForeignKey(User,on_delete=models.CASCADE)
    time = models.DateTimeField()
    data = models.FloatField(null=True, blank=True, default=None)

class Food(models.Model):
    f_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=40)
    f_name = models.CharField(max_length=40,primary_key=True)
    amountStd = models.IntegerField(default=100)
    cal = models.FloatField(null=True, blank=True, default=None)
    dang = models.FloatField(null=True, blank=True, default=None)
    nat = models.FloatField(null=True, blank=True, default=None)
    fat = models.FloatField(null=True, blank=True, default=None)
    chol = models.FloatField(null=True, blank=True, default=None)

class Meal(models.Model):
    u_id = models.ForeignKey(User,on_delete=models.CASCADE)
    f_id = models.ForeignKey(Food,on_delete=models.CASCADE)
    eat_time = models.DateTimeField()

class Medicine(models.Model):
    u_id = models.ForeignKey(User,on_delete=models.CASCADE)
    med_name = models.CharField(max_length=40)
    med_time = models.DateTimeField()

class Hospital(models.Model):
    u_id = models.ForeignKey(User,on_delete=models.CASCADE)
    hos_area = models.CharField(max_length=40)
    hos_name = models.CharField(max_length=40)
    visit_date = models.DateTimeField()

class WeightLog(models.Model):
    u_id = models.ForeignKey(User,on_delete=models.CASCADE)
    r_time = models.DateTimeField()
    r_weight = models.FloatField(null=True, blank=True, default=None)






