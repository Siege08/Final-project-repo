from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .serializers import RegisterSerializer, PostSerializer, CommentSerializer
from .models import Post, Comment
from .utils import rate_limit

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    @rate_limit
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    @rate_limit
    def get(self, request):
        return Response({'message': 'Authenticated access granted'})

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    @rate_limit
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @rate_limit
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @rate_limit
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @rate_limit
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @rate_limit
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @rate_limit
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

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

    @rate_limit
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @rate_limit
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @rate_limit
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @rate_limit
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @rate_limit
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @rate_limit
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

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
