from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    PasswordChangeSerializer,
)


@extend_schema(
    tags=["Accounts"],
    summary="Register new user",
    description="Create a new user account in the system.",
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            response=UserSerializer,
            description="User registered successfully.",
        ),
        400: OpenApiResponse(
            description="Validation error.",
        ),
    },
)
class RegisterAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                {
                    "message": "Registration successful.",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(
    tags=["Accounts"],
    summary="User login",
    description=(
        "Authenticate user using email and password "
        "and return JWT tokens."
    ),
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            description=(
                "Login successful. Returns JWT access "
                "and refresh tokens."
            ),
        ),
        401: OpenApiResponse(
            description="Invalid email or password.",
        ),
    },
)
class LoginAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        User = get_user_model()

        try:

            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(
                {
                    "message": "Invalid email or password."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(password):

            return Response(
                {
                    "message": "Invalid email or password."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Accounts"],
    summary="Get current user",
    description="Returns authenticated user's information.",
    responses={
        200: OpenApiResponse(
            description="Authenticated user information.",
        ),
        401: OpenApiResponse(
            description="Authentication credentials were not provided.",
        ),
    },
)
class CurrentUserAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(
            {
                "is_authenticated": (
                    request.user.is_authenticated
                ),
                "user": str(request.user),
                "auth": str(request.auth),
                "headers": {
                    "Authorization": request.headers.get(
                        "Authorization"
                    ),
                },
            }
        )


@extend_schema(
    tags=["Accounts"],
    summary="Change password",
    description="Change password for authenticated user.",
    request=PasswordChangeSerializer,
    responses={
        200: OpenApiResponse(
            description="Password changed successfully.",
        ),
        400: OpenApiResponse(
            description="Validation error.",
        ),
        401: OpenApiResponse(
            description="Authentication credentials were not provided.",
        ),
    },
)
class PasswordChangeAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = PasswordChangeSerializer(
            data=request.data,
            context={
                "request": request
            },
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = request.user

        user.set_password(
            serializer.validated_data["new_password"]
        )

        user.save()

        return Response(
            {
                "message": "Password changed successfully."
            },
            status=status.HTTP_200_OK,
        )