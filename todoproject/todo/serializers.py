from rest_framework import serializers
from .models import Todo

class TestTodoSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    body = serializers.CharField()

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)

        return instance

    def validate_title(self, value):
        # Custom Validation
        if "$" in value:
            raise serializers.ValidationError('Error, title connot have the symbol $.')
        return value

    def validate_body(self, value):
        # Custom Validation
        if "$" in value:
            raise serializers.ValidationError('Error, body cannot have the symbol $.')
        return value

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo 
        fields = '__all__'
        read_only_fields = ('create_at', 'done_at', 'updated_at', 'deleted_at', )