from django.db import models

from django.utils import timezone


# class VisitCount(models.Model):
#     visits = models.IntegerField(default=0)
#     date = models.DateField(auto_now=False, auto_now_add=False, default=timezone.localtime)

#     def __str__(self) -> str:
        # return f"{self.visits} | {self.date}"

class GeneralData(models.Model):
    monthly_price = models.FloatField(default=10)
    yearly_price = models.FloatField(default=100)

    @classmethod
    def get_or_create(cls):
        try:
            return cls.objects.get()
        except: 
            general_data = cls()
            general_data.save()
        
            return general_data