from django import forms
from django.forms import ValidationError

from user.models import Profile


class ProfileForm(forms.ModelForm):
    def clean_max_distance(self):
        cleansd_data = self.clean()
        min_distance = cleansd_data.get('min_distance')
        max_distance = cleansd_data.get('max_distance')
        if min_distance > max_distance:
            raise ValidationError('min distance > max distance')
        return max_distance

    def clean_max_dating_age(self):
        cleansd_data = self.clean()
        min_dating_age = cleansd_data.get('min_dating_age')
        max_dating_age = cleansd_data.get('max_dating_age')
        if min_dating_age > max_dating_age:
            raise ValidationError('min dating age > max dating age')
        return max_dating_age

    class Meta:
        model = Profile
        fields = '__all__'
        # exclude = ['auto_play']  # 排除哪个字段不要