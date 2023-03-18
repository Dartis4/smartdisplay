from django.db import models
from django.forms import ModelForm
from django.urls import reverse


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return ' '.join([self.first_name.to_python(str), self.last_name.to_python(str)])


class API(models.Model):
    name = models.CharField(max_length=30, default='')
    base_address = models.URLField(max_length=100, default='')
    format = models.CharField(max_length=10, default='')
    params = models.CharField(max_length=100, default='')
    token = models.CharField(max_length=30, default='')
    switch_display_zones = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('displayconf:results', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class ApiForm(ModelForm):
    class Meta:
        model = API
        fields = '__all__'
