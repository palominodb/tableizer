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
