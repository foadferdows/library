from django.core.management.base import BaseCommand , CommandError
from books.models import *
from django.db import transaction
from django.contrib.auth import get_user_model
import random
import tqdm
import string



class Command(BaseCommand):

    help = "seed sample authors & books."

    def add_arguments(self, parser):
        parser.add_argument("--all", type=int , default = 6 , help="How many authors?")
        # parser.add_argument("--books", type=int , default = 20, help="How many books?")
        # parser.add_argument("--users", type=int , default = 3, help="How many users?")
        # parser.add_argument("--favs", type=int , default = 2, help="How many favs?")


    def handle(self,*args , **options):
        author_n = options["all"]
        users_n = options["all"]
        books_n = options["all"]
        favs_n = options["all"]

        if author_n < 0 or books_n < 0 or users_n < 0 or favs_n < 0:
            raise CommandError("Counts must be non-negative.")
        

        User = get_user_model()

        with transaction.atomic():
            users = []
            for i in  range(users_n):
                username = f"user{i+1}"
                email = f"{username}@foad.com"
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults = {"email":email , "is_staff":False , "is_active":True}
                )
                if created:
                    user.set_password("password")
                    user.save()
                users.append(user)
            
            authors = []
            for i in  range(author_n):
                a = Author.objects.create(name = f"Author {i+1}"
                                          , bio = "Seeded Author")
                authors.append(a)
            cat_codes = [c[0] for c in CATEGORY_CHOICES]
            def rand_title():
                return "Book "+ "".join(random.choices(string.ascii_uppercase , k=5))
            
            books = []
            for i in  range(books_n):
                book= Book.objects.create(title=rand_title(),
                                       author=random.choice(authors),
                                       category = random.choice(cat_codes),
                                       price=random.randint(100,300),
                                       description="Seeded")
                books.append(book)

            favorites_to_create = []
            for u in  users:
                k = min(favs_n, len(books))
                if k <= 0:
                    continue
                for book_id in random.sample(books, k):
                    # self.stdout.write(self.style.NOTICE(f"user {user} , book_id {book_id.id}  "))
                    fav = Favorite.objects.create(user=u, book_id=book_id.id)
            
                favorites_to_create.append(fav)


        self.stdout.write(self.style.NOTICE(f"Seeding : Users {users_n} ,  {author_n} Authors, {books_n} books , {favs_n} favs"))

        self.stdout.write(self.style.SUCCESS("Done."))