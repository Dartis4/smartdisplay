from django.db import models

#TODO create a class for timezone choices

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # def __str__(self):
    #     return ' '.join([self.first_name.to_python(str), self.last_name.to_python(str)])

class User_Setting(model.Model):
    name = models.CharField(max_length=30)
    value = models.AutoField()


class API(models.Model):
    name = models.CharField(max_length=30)
    base_address = models.URLField()
    format = models.CharField(max_length=10)
    params = models.CharField()
    token = models.CharField(max_length=300)
    # def __str__(self):
    #     return self.name.to_python(str)
