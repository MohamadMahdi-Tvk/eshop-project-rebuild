from django import forms


class ContactUsForm(forms.Form):
    full_name = forms.CharField(
        label='نام و نام خانوادگی',
        max_length=50,
        error_messages={
            'required': 'لطفا نام و نام خانوادگی خود را وارد کنید',
            'max_length': 'نام و نام خانوادگی نمیتواند بیشتر از 50 کارکتر باشد'
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام و نام خانوادگی',
            'autocomplete': 'name',
        })
    )

    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل',
            'autocomplete': 'email'
        })
    )

    subject = forms.CharField(
        label='عنوان',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'عنوان',
            'autocomplete': 'off',

        })
    )

    text = forms.CharField(
        label='متن پیام',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'متن پیام',
            'rows': '5',
            'id': 'message',
            'autocomplete': 'off'
        })
    )
