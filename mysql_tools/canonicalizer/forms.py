# forms.py
# Copyright (C) 2009-2013 PalominoDB, Inc.
# 
# You may contact the maintainers at eng@palominodb.com.
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class LastStatementsForm(forms.Form):
    minutes = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'

        self.helper.add_input(Submit('view_last_statements', 'View last statements'))
        super(LastStatementsForm, self).__init__(*args, **kwargs)


class TopQueriesForm(forms.Form):
    limit = forms.IntegerField()
    column = forms.ChoiceField(help_text='Column to initially sort by.')
    hostname = forms.ChoiceField(required=False, help_text='Select hostname to include in the result.')
    schema = forms.ChoiceField(required=False, help_text='Select schema to include in the result.')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'

        self.helper.add_input(Submit('view_top_queries', 'View top queries'))
        super(TopQueriesForm, self).__init__(*args, **kwargs)
