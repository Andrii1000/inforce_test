from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Restaurant, Menu, Vote
from .serializers import RestaurantSerializer, MenuSerializer, VoteSerializer
from user.models import Employee

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set today's date when creating a menu
        day = timezone.now().date()
        serializer.save(day=day)

    @action(detail=False, methods=['get'], url_path='today')
    def get_today_menu(self, request):
        # Get today's menus
        today = timezone.now().date()
        queryset = Menu.objects.filter(day=today)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='today-votes')
    def get_todays_votes(self, request):
        # Get today's menus along with vote counts
        today = timezone.now().date()
        queryset = Menu.objects.filter(day=today).annotate(vote_count=Count('vote'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Get the employee based on the authenticated user
        employee = get_object_or_404(Employee, user=self.request.user)

        # Validate menu_id from the request
        menu_id = self.request.data.get('menu')
        if not menu_id:
            return Response({"detail": "menu_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the menu exists and the employee has not already voted
        menu = get_object_or_404(Menu, id=menu_id)
        if Vote.objects.filter(employee=employee, menu=menu).exists():
            return Response({"detail": "You have already voted for this menu."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the vote with the employee and menu
        serializer.save(employee=employee, menu=menu)

