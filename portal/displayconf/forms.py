#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

from django import forms
from .models import APIData, API


class NameEntryForm(forms.Form):
    class Meta:
        model = API
        fields = '__all__'


class APIForm(forms.ModelForm):
    class Meta:
        model = APIData
        fields = '__all__'
