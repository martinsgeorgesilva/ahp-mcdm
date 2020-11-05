from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.urls import reverse
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Groups(BaseModel):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        'user.User', 
        on_delete=models.PROTECT, 
        verbose_name=_("Criado por"),
        related_name='user_created_by'        
    )
    created_at = models.DateTimeField(auto_now_add=True,  null=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('groups:detail', kwargs={'pk': self.pk})

    def relations_count(self):
        a = GroupRelationship.objects.filter(group=self.id).count()
        return a

    def amount_questions(self):
        sum = 0
        for i in range(1,self.relations_count()):
            sum += i
        return sum

    def __str__(self):
        return self.name

class GroupRelationship(BaseModel):
    group = models.ForeignKey(
        'groups.Groups', 
        on_delete=models.PROTECT, 
        verbose_name=_("Grupo"),
    )
    criterion = models.ForeignKey(
        'criterion.Criterion', 
        on_delete=models.PROTECT, 
        verbose_name=_("Critério"),
    )

    def get_absolute_url(self):
        return reverse('groups:groups', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.criterion.name
