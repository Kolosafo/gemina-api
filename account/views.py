from .models import User
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
# Create your views here.



@api_view(['POST'])
def register(request):
    data = request.data
    if User.objects.filter(email=data['email']):
        return Response("User with this email already exists", status=status.HTTP_409_CONFLICT)
    if data['password'] != data['password_confirm']:
        return Response("Passwords do not match", status=status.HTTP_400_BAD_REQUEST)
    data['username'] = data['email']
    
    serializer = UserSerializer(data=data)
    
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        # send_mail("Confirm Your Email", email_message, settings.EMAIL_HOST_USER, [
        #     data["email"]], fail_silently=False)
        return Response({"refresh":str(refresh), "access": access_token,"data":serializer.data, "status": status.HTTP_201_CREATED})
    else:
        print(serializer.errors)
        return Response({
            "errors": serializer.errors,
            "message": "An error occurred",
            "status": "error",
        })
        



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['username'] = user.username
        token['id'] = user.id
        token['first_name'] = user.first_name
        token['profile_picture'] = user.profile_picture
        token['last_name'] = user.last_name
        token['gender'] = user.gender
        token['learningPace'] = user.learningPace
        token['DOB'] = str(user.DOB)
        token['school_level'] = user.school_level
        token['grade_level'] = user.grade_level
        token['country'] = user.country
        
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.data
    try:
        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
                "data": serializer.data,
                "errors": None,
                "message": "succcess!",
                "status": status.HTTP_200_OK,
            })
    except Exception as e:
        return Response({
                "errors": str(e),
                "message": f"{e}",
                "status": status.HTTP_400_BAD_REQUEST,
            })
        