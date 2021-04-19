"""
Services for views
"""
from .models import UserFollows
from .models import Ticket
from .models import Review
from django.db.models import Value, Q
from django.db.models import CharField
from itertools import chain
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import models
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .forms import ReviewForm
from .forms import TicketForm
from .forms import LoginForm
from .forms import RegistrationForm
from .forms import SubsriptionForm


def service_ticket_review(id_ticket=None):
    """
    Function creating a list containing all reviews objects
    or review object of a ticket
    """
    ticket_review = [
        review.ticket for review in Review.objects.all()]
    if id_ticket:
        ticket = Ticket.objects.get(pk=id_ticket)
        if ticket in ticket_review:
            return ticket
    else:
        return ticket_review


def service_login_registration(request, registration=False):
    """
    Fonction of creating a user account
    or connecting an account
    """
    if registration:
        form = RegistrationForm(request.POST)
    else:
        form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        if registration:
            models.User.objects.create_user(
                username=username, password=password)
        else:
            userlogin = authenticate(
                request, username=username, password=password)
            login(request, userlogin)
    return form


def service_posts(request, followers=False):
    """
    Post list creation function
    """
    users = []
    for user in UserFollows.objects.filter(user=request.user):
        users.append(user.followed_user)
    users.append(request.user)
    if followers:
        ticket = Ticket.objects.filter(user__in=users)
        review = Review.objects.filter(
            Q(ticket__in=ticket) | Q(user__in=users))

    else:
        ticket = Ticket.objects.filter(user=request.user)
        review = Review.objects.filter(user=request.user)
    ticket = ticket.annotate(content_type=Value('TICKET', CharField()))
    review = review.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(
        chain(review, ticket), key=lambda post: post.time_created,
        reverse=True)
    return posts


def service_followed_users(request):
    """
    Function that returns the list of followed users
    """
    followed = []
    followed_users_list = UserFollows.objects.filter(
        user=request.user)
    followed_by_list = UserFollows.objects.filter(
        followed_user=request.user)
    followed_users_list = followed_users_list.annotate(
        content_type=Value('FOLLOWED_USER', CharField()))
    for user in followed_users_list:
        followed.append(user)
    followed_by_list = followed_by_list.annotate(
        content_type=Value('FOLLOWED_BY', CharField()))
    for user in followed_by_list:
        followed.append(user)
    return followed


def service_save_review(request, instance_ticket, instance_review):
    """
    Save review function
    """
    review_form = ReviewForm(request.POST, instance=instance_review)
    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.ticket = instance_ticket
        review.user = request.user
        review.save()
    return review_form


def service_save_ticket(request,
                        instance_ticket,
                        instance_review=None,
                        review=False):
    """
    Save ticket function
    """
    ticket_form = TicketForm(request.POST, instance=instance_ticket)
    if ticket_form.is_valid():
        ticket = ticket_form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        if review:
            service_save_review(request, ticket, instance_review)
    return ticket_form


def service_delete(request, model, id_model):
    """
    Object deletion function
    """
    delete_model = get_object_or_404(model, pk=id_model)
    if delete_model.user == request.user:
        delete_model.delete()
    else:
        pass


def service_get_instance(request, model, id_model, review=False):
    """
    Function for retrieving an instance of an object
    """
    if id_model is not None:
        if model == Review:
            try:
                instance = Review.objects.get(ticket=id_model)
                if review and instance.user != request.user:
                    instance = False
            except Review.DoesNotExist:
                instance = None
        else:
            instance = get_object_or_404(model, pk=id_model)
            if review is False and instance.user != request.user:
                instance = False
    else:
        instance = None
    return instance


def service_subscription(request):
    """
    Add user follow-up function
    """
    form = SubsriptionForm(request.POST)
    if form.is_valid():
        user = form.cleaned_data['username']
        user_follow = models.User.objects.get(username=user)
        if user_follow == request.user:
            return SubsriptionForm()
        try:
            user_follow = UserFollows.objects.create(
                user=request.user, followed_user=user_follow)
            user_follow.save()
        except IntegrityError as e:
            if 'unique constraint' in e.args:
                pass
    return form


def service_unsubscribe_user(request, id_user):
    """
    Follow-up user deletion function
    """
    followed_user = get_object_or_404(UserFollows, pk=id_user)
    if followed_user.user == request.user:
        followed_user.delete()
    else:
        pass
