from django.forms import ModelForm
from .models import User
from django import forms

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User  # Replace with your user model
        fields = ['first_name', 'last_name', 'username', 'email', 'image']  # Include 'image' field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False  # Allow image field to be optional
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})  # Add class for styling

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 4 * 1024 * 1024:  # 4 MB limit
                raise forms.ValidationError("Rasm fayli hajmi 4 MB dan oshmasligi kerak.")
        return image