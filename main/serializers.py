from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Education, Skill


# ---------------------------------------------------------------------------
# Education
# ---------------------------------------------------------------------------
class EducationSerializer(serializers.ModelSerializer):
    is_ongoing = serializers.BooleanField(read_only=True)
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = [
            "id",
            "institution_name",
            "degree",
            "location",
            "maps_url",
            "logo",
            "start_year",
            "end_year",
            "is_ongoing",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id", "is_ongoing"]

    def validate_institution_name(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Institution name cannot be empty.")
        return value

    def validate_degree(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Degree cannot be empty.")
        return value

    def validate_location(self, value):
        if value:
            return strip_tags(value).strip()
        return ""

    def validate_logo(self, value):
        if value:
            return strip_tags(value).strip()
        return ""

    def validate(self, data):
        start_year = data.get("start_year")
        end_year = data.get("end_year")

        # In partial updates (PATCH), retrieve existing start_year if not provided
        if self.instance:
            if start_year is None:
                start_year = self.instance.start_year
            if end_year is None and "end_year" not in data:
                end_year = self.instance.end_year

        if start_year is not None and end_year is not None and end_year < start_year:
            raise serializers.ValidationError({"end_year": "End year cannot be before start year."})
        return data

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return obj.starred_by.filter(pk=request.user.pk).exists()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


# ---------------------------------------------------------------------------
# Skill
# ---------------------------------------------------------------------------
class SkillSerializer(serializers.ModelSerializer):
    percentage = serializers.FloatField(read_only=True)
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = [
            "id",
            "category",
            "name",
            "score",
            "order",
            "percentage",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id", "percentage"]

    def validate_name(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Skill name cannot be empty.")
        return value

    def validate_score(self, value):
        if value is not None and not (0 <= float(value) <= 10):
            raise serializers.ValidationError("Score must be between 0 and 10.")
        return value

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return obj.starred_by.filter(pk=request.user.pk).exists()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())
