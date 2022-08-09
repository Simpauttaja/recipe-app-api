"""
Because of the file structure, Django will automatically detect this as management command
"""


from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        pass
