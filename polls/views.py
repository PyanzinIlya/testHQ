from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from polls.models import User, Product, Lesson, ProductAccess
from polls.serializers import UserSerializer, ProductSerializer, LessonSerializer, ProductAccessSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('lessons').select_related("owner")
    serializer_class = ProductSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects
    serializer_class = LessonSerializer


class UserLessonsViewSet(mixins.ListModelMixin , GenericViewSet):
    queryset = Lesson.objects
    serializer_class = LessonSerializer
    # filterset_class = LessonFilter


class ProductAccessViewSet(viewsets.ModelViewSet):
    queryset = ProductAccess.objects
    serializer_class = ProductAccessSerializer
