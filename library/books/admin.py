from django.contrib import admin
from .models import Author, Book, Favorite, user_extra

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "sex", "birth_date")
    search_fields = ("name", "bio")
    list_filter = ("country", "sex")

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "price", "published_date")
    search_fields = ("title", "description", "author__name")
    list_filter = ("category", "published_date")
    
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "date")
    search_fields = ("user__username", "book__title")

@admin.register(user_extra)
class UserExtraAdmin(admin.ModelAdmin):
    list_display = ("user_id", "sex", "nationalcode")
    search_fields = ("user_id__username", "nationalcode")
