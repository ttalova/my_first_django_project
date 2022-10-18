from django import forms

from web.models import Advertisement


class AdvertForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        self.instance.user = self.initial['user']
        return super(AdvertForm, self).save(*args, **kwargs)

    class Meta:
        model = Advertisement
        fields = ('title', 'text', 'price')


class AuthForm(forms.Form):
    # first_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
