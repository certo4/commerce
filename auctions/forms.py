from django import forms
from django.forms import ModelForm
from .models import Listing, Bid, Comment


class CloseListing(forms.Form):
    close_listing = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.HiddenInput()
    )


class WatchlistAction(forms.Form):
    set_watchlist = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput()
    )


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'starting_bid',
            'img_url',
            'category'
        ]


class BiddingForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
