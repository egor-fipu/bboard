from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

from .apps import user_registered
from .models import AdvUser, Bb, AdditionalImage, Comment, SubRubric, \
    SuperRubric


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'send_messages'
        )


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name',
                  'last_name', 'send_messages')


class SubRubricForm(forms.ModelForm):
    """Форма создана, чтобы поле надрубрки было обязательным для заполнения
    в админке"""
    super_rubric = forms.ModelChoiceField(queryset=SuperRubric.objects.all(),
                                          empty_label=None, label='Надрубрика',
                                          required=True)

    class Meta:
        model = SubRubric
        fields = '__all__'


class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='')


class BbForm(forms.ModelForm):
    class Meta:
        model = Bb
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


AIFormSet = inlineformset_factory(Bb, AdditionalImage, fields='__all__')


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'bb': forms.HiddenInput}


class GuestCommentForm(forms.ModelForm):
    captcha = CaptchaField(label='Введите текст с картинки',
                           error_messages={'invalid': 'Неправильный текст'})

    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'bb': forms.HiddenInput}
