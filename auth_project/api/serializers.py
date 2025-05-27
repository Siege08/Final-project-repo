from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'photo')

    def validate_photo(self, value):
        if value:
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError('Image size should not exceed 2MB.')
            valid_types = ['image/jpeg', 'image/png', 'image/webp']
            if value.content_type not in valid_types:
                raise serializers.ValidationError('Only JPEG, PNG, and WebP images are allowed.')
        return value

    def create(self, validated_data):
        photo = validated_data.pop('photo', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        if photo:
            # Optional: Crop to 1:1 aspect ratio
            image = Image.open(photo)
            min_side = min(image.size)
            left = (image.width - min_side) / 2
            top = (image.height - min_side) / 2
            right = (image.width + min_side) / 2
            bottom = (image.height + min_side) / 2
            image = image.crop((left, top, right, bottom))
            buffer = BytesIO()
            image_format = 'JPEG' if image.format == 'JPEG' else 'PNG'
            image.save(buffer, format=image_format)
            file_name = photo.name
            user.photo.save(file_name, ContentFile(buffer.getvalue()), save=True)
        return user

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
