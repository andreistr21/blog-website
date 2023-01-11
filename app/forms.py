from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy
from tinymce.widgets import TinyMCE

from app.models import Comments, Post, Subscribe


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ("content",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs["placeholder"] = "Type your comment...."


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = "__all__"
        labels = {"email": gettext_lazy("")}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "Enter your email"


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))


class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"}))

    class Meta:
        model = User
        fields = ("username", "email", "password")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Create password"}),
        }

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("confirm_password", "Password mismatch")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("image", "title", "content", "tags")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["placeholder"] = "Title"
        self.fields["content"].widget = TinyMCE()
        self.fields["content"].widget.attrs["placeholder"] = "Enter content here"
        self.fields["tags"].help_text = "Hold down “Control”, or “Command” on a Mac, to select more than one."
