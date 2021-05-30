from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from user import serializers, models
from django.utils.crypto import get_random_string
from rest_framework import viewsets
from user.models import User
from common.permissions import IsOwnerOrReadOnly, IsOwnerOfEmail
from rest_framework import viewsets, permissions

from django.contrib.gis.geos import Point, fromstr

from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from common.mailer import sendMail


class SignUpAPI(generics.GenericAPIView):
    serializer_class = serializers.SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": serializers.UserSerializer(user).data,
                #'refresh': str(refresh),
                "access": str(refresh.access_token),
            }
        )


class SignInAPI(generics.GenericAPIView):
    serializer_class = serializers.SignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": serializers.UserSerializer(user).data,
                #'refresh': str(refresh),
                "access": str(refresh.access_token),
            }
        )


class ResetPasswordAPI(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        generated_password = get_random_string()
        user.set_password(generated_password)
        user.save()

        body = "Your new password is: " + generated_password

        # send_mail(serializer.data['email'], body)

        sendMail(
            "blog@oktocode.com",
            serializer.data["email"],
            "Réinitialisation de mot de passe",
            body,
        )

        return Response(
            {
                "message": "check your email",
            }
        )


class UpdateProfilAPI(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        return Response(
            serializers.UserSerializer(user).data,
        )

    def put(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        user = User.objects.get(id=request.user.id)
        # update user
        # for attr, value in serializer.validated_data.items():
        for attr, value in request.data.items():
            setattr(user, attr, value)
            user.save()

        return Response(
            serializers.UserSerializer(user).data,
        )


class ChangePasswordAPI(generics.GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=request.user.id)

        print(user)

        # user = serializer.validated_data
        user.set_password(request.data["password"])
        user.save()

        return Response(
            {
                "message": "your new password is set",
            }
        )


from rest_framework import generics


class ProfileViewSetDeprecated(generics.RetrieveUpdateDestroyAPIView):
    # queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    # filterset_class = filters.SocialAccountFilter
    # filter_fields = ["email", "phone", "updated_date"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset

    # def perform_update(self, serializer):
    # serializer.save(user=self.request.user)


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    # filterset_class = filters.SocialAccountFilter
    # filter_fields = ["email", "phone", "updated_date"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = User.objects.all()
        long = self.request.query_params.get("long", None)
        lat = self.request.query_params.get("lat", None)
        if long is not None and lat is not None:
            longitude = long  # -80.191788
            latitude = lat  # 25.761681
            # longitude = -80.191788
            # latitude = 25.761681
            # user_location = Point(longitude, latitude, srid=4326)

            # user_location = fromstr("POINT(%s %s)" % (long, lat))
            user_location = fromstr(f"POINT({longitude} {latitude})", srid=4326)

            # queryset = queryset.filter(location__distance_lte=(user_location, D(km=7))) # D(mi=20)
            queryset = User.objects.annotate(
                raw_distance=Distance("location", user_location)
            ).order_by("raw_distance")
            # for q in queryset:
            # print(q.distance)
        if self.request.user is not None:
            return queryset.exclude(pk=self.request.user.id)
        return queryset

    # def perform_create(self, serializer):
    # serializer.save(user=self.request.user)

    # def perform_update(self, serializer):
    # long = request.data["long"]
    # lat = long = request.data["lat"]
    # location = fromstr("POINT(%s %s)" % (long, lat))
    # serializer.save(location=location)
    # return super().perform_update(serializer)
