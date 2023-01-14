from django.db import models
from datetime import datetime


class Room(models.Model):
    name = models.CharField(max_length=255, default="Room")
    room_id = models.AutoField(primary_key=True, editable=False)
    capacity = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} {self.room_id} {self.capacity} {self.price_per_day}"

class Reservation(models.Model):
    PAYMENT_METHODS = (
        ("Cash", "Cash"),
        ("Credit Card", "Credit Card"),
        ("PayPal", "PayPal"),
        ("pending", "pending"),
    )
    reservation_id = models.AutoField(primary_key=True, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default="pending")
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField() 
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="pending")
    total_persons = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.room} Date: {self.start_date} - {self.end_date} - Status: {self.status} - Customer: {self.customer_name} - {self.customer_email} - Total Price: {self.total_price} - Payment Method: {self.payment_method} - Total Persons: {self.total_persons}"
    def get_total_price(self):
        return self.room.price_per_day * (self.end_date - self.start_date).days

    def save(self, *args, **kwargs):
        self.total_price = self.get_total_price()
        super().save(*args, **kwargs)


