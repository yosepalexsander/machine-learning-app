from django import forms


class ReviewForm(forms.Form):

    review_name = forms.CharField(label="Your name", max_length=100)
    review_text = forms.CharField(
        label="Drop your thought about our product", widget=forms.Textarea
    )
