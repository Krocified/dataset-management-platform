from django import forms

class ZipForm(forms.Form):
    zip_file = forms.FileField(label='Select Task file')