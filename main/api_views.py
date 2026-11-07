from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Achievement, Certification, Education, Experience, Skill
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import (
    AchievementSerializer,
    CertificationSerializer,
    EducationSerializer,
    ExperienceSerializer,
    SkillSerializer,
)


# ---------------------------------------------------------------------------
# Education
# ---------------------------------------------------------------------------
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_list(request):
    if request.method in ("GET", "HEAD"):
        educations = Education.objects.prefetch_related("starred_by").order_by("-start_year", "institution_name")
        q = (
            request.query_params.get("search", "").strip()
            or request.query_params.get("institution_name", "").strip()
            or request.query_params.get("q", "").strip()
        )
        if q:
            educations = educations.filter(
                Q(institution_name__icontains=q) |
                Q(degree__icontains=q) |
                Q(location__icontains=q)
            )
        serializer = EducationSerializer(educations, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = EducationSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_detail(request, education_id):
    education = get_object_or_404(
        Education.objects.prefetch_related("starred_by"), pk=education_id
    )
    if request.method in ("GET", "HEAD"):
        serializer = EducationSerializer(education, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = EducationSerializer(
        education,
        data=request.data,
        partial=(request.method == "PATCH"),
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def education_star(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    if education.starred_by.filter(pk=request.user.pk).exists():
        education.starred_by.remove(request.user)
    else:
        education.starred_by.add(request.user)
    serializer = EducationSerializer(education, context={"request": request})
    return Response(serializer.data)


# ---------------------------------------------------------------------------
# Skill
# ---------------------------------------------------------------------------
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def skill_list(request):
    if request.method in ("GET", "HEAD"):
        skills = Skill.objects.prefetch_related("starred_by").order_by("category", "order", "-score")
        q = (
            request.query_params.get("search", "").strip()
            or request.query_params.get("name", "").strip()
            or request.query_params.get("q", "").strip()
        )
        if q:
            skills = skills.filter(
                Q(name__icontains=q) | Q(category__icontains=q)
            )
        serializer = SkillSerializer(skills, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = SkillSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def skill_detail(request, skill_id):
    skill = get_object_or_404(Skill.objects.prefetch_related("starred_by"), pk=skill_id)

    if request.method in ("GET", "HEAD"):
        serializer = SkillSerializer(skill, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = SkillSerializer(
        skill,
        data=request.data,
        partial=(request.method == "PATCH"),
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def skill_star(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    if skill.starred_by.filter(pk=request.user.pk).exists():
        skill.starred_by.remove(request.user)
    else:
        skill.starred_by.add(request.user)
    serializer = SkillSerializer(skill, context={"request": request})
    return Response(serializer.data)


# ---------------------------------------------------------------------------
# Experience
# ---------------------------------------------------------------------------
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    if request.method in ("GET", "HEAD"):
        experiences = Experience.objects.prefetch_related("starred_by").order_by("-started_at")
        q = (
            request.query_params.get("search", "").strip()
            or request.query_params.get("title", "").strip()
            or request.query_params.get("q", "").strip()
        )
        category_query = request.query_params.get("category", "").strip()
        if q:
            experiences = experiences.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(category__icontains=q)
            )
        if category_query:
            experiences = experiences.filter(category__icontains=category_query)

        serializer = ExperienceSerializer(experiences, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = ExperienceSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"), pk=experience_id
    )
    if request.method in ("GET", "HEAD"):
        serializer = ExperienceSerializer(experience, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ExperienceSerializer(
        experience,
        data=request.data,
        partial=(request.method == "PATCH"),
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)
    serializer = ExperienceSerializer(experience, context={"request": request})
    return Response(serializer.data)


# ---------------------------------------------------------------------------
# Achievement
# ---------------------------------------------------------------------------
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def achievement_list(request):
    if request.method in ("GET", "HEAD"):
        achievements = Achievement.objects.prefetch_related("starred_by").order_by("-year")
        q = (
            request.query_params.get("search", "").strip()
            or request.query_params.get("title", "").strip()
            or request.query_params.get("q", "").strip()
        )
        category_query = request.query_params.get("category", "").strip()
        if q:
            achievements = achievements.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(category__icontains=q)
            )
        if category_query:
            achievements = achievements.filter(category__icontains=category_query)

        serializer = AchievementSerializer(achievements, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = AchievementSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def achievement_detail(request, achievement_id):
    achievement = get_object_or_404(
        Achievement.objects.prefetch_related("starred_by"), pk=achievement_id
    )
    if request.method in ("GET", "HEAD"):
        serializer = AchievementSerializer(achievement, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        achievement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = AchievementSerializer(
        achievement,
        data=request.data,
        partial=(request.method == "PATCH"),
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def achievement_star(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    if achievement.starred_by.filter(pk=request.user.pk).exists():
        achievement.starred_by.remove(request.user)
    else:
        achievement.starred_by.add(request.user)
    serializer = AchievementSerializer(achievement, context={"request": request})
    return Response(serializer.data)

# ---------------------------------------------------------------------------
# Certification
# ---------------------------------------------------------------------------
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def certification_list(request):
    if request.method in ("GET", "HEAD"):
        certifications = Certification.objects.prefetch_related("starred_by").order_by("title")
        q = (
            request.query_params.get("search", "").strip()
            or request.query_params.get("title", "").strip()
            or request.query_params.get("q", "").strip()
        )
        if q:
            certifications = certifications.filter(
                Q(title__icontains=q) |
                Q(issuer__icontains=q) |
                Q(description__icontains=q)
            )

        serializer = CertificationSerializer(certifications, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = CertificationSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def certification_detail(request, certification_id):
    certification = get_object_or_404(
        Certification.objects.prefetch_related("starred_by"), pk=certification_id
    )
    if request.method in ("GET", "HEAD"):
        serializer = CertificationSerializer(certification, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        certification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = CertificationSerializer(
        certification,
        data=request.data,
        partial=(request.method == "PATCH"),
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def certification_star(request, certification_id):
    certification = get_object_or_404(Certification, pk=certification_id)
    if certification.starred_by.filter(pk=request.user.pk).exists():
        certification.starred_by.remove(request.user)
    else:
        certification.starred_by.add(request.user)
    serializer = CertificationSerializer(certification, context={"request": request})
    return Response(serializer.data)

