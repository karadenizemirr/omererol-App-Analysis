from django import forms

class UploadFileForm(forms.Form):
    app_file = forms.FileField()