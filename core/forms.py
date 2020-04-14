from django import forms
from ckeditor.widgets import CKEditorWidget

class ProductReviewForm(forms.Form): 
    REVIEW_CHOICES = (
        (1,'1'),
        (1.5,'1.5'),
        (2,'2'),
        (2.5,'2.5'),
        (3,'3'),
        (3.5,'3.5'),
        (4,'4'),
        (4.5,'4.5'),
        (5,'5') 
    )
    review_number = forms.ChoiceField(choices=REVIEW_CHOICES, label=False)
    review_content = forms.CharField(widget=forms.Textarea(attrs={'rows':'5'}), label=False)