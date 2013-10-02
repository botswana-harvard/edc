from django import forms
from bhp_common.classes import MyModelForm

class BaseDxForm (MyModelForm): 
    
    def clean(self):
    
        cleaned_data = self.cleaned_data 
    
        cleaned_data = super(BaseDxForm, self).clean()    
    
        return cleaned_data
        

