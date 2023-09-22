from rest_framework import serializers

from polls.models import User, Product, Lesson, ProductAccess


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'video_duration', 'title', 'video_url']


class ProductSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    lessons = LessonSerializer(many=True, required=False)
    lesson_ids = serializers.ListSerializer(child=serializers.IntegerField(), write_only=True)

    def create(self, validated_data):
        lessons = validated_data.pop('lesson_ids')
        product = super().create(validated_data)
        product.lessons.set(lessons)
        return product

    def update(self, instance, validated_data):
        lessons = validated_data.pop('lesson_ids')
        product = super().update(instance, validated_data)
        product.lessons.set(lessons)
        return product

    class Meta:
        model = Product
        fields = ['id', 'owner_id', 'title', 'lessons', 'lesson_ids', 'owner']


class ProductAccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAccess
        fields = ['id', 'user', 'product']
