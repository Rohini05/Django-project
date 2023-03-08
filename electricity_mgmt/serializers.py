from .models import User_Application_Detail
from rest_framework import serializers



class applicationInfoSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User_Application_Detail
        fields = "__all__"
