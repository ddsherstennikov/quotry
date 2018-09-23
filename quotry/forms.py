from django import forms
from django.contrib.auth.models import User

from quotry.models import Tag, Quote, UserProfile


class TagForm(forms.ModelForm):
    # payload:
    name = forms.CharField(max_length=128, help_text="Please enter the tag name.")

    # ranging: *hidden
    visits = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    favs = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # tech: *optional
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Tag
        fields = ('name', 'visits', 'favs', 'slug',)


class QuoteForm(forms.ModelForm):
    # org: tag *exclude

    # payload: *required
    title = forms.CharField(max_length=128, help_text="Please enter the title of the quote.")
    author = forms.CharField(max_length=128, help_text="Please enter the author of the quote.")
    text = forms.CharField(widget=forms.Textarea, max_length=999, help_text="Please enter the quote.")
    #          *optional
    url = forms.URLField(widget=forms.URLInput, max_length=200, help_text="Optionally enter the URL, illustrating the quote.", required=False)

    # ranging: *hidden
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Quote
        exclude = ('tag',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data


class UserForm(forms.ModelForm):
    # payload:
    email = forms.EmailField(widget=forms.EmailInput(), required=False)

    class Meta:
        model = User
        fields = ('email',)


class UserProfileForm(forms.ModelForm):
    # tech and payload: user - CRT link when we reg the user
    # org: favs, likes - exclude
    # addon payload: website, picture - leave default form fields
    website = forms.URLField(required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('website', 'picture')