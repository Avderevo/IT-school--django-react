from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('status',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'id', 'email', 'is_active', 'profile')


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('token', 'username', 'password', 'email')


