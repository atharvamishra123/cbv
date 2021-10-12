from rest_framework import serializers
from fifthapp.models import Snippet


# def title_length(value):
#     if len(value) < 5:
#         raise serializers.ValidationError("title can't be too short..")


class SnippetSerializer(serializers.ModelSerializer):
    len_title = serializers.SerializerMethodField()
    len_code = serializers.SerializerMethodField()
    class Meta:
        model = Snippet
        fields = "__all__"

    def get_len_title(self, object):
        return len(object.title)

    def get_len_code(self, object):
        return len(object.code)

    def validate(self, data):  # Object Level Validation
        if data['title'] == data['code']:
            raise serializers.ValidationError("title and description were not same..")
        else:
            return data

    def validate_title(self, value):  # Field Level Validation (we can use Validators instead)
        if len(value) < 5:
            serializers.ValidationError("title cant be too small..")
        else:
            return value

# class SnippetSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     # title = serializers.CharField(validators=[title_length])
#     code = serializers.CharField()
#
#     def create(self, validated_data):
#         print("create..")
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         print("update...")
#         instance.title = validated_data.get("title", instance.title)
#         instance.code = validated_data.get("code", instance.code)
#         instance.save()
#         return instance
#
#     def validate(self, data):  # Object Level Validation
#         if data['title'] == data['code']:
#             raise serializers.ValidationError("title and description were not same..")
#         else:
#             return data
#
#     def validate_title(self, value):  # Field Level Validation (we can use Validators instead)
#         if len(value) < 5:
#             serializers.ValidationError("title cant be too small..")
#         else:
#             return value
