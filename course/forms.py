from django import forms
from .models import *

class DynamicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DynamicForm, self).__init__(*args, **kwargs)
        fields = DynamicField.objects.all()
        for field in fields:
            if field.field_type == 'char':
                self.fields[field.name] = forms.CharField(label=field.name, max_length=255)
            elif field.field_type == 'int':
                self.fields[field.name] = forms.IntegerField(label=field.name)
            elif field.field_type == 'choice':
                choices = [(choice.strip(), choice.strip()) for choice in field.choices.split(',')]
                self.fields[field.name] = forms.ChoiceField(label=field.name, choices=choices)


class DynamicFieldForm(forms.ModelForm):
    class Meta:
        model = DynamicField
        fields = ['name', 'field_type', 'choices']
        widgets = {
            'field_type': forms.Select(choices=DynamicField.FIELD_TYPES),
            'choices': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Comma-separated values for ChoiceField'}),
        }
        labels = {
            'name': 'Field Name',
            'field_type': 'Field Type',
            'choices': 'Choices (for ChoiceField)',
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'task', 'date', 'file', 'course']

class GradeForm(forms.ModelForm):
    def __init__(self, course=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if course:
            self.fields['student'].queryset = course.students.all()

    class Meta:
        model = Grade
        fields = ['student', 'grade']

class EditGradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['grade']




class CourseForm(forms.ModelForm):
    student_search = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.SelectMultiple(attrs={'size': 10}),
        label='Students',
        required=False  # Allow the field to be optional
    )

    class Meta:
        model = Course
        fields = ['name', 'student_search']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_search'].queryset = Student.objects.all()

    def clean_student_search(self):
        students = self.cleaned_data['student_search']
        return students

class CourseFilterForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=False)


class ReceiptionForm(forms.ModelForm):
    class Meta:
        model = Receiption
        fields = ['full_name', 'phone_number', 'course', 'info_text','status']

# forms.py
from django import forms
from payment.models import Discounted_students

class DiscountedStudentsForm(forms.ModelForm):
    class Meta:
        model = Discounted_students
        fields = ['student', 'discount_summ', 'date']


from .models import Deal

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['student', 'teacher', 'course', 'price']

