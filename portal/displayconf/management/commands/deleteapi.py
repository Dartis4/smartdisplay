#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Removes an api from the database'

    def handle(self, *args, **options):
        self.stdout.write("This command is not implemented yet.")

