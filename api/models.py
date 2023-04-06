from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    balance = models.FloatField(null=False, blank=False, default=0.0)

class Operation(models.Model):
    TYPE_CHOICES = (
        (1, "addition"),
        (2, "substraction"),
        (3, "multiplication"),
        (4, "division"),
        (5, "square_root"),
        (6, "random_string"),
    )
    ARITHMETIC_OPERATIONS = [1,2,3,4,5]

    type = models.IntegerField(choices=TYPE_CHOICES, null=False)
    cost = models.FloatField(null=False, blank=False, default=0.0)
    

    @property
    def type_str(self):
        return [v[1] for v in self.TYPE_CHOICES if v[0] == self.type][0]
    
    def __str__(self):
        return "{} {}".format(self.type_str, self.cost)


class Record(models.Model):
    cost = models.FloatField(null=False, blank=False, default=0.0)
    user_balance = models.FloatField(null=False, blank=False, default=0.0)
    operation_response = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return "{} {}".format(self.user, self.operation)

