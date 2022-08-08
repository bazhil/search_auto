from django.db import models
from abc import abstractmethod
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


def year_choices():
    return [(r, r) for r in range(1960, datetime.date.today().year+1)]


# Create your models here.
class Venicle(type):
    """
    Абстрактный класс с общими для всех транспортных средств свойствами.
    """

    @abstractmethod
    def move(self):
        """
        Переместить объект
        """
        pass

    @abstractmethod
    def speed(self):
        """
        Скорость транспортного средства
        """
        pass


class Categories(models.Model):
    """
    Категории автомобилей
    """
    category = models.CharField(max_length=150)
    description = models.CharField(max_length=200)


class Auto(models.Model):
    """
    Модель Автомобиля
    """
    __metaclass__ = Venicle

    mark = models.CharField(max_length=150)
    model = models.CharField(max_length=150)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    reg_number = models.CharField(max_length=12)
    issue_year = models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1960),
                                                                                 max_value_current_year])
    vin = models.CharField(max_length=17)
    sts_number = models.CharField(max_length=30)
    sts_date = models.DateField()
    description = models.CharField(max_length=300, blank=True)
    photo = models.ImageField()

    def __str__(self):
        return f'{self.mark} {self.model} {self.issue_year}'
