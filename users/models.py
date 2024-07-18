from django.db import models
# from users.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.
from course.validators import validate_phone_number
class User(AbstractUser):
      is_teacher = models.BooleanField(default=False, help_text = 'Agar yaratilayotgan foydalanuvchi ustoz bo\'lsa.')
      is_admin  = models.BooleanField(default = False,  help_text = 'Agar yaratilayotgan foydalanuvchi adminstrator bo\'lsa.')
      is_student = models.BooleanField(default=False, help_text = 'Agar yaratilayotgan foydalanuvchi O`quvchi bo\'lsa.')
      phone_number = models.CharField(max_length=120, validators=[validate_phone_number], help_text = 'telefon raqam +998 dan boshlanishi va undan tashqari 9 ta sondan tashkil topishi kerak')
      wallet = models.PositiveBigIntegerField(default=0)
      image = models.ImageField(upload_to='users/', blank=True, null=True)
      # user = User
      def __str__(self):
            if  self.is_teacher == True and self.is_admin ==False:
                  return  "Ustoz: " + str( self.first_name ) + " "+str(self.last_name)
            elif self.is_teacher == False and self.is_admin ==True:      
                  return  "Admin: "+ str( self.first_name ) + " "+str(self.last_name)
            elif self.is_student == True and self.is_admin == False:
                  return "O'quvchi: " + str( self.first_name ) + " "+str(self.last_name)

            else:
                  return str( self.first_name ) + " "+str(self.last_name)



