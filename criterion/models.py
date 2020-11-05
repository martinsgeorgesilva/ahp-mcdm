from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.urls import reverse
import uuid



class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class Criterion(BaseModel):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        'user.User', 
        on_delete=models.PROTECT, 
        verbose_name=_("Criado por"),
        null=True,
        blank=True
        )
    created_at = models.DateTimeField(auto_now_add=True,  null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def get_absolute_url(self):
        return reverse('criterion-detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.name