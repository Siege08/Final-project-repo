from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .serializers import RegisterSerializer, PostSerializer, CommentSerializer
from .models import Post, Comment

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Authenticated access granted'})

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if self.get_object().user != self.request.user:
            raise PermissionDenied('You do not have permission to edit this post.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('You do not have permission to delete this post.')
        instance.delete()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if self.get_object().user != self.request.user:
            raise PermissionDenied('You do not have permission to edit this comment.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('You do not have permission to delete this comment.')
        instance.delete()
