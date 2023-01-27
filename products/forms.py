from django import forms



class ProductCreateForm(forms.Form):
    title = forms.CharField(min_length=5)
    description = forms.CharField(widget=forms.Textarea())
    rate = forms.FloatField(max_value=5, min_value=2)
    price = forms.FloatField(min_value=1)

class  ReviewCreateForm(forms.Form):
    text = forms.CharField(min_length=4)
