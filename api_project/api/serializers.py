from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author']
        # Or fields = '__all__' to include all fields


class CustomSerializer(serializers.Serializer):
    net_worth = serializers.SerializerMethodField()

    def get_net_worth(self, obj):
        return 10.23 * obj.net_worth