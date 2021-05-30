import django_filters
from socialaccount.models import SocialAccount


class SocialAccountFilter(django_filters.FilterSet):
    class Meta:
        fields = {
            "identifier": ["exact", "icontains"],
            "updated_date": ["gte", "lte"],
            "network__id": ["exact"],
            "user__id": ["exact"],
        }
        model = SocialAccount
