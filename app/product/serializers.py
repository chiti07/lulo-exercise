from rest_framework import serializers

from core.models import Tag, Product


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'code', 'description', 'picture')
        read_only_fields = ('id',)


class ProductDetailSerializer(ProductSerializer):
    """"""
