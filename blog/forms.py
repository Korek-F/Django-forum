from django import forms
from .models import Profile, ProfileImage


class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    birth_date = forms.DateField(widget=forms.DateInput)
    country = forms.CharField(max_length=30, required=False)
    city = forms.CharField(max_length=30, required=False)
    height = forms.DecimalField(max_value=300,min_value=0, required=False)
    weight = forms.DecimalField(max_value=300,min_value=0, required=False)
    CHOICES = [("Mężczyzna","Male"),("Kobieta","Female")]
    gender = forms.ChoiceField(widget=forms.Select, choices=CHOICES, required=False)
    description = forms.CharField(max_length=400,widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ('image',)