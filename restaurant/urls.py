from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, MenuViewSet, VoteViewSet


app_name = 'restaurant'

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'menus', MenuViewSet, basename='menu')
router.register(r'votes', VoteViewSet, basename='vote')

urlpatterns = [
    path('', include(router.urls)),
    path('menus/today/', MenuViewSet.as_view({'get': 'get_today_menu'})),
    path('menus/today-votes/', MenuViewSet.as_view({'get': 'get_todays_votes'})),
]
