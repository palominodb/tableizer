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

class TopDatabasesForm(forms.Form):
    limit = forms.IntegerField(min_value=1)
    days = forms.IntegerField(min_value=1)
    percent = forms.FloatField(required=False)
    gbytes = forms.FloatField(required=False)
    
    def clean(self):
        cleaned_data = super(TopDatabasesForm, self).clean()
        limit = cleaned_data.get('limit')
        days = cleaned_data.get('days')
        percent = cleaned_data.get('percent')
        gbytes = cleaned_data.get('gbytes')
        if not percent and not gbytes and percent != 0 and gbytes != 0:
            raise forms.ValidationError('Must specify percentage.')
        return cleaned_data
        
class TopTablesForm(forms.Form):
    limit = forms.IntegerField(min_value=0)
    days = forms.IntegerField(min_value=0)
    percent = forms.FloatField()
