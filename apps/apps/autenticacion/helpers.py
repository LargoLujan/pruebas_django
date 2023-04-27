# helpers.py
from django.contrib.auth import get_user_model
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat

from .models import CustomUser


def get_users_with_group():
    users = CustomUser.objects.all().annotate(
        display_name=Concat(
            F('username'),
            Value(' ('),
            F('groups__name'),
            Value(')'),
            output_field=CharField()
        )
    )
    return users
