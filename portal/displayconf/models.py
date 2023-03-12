from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return ' '.join([self.first_name.to_python(str), self.last_name.to_python(str)])


class API(models.Model):
    name = models.CharField(max_length=30)


class APIData(models.Model):
    name = models.ForeignKey(API, on_delete=models.CASCADE)
    base_address = models.URLField()
    format = models.CharField(max_length=10)
    params = models.CharField(max_length=100)
    token = models.CharField(max_length=30)
    switch_zones = models.BooleanField()

    def __str__(self):
        return self.name.to_python(str)

