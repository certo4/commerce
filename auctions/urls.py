from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-listing", views.new_listing, name="new_listing"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listings/<str:id>", views.listing, name="listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist_action/<str:id>", views.watchlist_action, name="watchlist_action"),
    path("close_listing/<str:id>", views.close_listing, name="close_listing"),
    path("categories", views.categories, name="categories"),
    path("category/<str:id>", views.category, name="category"),
    path("bid/<str:id>", views.bid, name="bid")
]
