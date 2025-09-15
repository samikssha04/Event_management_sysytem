from django import forms
from app1.models import CustomUser, Profile,Event

class SignupForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full pl-3 pr-3 py-2 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-3 pr-3 py-2 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200',
            'placeholder': 'Create a password'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-3 pr-3 py-2 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200',
            'placeholder': 'Confirm your password'
        })
    )
    student_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-3 pr-3 py-2 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200',
            'placeholder': 'Enter your student ID'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2', 'student_id']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # Auto-generate username from email
        user.username = self.cleaned_data['email'].split('@')[0]
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class EventForm(forms.ModelForm):

    class Meta:

        model =Event

        fields = ['title', 'description', 'date', 'time', 'location', 'max_participants', 'category', 'image']

        widgets = {

            'title': forms.TextInput(attrs={'class': 'border p-2 rounded w-full'}),

            'description': forms.Textarea(attrs={'class': 'border p-2 rounded w-full', 'rows': 4}),

            'date': forms.DateInput(attrs={'type': 'date', 'class': 'border p-2 rounded'}),

            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'border p-2 rounded'}),

            'location': forms.TextInput(attrs={'class': 'border p-2 rounded w-full'}),

            'max_participants': forms.NumberInput(attrs={'class': 'border p-2 rounded w-full'}),

            'category': forms.TextInput(attrs={'class': 'border p-2 rounded w-full'}),

        }

