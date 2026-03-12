from django.db import models


class Application(models.Model):
    STATUS_CHOICES = [
        ("new", "Новая"),
        ("in_progress", "В работе"),
        ("done", "Выполнена"),
        ("cancelled", "Отменена"),
    ]
    SOURCE_CHOICES = [
        ("general", "Общая"),
        ("service", "Услуга"),
        ("product", "Товар"),
    ]

    name = models.CharField(max_length=200, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    message = models.TextField(blank=True, verbose_name="Сообщение")
    service = models.ForeignKey(
        "services.Service",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Услуга",
    )
    product = models.ForeignKey(
        "catalog.Product",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Товар",
    )
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="general")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    manager_comment = models.TextField(blank=True, verbose_name="Комментарий менеджера")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self) -> str:
        return f"Заявка #{self.id} — {self.name} ({self.phone})"

