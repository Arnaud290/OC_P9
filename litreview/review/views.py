from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import LoginForm
from .forms import RegistrationForm
from .forms import TicketForm
from .forms import ReviewForm
from .forms import SubsriptionForm
from .models import Ticket, Review
from .services import service_unsubscribe_user
from .services import service_followed_users
from .services import service_login_registration
from .services import service_posts
from .services import service_ticket_review
from .services import service_get_instance
from .services import service_save_ticket
from .services import service_delete
from .services import service_subscription
from .services import service_save_review


def index(request):
    return redirect('userlogin')


def userlogin(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = service_login_registration(request)
        if form.is_valid():
            return redirect('feed')
    else:
        form = LoginForm()
    return render(
        request, "review/login.html",
        {'form': form})


def userlogout(request):
    logout(request)
    return redirect('userlogin')


def registration(request):
    if request.method == 'POST':
        form = service_login_registration(
            request, registration=True)
        if form.is_valid():
            return redirect('userlogin')
    else:
        form = RegistrationForm()
    return render(
        request, "review/registration.html",
        {'form': form})


def feed(request):
    if request.user.is_authenticated:
        context = {
            'posts': service_posts(request, followers=True),
            'ticket_review': service_ticket_review(),
            'n': range(5)}
        return render(
            request, "review/feed.html",
            context)
    else:
        return redirect('userlogin')


def ticket(request, id_ticket=None):
    if request.user.is_authenticated:
        instance_ticket = service_get_instance(
            request, Ticket, id_ticket)
        if instance_ticket is False:
            return redirect('feed')
        if request.method == 'POST':
            ticket_form = service_save_ticket(
                request, instance_ticket)
            if ticket_form.is_valid():
                if id_ticket is not None:
                    return redirect('posts')
                else:
                    return redirect('feed')
            else:
                error = 'Lien URL non valide'
        else:
            error = False
            ticket_form = TicketForm(instance=instance_ticket)
        return render(
            request, "review/ticket.html",
            {'ticket_form': ticket_form, 'error': error})
    else:
        return redirect('userlogin')


def delete_ticket(request, id_ticket):
    if request.user.is_authenticated:
        service_delete(request, Ticket, id_ticket)
        return redirect(request.META.get('HTTP_REFERER'))


def subscription(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = service_subscription(request)
        else:
            form = SubsriptionForm()
        context = {
            'form': form,
            'followed': service_followed_users(request)
        }
        return render(
            request, "review/subscription.html",
            context)
    else:
        return redirect('userlogin')


def unsubscribe_user(request, id_user):
    if request.user.is_authenticated:
        service_unsubscribe_user(request, id_user)
        return redirect('subscription')


def review(request, id_ticket=None):
    if request.user.is_authenticated:
        instance_ticket = service_get_instance(
            request, Ticket, id_ticket,
            review=True)
        instance_review = service_get_instance(
            request, Review, id_ticket,
            review=True)
        if instance_review is False:
            return redirect('feed')
        ticket_form = TicketForm(instance=instance_ticket)
        review_form = ReviewForm(instance=instance_review)
        if request.method == 'POST':
            if id_ticket is not None:
                review_form = service_save_review(
                    request,
                    instance_ticket=instance_ticket,
                    instance_review=instance_review)
                if instance_review is None:
                    return redirect('feed')
                else:
                    return redirect('posts')
            else:
                ticket_form = service_save_ticket(
                    request,
                    instance_ticket=instance_ticket,
                    instance_review=instance_review,
                    review=True)
                if ticket_form.is_valid():
                    return redirect('feed')
                else:
                    error = 'Lien URL non valide'
        else:
            error = False
        context = {
            'ticket_form': ticket_form,
            'review_form': review_form,
            'error': error}
        return render(
            request, "review/review.html", context)
    else:
        return redirect('userlogin')


def delete_review(request, id_review):
    if request.user.is_authenticated:
        service_delete(
            request, Review, id_review)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        pass


def posts(request):
    if request.user.is_authenticated:
        context = {'posts': service_posts(request), 'n': range(5)}
        return render(
            request, "review/posts.html",
            context)
    else:
        return redirect('userlogin')
