from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('about', 'birth_date', 'avatar')
        labels = {'about': 'О себе',
                  'birth_date': 'Дата рождения',
                  'avatar': 'Аватар'}
        help_texts = {'about': 'Напиши о себе',
                      'birth_date': 'Выбери дату своего рождения',
                      'avatar': 'Вставь сюда свой аватар'}
        widgets = {'about': forms.Textarea(attrs={'class': 'form-control',
                                                  'rows': 3,
                                                  'placeholder': 'Напиши о себе'}),
                    'birth_date': forms.DateInput(attrs={'class': 'form-control',
                                                         'type': 'date'}),
                    'avatar': forms.FileInput(attrs={'class': 'form-control'})}
