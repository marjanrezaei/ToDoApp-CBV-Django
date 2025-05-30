from rest_framework import serializers
from ...models import Task
from django.urls import reverse
from accounts.models import Profile

class TaskSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source='get_snippet')
    relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    absolute_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = ['id', 'author', 'title', 'description', 'snippet', 'completed', 'relative_url', 'absolute_url', 'created_at', 'updated_at'] 
        read_only_fields = ['author'] 
    
    def get_absolute_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(reverse('blog:api-v1:task-detail', kwargs={'pk': obj.pk}))
        return reverse('blog:api-v1:task-detail', kwargs={'pk': obj.pk})

    def to_representation(self, instance):
        request = self.context.get('request') 
        rep = super().to_representation(instance)
        if request and request.parser_context and request.parser_context.get('kwargs'):
            if request.parser_context['kwargs'].get('pk'):
                rep.pop('snippet', None)
                rep.pop('relative_url', None)
                rep.pop('absolute_url', None)
            else:
                rep.pop('description', None)
        return rep
    
    def create(self, validated_data):
        user = self.context.get('request').user
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to create a task.")
        
        validated_data['author'] = Profile.objects.get(user__id=user.id)
        return super().create(validated_data)
