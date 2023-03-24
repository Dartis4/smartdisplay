from django.db import models
from django.forms import ModelForm
from django.urls import reverse


class API(models.Model):
    name = models.CharField(max_length=30, unique=True, default='')
    base_address = models.URLField(max_length=100, default='')
    format = models.CharField(max_length=10, blank=True)
    params = models.JSONField(max_length=100, blank=True, default=dict)
    token = models.JSONField(max_length=100, blank=True, default=dict)
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


class ApiData(models.Model):
    api = models.ForeignKey(API, on_delete=models.CASCADE)
    data = models.JSONField(max_length=500, default=dict)
    tags = models.JSONField(max_length=300, default=dict)

    def __str__(self):
        return self.data
