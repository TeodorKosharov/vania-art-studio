from django import forms
from django.core.exceptions import ValidationError

from vania_art_studio.products.models import Card, Album, Frame, ChristeningSet


class AddCardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = '__all__'


class AddAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = '__all__'


class AddFrameForm(forms.ModelForm):
    class Meta:
        model = Frame
        fields = '__all__'


class AddChristeningSetForm(forms.ModelForm):
    class Meta:
        model = ChristeningSet
        fields = '__all__'


class SearchForm(forms.Form):
    search = forms.CharField(max_length=40, label='', widget=forms.TextInput(attrs={
        'placeholder': 'Търсене...',
        'class': 'search-form-input'
    }))


class FilterProductsForm(forms.Form):
    field = forms.ChoiceField(choices=(
        ('male_products', 'мъжки продукти'),
        ('female_products', 'женски продукти'),
        ('price_ascending', 'цена \u2B08'),
        ('price_descending', 'цена \u2B0A'),
        ('quantity_ascending', 'количество \u2B08'),
        ('quantity_descending', 'количество \u2B0A'),
    ),
        widget=forms.Select(attrs={'class': 'filter-criteria'}))


class FilterViewProductsForm(forms.Form):
    products_per_row = forms.ChoiceField(choices=(
        ('3', '3 продукта на ред'),
        ('4', '4 продукта на ред')
    ), widget=forms.Select(attrs={
        'class': 'filter-criteria'
    }))


class FilterCommentsForm(forms.Form):
    field = forms.ChoiceField(choices=(
        ('most_recent', 'най-нови'),
        ('oldest', 'най-стари')
    ),
        widget=forms.Select(attrs={'class': 'filter-criteria'}))


class AddCommentForm(forms.Form):
    comment = forms.CharField(max_length=150, label='', widget=forms.TextInput(attrs={
        'class': 'add-comment-input',
        'placeholder': 'Коментар...'
    }))

    def clean_comment(self):
        value = self.cleaned_data.get('comment')
        if len(value) < 10:
            raise ValidationError('Коментарът трябва да съдържа минимум 10 символа')
        return value


class EditCommentForm(AddCommentForm):
    comment = forms.CharField(max_length=150, label='', widget=forms.TextInput(attrs={
        'class': 'add-comment-input',
        'placeholder': 'Редакция на коментар...'
    }))
