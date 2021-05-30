from rest_framework import serializers
from user.models import User
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from socialaccount.models import SocialAccount
from common.serializers import NetworkSerializer
from django.utils import dateparse


def convert_to_km(distance):
    # print(distance)
    return round(float(distance.replace("m", "")) / 1000, 2)


class UserSerializer(serializers.ModelSerializer):
    # longitude = serializers.SerializerMethodField(method_name='calculate_longitude')
    # latitude = serializers.SerializerMethodField(method_name='calculate_latitude')
    raw_distance = serializers.CharField(read_only=True)
    distance = serializers.SerializerMethodField(method_name="calculate_distance")
    age = serializers.SerializerMethodField(method_name="calculate_age")

    networks = serializers.SerializerMethodField(method_name="calculate_networks")

    class Meta:
        fields = (
            "id",
            "username",
            "profession",
            "first_name",
            "last_name",
            "phone",
            "email",
            "bio",
            "birthday",
            "avatar",
            "city",
            "longitude",
            "latitude",
            "raw_distance",
            "distance",
            "age",
            "networks"
            # "distance2"
        )
        model = User

    def calculate_age(self, instance):
        if instance.birthday is not None and instance.birthday != "":
            from datetime import date, datetime

            print("the date is " + str(instance.birthday))
            today = date.today()
            # born = datetime.strftime(instance.birthday, "%Y-%m-%d")
            born = dateparse.parse_date(str(instance.birthday))
            return (
                today.year
                - born.year
                - ((today.month, today.day) < (born.month, born.day))
            )
        return ""

    def calculate_networks(self, instance):
        # Get all social accounts
        socialaccounts = SocialAccount.objects.filter(user__id=instance.pk)

        if socialaccounts is not None:
            return NetworkSerializer(socialaccounts, many=True).data
        return ""

    def calculate_distance(self, instance):
        if hasattr(instance, "raw_distance"):
            # return str(instance.distance)
            # print(instance.raw_distance)
            if instance.raw_distance is not None:
                distance = str(instance.raw_distance)
                return str(convert_to_km(distance))
        return None

    # def calculate_longitude(self, instance):
    # return  instance.dob.year
    # return -123

    # def calculate_latitude(self, instance):
    # return  instance.dob.year
    # return -124


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone",
            "password",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"required": False, "allow_null": True},
            "phone": {"required": False, "allow_null": True},
            "first_name": {"required": False, "allow_null": True},
            "last_name": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        counted = str(User.objects.count() + 1)
        user = User.objects.create_user(
            username=validated_data.get("username", counted),
            email=validated_data["email"],
            phone=validated_data.get("phone", counted),
            password=validated_data["password"],
            first_name=validated_data.get("first_name", counted),
            last_name=validated_data.get("last_name", counted),
        )
        return user
        # user = authenticate(username=user.email, password=user.password)
        # if user is not None:
        # return user
        # raise serializers.ValidationError("Unable to log in with provided credentials.")


class SignInSerializer(serializers.Serializer):
    emailOrPhone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data["emailOrPhone"], password=data["password"])
        if user is not None:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate(self, data):
        user = User.objects.get(email=data["email"])
        if user is not None:
            return user
        raise serializers.ValidationError("Email doesn't exists.")


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()


class UserUpdateSerializer(serializers.Serializer):
    user = UserSerializer()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()