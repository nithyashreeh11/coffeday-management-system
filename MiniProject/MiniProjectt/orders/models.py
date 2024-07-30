from django.db import models

class Coffee(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

class CartItem(models.Model):
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    session_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.coffee.name} - {self.quantity}"
