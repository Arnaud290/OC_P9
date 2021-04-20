"""
URL address routing module
for the review application
"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.userlogin, name='userlogin'),
    path('logout/', views.userlogout, name='userlogout'),
    path('registration/', views.registration, name='registration'),
    path('feed/', views.feed, name='feed'),
    path('subsription/', views.subscription, name='subscription'),
    path(
        'unsubscribeuser/<int:id_user>', views.unsubscribe_user,
        name='unsubscribe_user'),
    path('ticket/', views.ticket, name='ticket'),
    path('ticket/<int:id_ticket>', views.ticket, name='ticket'),
    path(
        'deleteticket/<int:id_ticket>', views.delete_ticket,
        name='delete_ticket'),
    path('review/', views.review, name='review'),
    path('review/<int:id_ticket>', views.review, name='review'),
    path(
        'deletereview/<int:id_review>', views.delete_review,
        name='delete_review'),
    path('posts/', views.posts, name='posts'),
]
