from rest_framework import serializers
from .models import User, Stopover, StopoverImage, StopoverCoords, StopoverLevel
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class StopoverCoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopoverCoords
        fields = ['latitude', 'longitude', 'height']


class StopoverLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopoverLevel
        fields = ['level_winter', 'level_summer', 'level_autumn', 'level_spring']


class StopoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopoverImage
        fields = ['data', 'title']


class StopoverSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    images = StopoverImageSerializer(many=True)
    coords = StopoverCoordsSerializer()
    level = StopoverLevelSerializer()
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Stopover
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        user, created = User.objects.get_or_create(email=user_data['email'], defaults=user_data)

        if not created:
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        coords = StopoverCoords.objects.create(**coords_data)
        level = StopoverLevel.objects.create(**level_data)
        stopover_obj = Stopover.objects.create(user=user, coords=coords, level=level, **validated_data)

        for image_data in images_data:
            StopoverImage.objects.create(stopover=stopover_obj, **image_data)

        return stopover_obj

    def validate_images(self, value):
        if not value:
            raise ValidationError("Должно быть хотя бы одно изображение.")
        return value

    def update(self, instance, validated_data):
        read_only_fields = ['email', 'fam', 'name', 'otc', 'phone']

        user_data = validated_data.get('user', {})
        for field in read_only_fields:
            if field in user_data and getattr(instance.user, field) != user_data[field]:
                raise serializers.ValidationError({field: "Это поле нельзя изменить."})

        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                if attr not in read_only_fields:
                    setattr(user, attr, value)
            user.save()

        images_data = validated_data.pop('images', None)
        if images_data:
            instance.images.all().delete()
            for image_data in images_data:
                StopoverImage.objects.create(stopover=instance, **image_data)

        coords_data = validated_data.pop('coords', None)
        if coords_data:
            coords = instance.coords
            for attr, value in coords_data.items():
                setattr(coords, attr, value)
            coords.save()

        level_data = validated_data.pop('level', None)
        if level_data:
            level = instance.level
            for attr, value in level_data.items():
                setattr(level, attr, value)
            level.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance