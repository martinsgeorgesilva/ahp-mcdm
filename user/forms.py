from django.contrib.auth.forms import UserCreationForm
from user.models import User

class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'occupation' , 'company', )