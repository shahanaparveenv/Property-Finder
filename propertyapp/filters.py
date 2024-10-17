import django_filters
from django import forms
from django_filters import CharFilter

from propertyapp.models import Property


class LocationFilter(django_filters.FilterSet):
    place = CharFilter(label="", lookup_expr="icontains", widget=forms.TextInput(attrs={
        'placeholder':'Search Location', 'class':'form-control'}))

    class Meta:
        model = Property
        fields = ('place',)
