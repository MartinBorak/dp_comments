from django.contrib.auth.models import User
from django import forms


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class RadioForm(forms.Form):
    MY_CHOICES = (
        ('opt0', ' '),
        ('opt1', ' '),
        ('opt2', ' '),
    )

    comment_radio = forms.ChoiceField(widget=forms.RadioSelect, choices=MY_CHOICES)

    def __init__(self, *args, **kwargs):
        my_choices = (
            ('opt0', ' '),
            ('opt1', ' '),
            ('opt2', ' '),
        )

        if 'reply_count' in kwargs:
            reply_count = kwargs.pop('reply_count')
        else:
            reply_count = 0

        super(RadioForm, self).__init__(*args, **kwargs)

        for i in range(0, reply_count):
            self.fields['reply_%s' % i] = forms.ChoiceField(widget=forms.RadioSelect, choices=my_choices)

    def replies(self):
        i = 0
        for name, value in self.cleaned_data.items():
            if name.startswith('reply_'):
                i += 1
                yield value

    def comment_radio_choices(self):
        """
        Returns myfield's widget's default renderer, which can be used to
            render the choices of a RadioSelect widget.
        """
        field = self['comment_radio']
        widget = field.field.widget

        attrs = {}
        auto_id = field.auto_id
        if auto_id and 'id' not in widget.attrs:
            attrs['id'] = auto_id

        name = field.html_name

        return widget.get_renderer(name, field.value(), attrs=attrs)