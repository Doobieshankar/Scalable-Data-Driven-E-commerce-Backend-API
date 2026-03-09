from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, LoginSerializer

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "status": True,
                "message": "User registered successfully",
                "data": {
                    "email": user.email,
                    "role": user.role,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "status": True,
                "message": "Login successful",
                "data": serializer.validated_data,
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(APIView):
    def get(self, request):
        user = request.user
        return Response(
            {
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
            }
        )