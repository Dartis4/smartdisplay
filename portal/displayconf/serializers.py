#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

from rest_framework import serializers

from .models import API


class ApiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = API
        fields = ['id', 'name', 'base_address', 'format', 'params', 'token', 'switch_display_zones']
