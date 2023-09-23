from rest_framework import routers

from polls.views import UserViewSet, ProductViewSet, LessonViewSet, ProductAccessViewSet, UserLessonProgressViewSet, \
    ProductStatisticsViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename='user')

router.register('statistics', ProductStatisticsViewSet, basename='stats')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'user-product-access', ProductAccessViewSet, basename='user-product-access')
router.register(r'lesson-progress', UserLessonProgressViewSet, basename='lesson-progress')
urlpatterns = router.urls
