from django.contrib import admin
from .models import User, Character, Planet, Vehicle, FavoriteCharacter, FavoritePlanet, FavoriteVehicle


admin.site.register(User)
admin.site.register(Character)
admin.site.register(Planet)
admin.site.register(Vehicle)
admin.site.register(FavoriteCharacter)
admin.site.register(FavoritePlanet)
admin.site.register(FavoriteVehicle)