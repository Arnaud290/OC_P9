"""
module for managing views
"""
from django.shortcuts import (
    render,
    redirect
)
from django.contrib.auth import logout
from .models import (
    Ticket,
    Review
)
from .forms import (
    LoginForm,
    RegistrationForm,
    TicketForm,
    ReviewForm,
    SubsriptionForm
)
from .services import (
    service_unsubscribe_user,
    service_followed_users,
    service_login_registration,
    service_posts,
    service_ticket_review,
    service_get_instance,
    service_save_ticket,
    service_delete,
    service_subscription,
    service_save_review
)


def index(request):
    """
    Function that refers to the login
    view for access to the index page
    """
    return redirect('userlogin')


def userlogin(request):
    """
    Function of the login page view
    """
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
        {'form': form}
    )


def userlogout(request):
    """
    User logout function
    """
    logout(request)
    return redirect('userlogin')


def registration(request):
    """
    Add users function for the registration page
    """
    if request.method == 'POST':
        form = service_login_registration(
            request,
            registration=True
        )
        if form.is_valid():
            return redirect('userlogin')
    else:
        form = RegistrationForm()
    return render(
        request, "review/registration.html",
        {'form': form}
    )


def feed(request):
    """
    Post management function for the feed page
    """
    if request.user.is_authenticated:
        context = {
            'posts': service_posts(
                request,
                followers=True
            ),
            'ticket_review': service_ticket_review(),
            'n': range(5)
        }
        return render(
            request, "review/feed.html",
            context
        )
    return redirect('userlogin')


def ticket(request, id_ticket=None):
    """
    Ticket creation or modification management
    function for the tickets page
    """
    if request.user.is_authenticated:
        instance_ticket = service_get_instance(
            request,
            Ticket,
            id_ticket
        )
        if instance_ticket is False:
            return redirect('feed')
        if request.method == 'POST':
            ticket_form = service_save_ticket(
                request,
                instance_ticket
            )
            if ticket_form.is_valid():
                if id_ticket is not None:
                    return redirect('posts')
                return redirect('feed')
        else:
            ticket_form = TicketForm(instance=instance_ticket)
        return render(
            request,
            "review/ticket.html",
            {'ticket_form': ticket_form}
        )
    return redirect('userlogin')


def delete_ticket(request, id_ticket):
    """
    Ticket deletion function
    """
    if request.user.is_authenticated:
        service_delete(
            request,
            Ticket,
            id_ticket
        )
    return redirect(request.META.get('HTTP_REFERER'))


def subscription(request):
    """
    Management function of the followed users page
    """
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
            request,
            "review/subscription.html",
            context
        )
    return redirect('userlogin')


def unsubscribe_user(request, id_user):
    """
    User unsubscribe function
    """
    if request.user.is_authenticated:
        service_unsubscribe_user(request, id_user)
    return redirect('subscription')


def review(request, id_ticket=None):
    """
    Review page management function
    """
    if request.user.is_authenticated:
        instance_ticket = service_get_instance(
            request,
            Ticket,
            id_ticket,
            review=True
        )
        instance_review = service_get_instance(
            request,
            Review,
            id_ticket,
            review=True
        )
        if instance_review is False:
            return redirect('feed')
        ticket_form = TicketForm(instance=instance_ticket)
        review_form = ReviewForm(instance=instance_review)
        if request.method == 'POST':
            if id_ticket is not None:
                review_form = service_save_review(
                    request,
                    instance_ticket=instance_ticket,
                    instance_review=instance_review
                )
                if instance_review is None:
                    return redirect('feed')
                return redirect('posts')
            ticket_form = service_save_ticket(
                request,
                instance_ticket=instance_ticket,
                instance_review=instance_review,
                review=True
            )
        context = {
            'ticket_form': ticket_form,
            'review_form': review_form,
        }
        return render(
            request, "review/review.html", context)
    return redirect('userlogin')


def delete_review(request, id_review):
    """
    Fonction to delete a review
    """
    if request.user.is_authenticated:
        service_delete(
            request,
            Review,
            id_review
        )
    return redirect(request.META.get('HTTP_REFERER'))


def posts(request):
    """
    Management function of the posts page
    """
    if request.user.is_authenticated:
        context = {
            'posts': service_posts(request),
            'n': range(5)
        }
        return render(
            request, "review/posts.html",
            context
        )
    return redirect('userlogin')
