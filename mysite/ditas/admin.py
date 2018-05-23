from django.contrib import admin

from .models import User
from .models import Blood
from .models import Food
from .models import Meal
from .models import Medicine
from .models import Hospital
from .models import Weight

# Register your models here.

admin.site.register(User)
admin.site.register(Blood)
admin.site.register(Food)
admin.site.register(Meal)
admin.site.register(Medicine)
admin.site.register(Hospital)
admin.site.register(Weight)

