from rest_framework import serializers

from core.models import Tag, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'calories')
        

class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    # tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Recipe
        fields = (
            'id', 'date', 'tags'
        )
        # read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe detail"""
    tags = TagSerializer(many=True, read_only=True)