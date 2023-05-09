from django.contrib import admin
from .models import Academic, Skill,User,Cv,Profile,Referee,Experiance,Links,Language,Hobbies,ECA

model_list = [Cv,User,Profile,Academic,Experiance,Links,Skill,Language,Hobbies,ECA,Referee]
admin.site.register(model_list)

