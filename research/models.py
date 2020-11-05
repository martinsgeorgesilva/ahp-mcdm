from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.urls import reverse
import uuid

from groups.models import Groups
from django.db import models
import jsonfield


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class Research(BaseModel):
    created_by = models.ForeignKey(
        'user.User', 
        on_delete=models.PROTECT, 
        verbose_name=_("Criado por"),
        )
    Groups = models.ForeignKey(
        'groups.Groups', 
        on_delete=models.PROTECT, 
        verbose_name=_("Grupo"),
        )
    created_at = models.DateTimeField(auto_now_add=True,  null=True)
    objective = models.CharField(max_length=500)
    data_to_end = models.DateTimeField(null=True)

    def get_absolute_url(self):
        return reverse('research-detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.Groups.name

class Excution(BaseModel):
    group = models.ForeignKey(
        'groups.Groups', 
        on_delete=models.PROTECT, 
        verbose_name=_("Grupo"),
        related_name = 'Groups_group'

        )
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=100)
    who = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    answers = jsonfield.JSONField()
    ic = models.CharField(max_length=50)
    criterions = jsonfield.JSONField()
    preferences = jsonfield.JSONField()
    age = models.CharField(max_length=100)
    time_emp = models.CharField(max_length=100)
    time_xp = models.CharField(max_length=100)
    sexo = models.CharField(max_length=100)
    escolaridade = models.CharField(max_length=100)


