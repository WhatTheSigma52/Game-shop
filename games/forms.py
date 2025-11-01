from django import forms
from .models import Review



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', 'rating')
        labels = {'text': 'Текст комментария',
                  'rating': 'Рейтинг игры'}
        widgets = {'rating': forms.NumberInput(attrs={'class': 'form-control',
                                                      'min' : 1,
                                                      'max': 5,
                                                      'step': 0.5}),
                    'text': forms.Textarea(attrs={'class': 'form-control',
                                                  'rows': 4,
                                                  'placeholder': 'Напишите ваш отзыв.'})}

    def clean_text(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Поле не должно быть пустым')
        return data
