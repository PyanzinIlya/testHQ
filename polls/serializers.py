from django.db.models import Sum
from rest_framework import serializers

from polls.models import User, Product, Lesson, ProductAccess, UserLessonProgress


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username']


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserLessonProgress

        fields = ['id', 'lesson_completed', 'time_viewed', 'last_time_viewed', 'lesson']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        instance = super().create(validated_data)
        return self.save_completed(instance)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return self.save_completed(instance)



    def save_completed(self, instance):
        if instance.time_viewed >= instance.lesson.video_duration * 0.8:
            instance.lesson_completed = True
            instance.save()
        return instance


class LessonSerializer(serializers.ModelSerializer):
    progress = LessonProgressSerializer(source='user_progress')

    class Meta:
        model = Lesson
        fields = ['id', 'video_duration', 'title', 'video_url', 'progress']


class ProductSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    lessons = LessonSerializer(many=True, required=False)
    lesson_ids = serializers.ListSerializer(child=serializers.IntegerField(), write_only=True)

    def create(self, validated_data):
        lessons = validated_data.pop('lesson_ids')
        instance = super().create(validated_data)
        instance.lessons.set(lessons)
        return instance

    def update(self, instance, validated_data):
        lessons = validated_data.pop('lesson_ids')
        instance = super().update(instance, validated_data)
        instance.lessons.set(lessons)
        return instance

    class Meta:
        model = Product
        fields = ['id', 'owner_id', 'title', 'lessons', 'lesson_ids', 'owner']


class ProductAccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAccess
        fields = ['id', 'user', 'product']


class ProductStatisticsSerializer(serializers.ModelSerializer):
    lessons_viewed = serializers.SerializerMethodField(method_name='lessons_count')
    time_spend = serializers.SerializerMethodField(method_name='total_time_spent')
    students_count = serializers.SerializerMethodField(method_name='total_students')
    product_efficiency = serializers.SerializerMethodField(method_name='get_product_efficiency')


    def lessons_count(self, product):
        return product.lessons.filter(user_progress__lesson_completed=True).count()

    def total_time_spent(self, product):
        return product.lessons.aggregate(total=Sum('user_progress__time_viewed'))['total']

    def total_students(self, product):
        return product.product_access.count()

    def get_product_efficiency(self, product):
        return product.product_access.count() / User.objects.count() * 100

    class Meta:
        model = Product
        fields = ['id', 'title', 'owner', 'lessons_viewed', 'time_spend', 'students_count', 'product_efficiency']
