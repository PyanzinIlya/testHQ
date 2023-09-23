from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from polls.models import User, Product, Lesson, ProductAccess, UserLessonProgress
from polls.serializers import UserSerializer, ProductSerializer, LessonSerializer, ProductAccessSerializer, \
    LessonProgressSerializer, ProductStatisticsSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.prefetch_related('lessons').select_related("owner")
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.queryset.filter(product_access__user=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects
    serializer_class = LessonSerializer


class UserLessonsViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects
    serializer_class = LessonSerializer
    # filterset_class = LessonFilter


class ProductAccessViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProductAccess.objects
    serializer_class = ProductAccessSerializer


class UserLessonProgressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserLessonProgress.objects
    serializer_class = LessonProgressSerializer


class ProductStatisticsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects
    serializer_class = ProductStatisticsSerializer
