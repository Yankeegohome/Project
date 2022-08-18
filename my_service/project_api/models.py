from django.db import models
from datetime import datetime

class Device(models.Model):

    manufacturer = models.CharField(max_length=255,verbose_name="Произоводитель")
    model = models.CharField(max_length=255, verbose_name="Модель оборудования")

    class Meta:
        db_table = "devices"
        verbose_name = "Оборудавние в наличии"
        verbose_name_plural = "Оборудование в наличии"

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

class Customer(models.Model):

    class Meta:
        db_table = "customers"
        verbose_name = "Пользователь оборудования"
        verbose_name_plural = "Пользователи оборудования"

    customer_name = models.CharField(max_length=255, verbose_name="Название организации")
    customer_address = models.CharField(max_length=255, verbose_name="Адрес")
    customer_city = models.CharField(max_length=255, verbose_name="Город")

    def __str__(self):
        return f"{self.customer_name} по адресу {self.customer_address}"

class DeviceInField(models.Model):

    serial_number = models.CharField(max_length=255, verbose_name="Серийный номер")
    customer_id = models.ForeignKey(Customer, on_delete=models.RESTRICT, verbose_name="Адрес пользователя")
    analyzer_id = models.ForeignKey(Device, on_delete=models.RESTRICT, verbose_name="Модель оборудования")
    owner_status = models.CharField(max_length=255,verbose_name="Статус принадлежности")

    class Meta:
        db_table = "devicesInField"
        verbose_name = "Используемое оборудавние "
        verbose_name_plural = "Используемые оборудования"

    def __str__(self):
        return f"{self.analyzer_id} с/н {self.serial_number} в {self.customer_id}"



# def status_validator(order_status):
#     if order_status not in ["open", "closed", "in progress", "need info"]:
#         raise ValidationError(
#             gettext_lazy('%(order_status)s is wrong oreder status'),
#             params={'order_status': order_status},
#         )

class Order(models.Model):
    statuses = (("open", "открыта"),
                ("closed", "закрыта"),
                ("in progress", "в работе"),
                ("need info", "нужна информация"))

    device = models.ForeignKey(DeviceInField, verbose_name="Оборудование", on_delete=models.RESTRICT)
    order_description = models.TextField(verbose_name="Описание проблемы")
    created_at = models.DateTimeField(verbose_name="Создано", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Последнее изменение", blank=True, null=True)
    order_status = models.CharField(max_length=100, verbose_name="Статус заявки", choices=statuses)

    def __str__(self):
        return f"Заявка №{self.id} для {self.device}"

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "orders"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

