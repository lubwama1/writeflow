
from django import forms
from .models import Post, Comment, Contact


class CreatePostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'custom-input'}))
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'title-input'}))

    class Meta:
        model = Post
        fields = [
            'title', 'content', 'published'
        ]

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label_suffix = ''
            if field.label and '*' in field.label:
                field.label = field.label.replace('*', '')


class CommentForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'comment-form-content'}))

    class Meta:
        model = Comment
        fields = [
            'content'
        ]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'full_name', 'email', 'message'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
            'message': forms.Textarea(attrs={
                'class': 'message-control',
                'placeholder': 'Send a message',

            }),

        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        # Iterate over the fields and update labels
        for field_name, field in self.fields.items():
            field.label_suffix = ''  # Remove the colon after the label

            # Check if the label contains '*' and remove it
            if field.label and '*' in field.label:
                field.label = field.label.replace('*', '')

