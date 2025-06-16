from django import forms
from .models import TestCase, TestSummary

class TestCaseForm(forms.ModelForm): #the form is based on the model
    class Meta: #Metaclass is used to configure the form
        model = TestCase #the model that the form will be based on
        fields = '__all__'  #every field in the model will be editable via the form.

class TestSummaryForm(forms.ModelForm):
    class Meta:
        model = TestSummary
        fields = '__all__'
