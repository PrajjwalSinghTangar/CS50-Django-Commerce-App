from xml.etree.ElementInclude import include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.auth_login, name='login'),
    path('register', views.auth_register, name='register'),
    path('logout', views.auth_logout, name='logout'),
    path('categories', views.categories, name='categories'),
    path('create_listing', views.create_listing, name='create_listing'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('watchlist_add/<str:key>', views.watchlist_add, name='watchlist_add'),
    path('watchlist_remove/<str:key>', views.watchlist_remove, name='watchlist_remove'),
    path('watchlist_item_remove/<str:key>', views.watchlist_item_remove, name='watchlist_item_remove'),
    path('listing/<str:key>', views.listing, name='listing'),
    path("bidding/<str:key>", views.bidding, name="bidding"),
    path("bid_close/<str:key>", views.bid_close, name="bid_close"),
]
