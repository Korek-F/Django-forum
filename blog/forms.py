from django import forms
from .models import Profile, ProfileImage, Report_Post


class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False, label="Imię")
    last_name = forms.CharField(max_length=30, required=False, label="Nazwisko")
    birth_date = forms.DateField(widget=forms.DateInput, label="Data urodzenia")
    country = forms.CharField(max_length=30, required=False, label="Kraj")
    city = forms.CharField(max_length=30, required=False, label="Miasto")
    height = forms.DecimalField(max_value=300,min_value=0, required=False, label="Wzrost")
    weight = forms.DecimalField(max_value=300,min_value=0, required=False, label="Waga")
    CHOICES = [("Mężczyzna","Male"),("Kobieta","Female")]
    gender = forms.ChoiceField(widget=forms.Select, choices=CHOICES, required=False, label="Płeć")
    description = forms.CharField(max_length=400,widget=forms.Textarea, required=False, label="Opis")

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ('image',)

class ReportPostForm(forms.ModelForm):
    class Meta:
        model = Report_Post
        fields = ('report_type',)
        widgets = {
            'report_type': forms.Select(attrs={'class':"form-control"}),
        }
        labels = {
            "report_type": "Zgłoś za",
        }

from django.contrib.auth import get_user_model
from  django.contrib.auth.forms import PasswordChangeForm
class ResetPassword(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control',"placeholder":"Nowe hasło"})
        self.fields['new_password1'].label = ""

        self.fields['new_password2'].widget.attrs.update({'class': 'form-control',"placeholder":"Nowe hasło"})
        self.fields['new_password2'].label = ""

        self.fields['old_password'].widget.attrs.update({'class': 'form-control',"placeholder":"Stare hasło","label":""})
        self.fields['old_password'].label = ""
    


        