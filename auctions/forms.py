from django import forms

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


