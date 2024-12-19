# from django.shortcuts import render

# # Rest framework imports
# from rest_framework import generics  # Import generics for API views
# from rest_framework.permissions import AllowAny  # Import AllowAny permission to allow unrestricted access
# from rest_framework_simplejwt.views import TokenObtainPairView  # Import JWT view for token-based authentication

# from userauths.models import User, Profile  # Import User and Profile models
# from userauths.serializer import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer

# import random
# import shortuuid



# class MyTokenObtainPairView(TokenObtainPairView):
#     """
#     Custom token view that returns an additional user-specific data
#     in the JWT token, such as username, email, and vendor_id.
#     """
#     serializer_class = MyTokenObtainPairSerializer


# class RegisterView(generics.CreateAPIView):
#     """
#     View to handle user registration. This view allows any user
#     to register by creating a new user instance.
#     """
#     queryset = User.objects.all()  # Define the queryset for the view
#     permission_classes = (AllowAny,)  # Allow unrestricted access to the registration endpoint
#     serializer_class = RegisterSerializer  # Use the RegisterSerializer to validate and create a new user


# def generate_otp():
#     uuid_key = shortuuid.uuid()
#     unique_key = uuid_key[:6]
#     return unique_key  


# class PasswordEmailVerify(generics.RetrieveAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = UserSerializer
    
#     def get_object(self):
#         email = self.kwargs['email']
#         user = User.objects.get(email=email)

#         if user:
#             user.otp = generate_otp()
#             user.save()

#             uidb64 = user.pk
#             otp = user.otp

#             link = f"http://localhost:5173/create-new-password?otp={otp}&uidb64={uidb64}"

#             print("link =====", link)

#             # send Email
#         return user
    



# class PasswordChangeView(generics.CreateAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = UserSerializer
    
#     def create(self, request, *args, **kwargs):
#         payload = request.data
        
#         otp = payload['otp']
#         uidb64 = payload['uidb64']
#         reset_token = payload['reset_token']
#         password = payload['password']



#         user = User.objects.get(id=uidb64, otp=otp)
#         if user:
#             user.set_password(password)
#             user.otp = ""
#             user.reset_token = ""
#             user.save()

            
#             return Response( {"message": "Password Changed Successfully"}, status=status.HTTP_201_CREATED)
#         else:
#             return Response( {"message": "An Error Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from userauths.models import User, Profile
from userauths.serializer import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer
import random
import shortuuid
import base64
from django.core.exceptions import ObjectDoesNotExist

class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view that returns an additional user-specific data
    in the JWT token, such as username, email, and vendor_id.
    """
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    View to handle user registration. This view allows any user
    to register by creating a new user instance.
    """
    queryset = User.objects.all()  # Define the queryset for the view
    permission_classes = (AllowAny,)  # Allow unrestricted access to the registration endpoint
    serializer_class = RegisterSerializer  # Use the RegisterSerializer to validate and create a new user


def generate_otp():
    """Generates a 6-digit OTP using shortuuid."""
    uuid_key = shortuuid.uuid()
    unique_key = uuid_key[:6]
    return unique_key  


class PasswordEmailVerify(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    
    def get_object(self):
        email = self.kwargs['email']
        try:
            user = User.objects.get(email=email)
            if user:
                # Generate OTP and send it to the user
                user.otp = generate_otp()
                user.save()

                uidb64 = base64.urlsafe_b64encode(str(user.pk).encode()).decode()
                otp = user.otp
                link = f"http://localhost:5173/create-new-password?otp={otp}&uidb64={uidb64}"

                print("link =====", link)

                # send Email with the link here
            return user
        except User.DoesNotExist:
            raise Http404("User not found")


class PasswordChangeView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        payload = request.data
        
        otp = payload['otp']
        uidb64 = payload['uidb64']
        reset_token = payload['reset_token']
        password = payload['password']

        # Decode uidb64 to get the user id
        try:
            uid = base64.urlsafe_b64decode(uidb64).decode()
            user = User.objects.get(id=uid, otp=otp)

            if user:
                user.set_password(password)
                user.otp = ""  # Clear OTP after successful password reset
                user.reset_token = reset_token
                user.save()

                return Response({"message": "Password changed successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Invalid OTP or user"}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, ValueError):
            return Response({"message": "Invalid user or OTP"}, status=status.HTTP_400_BAD_REQUEST)
