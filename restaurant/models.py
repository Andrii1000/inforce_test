from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField(default='Empty')

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    day = models.DateField()
    dishes = models.TextField()

    class Meta:
        unique_together = ('restaurant', 'day')

    def __str__(self):
        return f'{self.restaurant.name} - {self.day}'


class Vote(models.Model):
    employee = models.ForeignKey('user.Employee', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    vote_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'menu')

    def __str__(self):
        return f'{self.employee.user.username} voted for {self.menu.restaurant.name}'
