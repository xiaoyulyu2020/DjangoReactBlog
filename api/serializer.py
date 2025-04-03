from http.client import responses

from rest_framework import serializers
from api.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    """
    we want return the ProfileSerializer.data looks like:
    {
        user: UserSerializer.data
        ...
    }
    """
    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        """
        Customize the serialized output of the Profile model.
        super() call once the serialized output of the Profile model
        exp:
        profile_models = Profile.objects.all()
        profile_serializer = ProfileSerializer(profile_models, many=True)
        return : profile_serializer with user = UserSerializer.data
        """
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation

class CategorySerializer(serializers.ModelSerializer):

    # automatically looks for a method in the serializer class using a naming convention.
    # call fn: get_post_count
    post_count = serializers.SerializerMethodField()

    def get_post_count(self, category):
        return category.post_set.count()
        #post_set relies on the class, if the class name change then *_set will be changed

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'image',
            'slug',
            'post_count'
        ]
    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3