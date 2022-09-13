from django import forms

class create_listing_form(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'mytitleclass'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'mydescriptionclass'}))
    bid = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'mybidclass'}))
    image_url = forms.CharField(widget=forms.URLInput(attrs={'class': 'myimageclass'}))

#    def clean(self):
#        cleaned_data = super(create_listing_form, self).clean()
#        title = cleaned_data.get('title')
#        description = cleaned_data.get('description')
#        bid = cleaned_data.get('bid')
#        image_url = cleaned_data.get('image_url')
#        if not title and not bid and not image_url:
#            raise forms.ValidationError('You have to write something!')