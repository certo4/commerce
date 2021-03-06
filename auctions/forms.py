from django import forms

class CloseListing(forms.Form):
    form_type = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput()
    )

class WatchlistAction(forms.Form):
    add_watchlist = forms.BooleanField(
        widget=forms.HiddenInput()
    )


