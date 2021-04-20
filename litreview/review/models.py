"""
Model management module for
migration into the database
"""
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    """
    Class of the Ticket model.
    The user will have to enter a title,
    a description and possibly an image
    """
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.URLField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    """
    Review model class.
    The user will have to enter
    a title (headline) and a description (body)
    """
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    """
    Class of the UserFollows model.
    The user will need to enter a user name
    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='following')
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='followed_by')

    class Meta:
        """
        Ensures we don't get multiple UserFollows instances
        for unique user-user_followed pairs
        """
        unique_together = ('user', 'followed_user')
