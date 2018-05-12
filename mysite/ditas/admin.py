from django.contrib import admin
from .models import User
from .models import Inform
from .models import InformCall
from .models import BloodSugar
from .models import Food
from .models import Meal
from .models import Medicine
from .models import Hospital
from .models import WeightLog
# Register your models here.

admin.site.register(User)
admin.site.register(Inform)
admin.site.register(InformCall)
admin.site.register(BloodSugar)
admin.site.register(Food)
admin.site.register(Meal)
admin.site.register(Medicine)
admin.site.register(Hospital)
admin.site.register(WeightLog)

