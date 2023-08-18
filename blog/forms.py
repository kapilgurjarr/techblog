from django import forms
from django.utils.translation import gettext_lazy as _

from tinymce.widgets import TinyMCE

from blog.models import Blog



class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','description','tags','image']
        labels = {
            'tags':_('Topics')
        }
        help_texts = {
            'tags':'''<ul>
                    <li>A comma-separated list of tags.</li>
                    <li>Add or change topics (up to 5) so readers know what your story is about</li>
                    </ul>
                    '''
        }

        # widgets = {
        #     'title':forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':'title'}),
        #     # 'description':TinyMCE(attrs={'cols': 80, 'rows': 30})
        # }

    