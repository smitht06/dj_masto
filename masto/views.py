from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from mastodon import Mastodon

from .forms import MastodonAccountForm
from .models import MastodonAccount


class ProfileView(View):
    template_name = "masto/profile.html"

    def get(self, request, *args, **kwargs):
        mastodon_account, created = MastodonAccount.objects.get_or_create(
            user=request.user
        )

        form = MastodonAccountForm(
            initial={
                "username": mastodon_account.username,
                "access_token": mastodon_account.access_token,
            }
        )

        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        mastodon_account, created = MastodonAccount.objects.get_or_create(
            user=request.user
        )

        form = MastodonAccountForm(request.POST)
        if form.is_valid():
            mastodon_account.username = form.cleaned_data["username"]
            mastodon_account.access_token = form.cleaned_data["access_token"]
            mastodon_account.save()

        return redirect("profile")


# ...


class MastodonAuthorizationView(View):
    def get(self, request):
        mastodon = Mastodon(
            client_id="LUnpeoioXBPuyHHmkQbJzLo5kb3YMqGuh7qJXHihlYI",
            client_secret="dUybd1c91vl6XyNiwrAzLkFC78VIxRiWrmWzC8GbkjM",
            api_base_url="https://mastodon.social",
        )
        redirect_url = mastodon.auth_request_url(
            redirect_uris="urn:ietf:wg:oauth:2.0:oob", scopes=["read", "write"]
        )

        return redirect(redirect_url)


class MastodonCallbackView(View):
    def get(self, request):
        mastodon = Mastodon(
            client_id="LUnpeoioXBPuyHHmkQbJzLo5kb3YMqGuh7qJXHihlYI",
            client_secret="dUybd1c91vl6XyNiwrAzLkFC78VIxRiWrmWzC8GbkjM",
            api_base_url="https://mastodon.social/",
        )
        code = request.GET.get("code")
        access_token = mastodon.log_in(
            code=code, redirect_uris="urn:ietf:wg:oauth:2.0:oob"
        )

        # Save the access token in your database along with the user's Mastodon username
        # Create or update the MastodonAccount model with the access token and username

        return redirect("profile")  # Redirect to the user's profile page after linking


from django.shortcuts import render
from django.views import View
from mastodon import Mastodon

from .models import MastodonAccount


import bleach

class TimelineView(View):
    template_name = 'masto/timeline.html'

    def get(self, request, *args, **kwargs):
        try:
            mastodon_account = MastodonAccount.objects.get(user=request.user)
        except MastodonAccount.DoesNotExist:
            return render(request, self.template_name, {'timeline': []})

        mastodon = Mastodon(
            client_id="LUnpeoioXBPuyHHmkQbJzLo5kb3YMqGuh7qJXHihlYI",
            client_secret="dUybd1c91vl6XyNiwrAzLkFC78VIxRiWrmWzC8GbkjM",
            api_base_url="https://mastodon.social/",
            access_token=mastodon_account.access_token,
        )
        
        timeline = mastodon.timeline_home()
        
        cleaned_timeline = []
        
        for post in timeline:
            cleaned_content = bleach.clean(post['content'], tags=[], attributes={}, strip=True)
            cleaned_timeline.append({
                'account_handle': post['account']['username'],
                'account_display_name': post['account']['display_name'],
                'account_avatar': post['account']['avatar'],
                'account_profile': post['account']['url'],
                'content': cleaned_content
            })

        return render(request, self.template_name, {'timeline': cleaned_timeline})