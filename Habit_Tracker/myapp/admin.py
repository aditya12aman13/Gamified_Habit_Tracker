from django.contrib import admin
from .models import Habit, HabitEntry

admin.site.register(Habit)
admin.site.register(HabitEntry)


