from django.db import models

class SubModel1(models.Model):
    # id = models.CharField(max_length=200, primary_key=True)
    id = models.AutoField(primary_key=True)
    age = models.IntegerField()
    name = models.CharField(max_length=100)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name
    

class SubModel2(models.Model):
    # id = models.CharField(max_length=200, primary_key=True)
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.description

class MainModel(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    title = models.CharField(max_length=100)
    submodel1 = models.ManyToManyField(SubModel1)  
    submodel2 = models.ManyToManyField(SubModel2) 
    def __str__(self):
        return self.title