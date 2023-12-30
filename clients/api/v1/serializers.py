from rest_framework import serializers
from clients.models import Client

class ClientResgisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('email', 'password', 'first_name', 'last_name', 'document')

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance  = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
