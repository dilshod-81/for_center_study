from course.models import *
from datetime import date

from course.models import Student, Course

from django.db import models
from django.utils.timezone import now
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import qrcode
from django.core.files import File

class PayToCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    transfer_summ = models.PositiveBigIntegerField()
    date = models.DateField(default=now)
    cheque_image = models.ImageField(upload_to='cheques/', blank=True, null=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def __str__(self):
        return f"{self.student.full_name} paid {self.transfer_summ} sum to {self.course}"

    def save(self, *args, **kwargs):
        if not self.cheque_image:
            self.generate_cheque()
        super().save(*args, **kwargs)

    def generate_cheque(self):
        # Create a blank cheque image
        cheque = Image.new('RGB', (600, 300), color=(255, 255, 255))
        d = ImageDraw.Draw(cheque)

        # Define fonts
        try:
            font = ImageFont.truetype("arial.ttf", 20)
            font_bold = ImageFont.truetype("arialbd.ttf", 24)
        except IOError:
            font = ImageFont.load_default()
            font_bold = ImageFont.load_default()

        # Draw cheque details
        d.text((30, 30), "Mrit Academy", font=font_bold, fill=(0, 0, 0))
        d.text((30, 70), f"O`quvchi: {self.student.full_name}", font=font, fill=(0, 0, 0))
        d.text((30, 110), f"Kurs: {self.course.name}", font=font, fill=(0, 0, 0))
        d.text((30, 150), f"To`landi: {self.transfer_summ}, so`m", font=font, fill=(0, 0, 0))
        d.text((30, 190), f"Sana: {self.date}", font=font, fill=(0, 0, 0))
        d.text((30, 230), "Imzo :", font=font, fill=(0, 0, 0))

        # Generate QR code
        qr_data = f"Student: {self.student.full_name}, Course: {self.course.name}, Amount: {self.transfer_summ}, Date: {self.date}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        self.qr_code.save(f'qr_{self.id}.png', File(buffer), save=False)

        # Paste the QR code onto the cheque
        qr_img = qr_img.resize((100, 100))
        cheque.paste(qr_img, (450, 180))

        # Save cheque image
        buffer = BytesIO()
        cheque.save(buffer, format='PNG')
        self.cheque_image.save(f'cheque_{self.id}.png', File(buffer), save=False)


class AddCashToWallet(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    summ = models.PositiveBigIntegerField()
    date = models.DateField(default=date.today, blank=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True, blank=True)
    recepient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    def __str__(self):
        return f"{self.summ} is transferred to {self.student}'s wallet on {self.date} at {self.time} by {self.recepient}"

class GiveSalary(models.Model):
      teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher")
      salary_summ = models.PositiveBigIntegerField()
      date = models.DateField(default= date.today(), blank=True, null=True )
      sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="sender")

      def __str__(self):
            return str(self.salary_summ) + ' is given to ' + str(self.teacher)



class Genraldata(models.Model):
      student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student")
      month = models.PositiveBigIntegerField()
      payment_status = models.BooleanField()


class Discounted_students(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    discount_summ = models.PositiveBigIntegerField()
    date = models.DateField(default=date.today, blank=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True, blank=True)
    recepient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.discount_summ} is transferred to {self.student}'s wallet on {self.date} at {self.time} by {self.recepient}"