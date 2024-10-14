from rest_framework import serializers

from .models import (
    Restaurant,
    Menu,
    Vote,
)


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'day', 'dishes', 'vote_count']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'employee', 'menu', 'vote_time']
        read_only_fields = ['employee', 'vote_time']
