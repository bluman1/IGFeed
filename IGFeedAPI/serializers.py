""" Author and finisher of this script is Michael on 17/09/2016 """
from rest_framework import serializers

from IGFeedAPI.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
