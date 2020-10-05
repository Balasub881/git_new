from django.contrib.auth import logout
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
import json


from .models import UploadImageTest
from .serializers import SignUpSerializer, LoginSerializer, ImageSerializer


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class LogoutView(GenericAPIView):
    def post(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

class ImageViewSet(ListAPIView):
    queryset = UploadImageTest.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        file = request.POST.get('file')
        image = UploadImageTest.objects.create(image=file)
        return HttpResponse(json.dumps({'message': "Your image Uploaded Successfully"}), status=200)

