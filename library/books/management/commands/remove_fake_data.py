from django.core.management.base import BaseCommand , CommandError
from django.db import transaction
from django.db.models import Q , Count
from django.utils import timezone
from datetime import timedelta

from books.models import *

class Command(BaseCommand):
    help = "to remove all records in DB"

    def add_arguments(self, parser):
        parser.add_argument("--all" , action="store_true" , help="to remove all recpords")

    def favorite_qs(self):
        return Favorite.objects.all()

    def book_qs(self):
        return Book.objects.all()
    
    def author_qs(self):
        return Author.objects.all()
    
    def handle(self, *args, **options):
        with transaction.atomic():
            
            books = self.book_qs()
            self.stdout.write(f"[Books] matched: {books.count()}")
            deleted, _ = books.delete()
            self.stdout.write(f"[Books] Deleted: {deleted}")

            authors = self.author_qs()
            self.stdout.write(f"[Author] matched: {authors.count()}")
            deleted, _ = authors.delete()
            self.stdout.write(f"[Author] Deleted: {deleted}")

            favorits = self.favorite_qs()
            self.stdout.write(f"[Favorits] matched: {favorits.count()}")
            deleted, _ = favorits.delete()
            self.stdout.write(f"[Favorits] Deleted: {deleted}")





    
    