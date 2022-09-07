
from django import forms
from .choices import read_choices, read_label_choices

CODE_CHOICES= []

## read labels/codes dictionnary  
codesDict = read_label_choices() 
choices =read_choices()

## create a list of code, label tuples
for key,value in codesDict.items():
    CODE_CHOICES.append((key, str(value).capitalize()))


class NameForm(forms.Form):    
    choice1 = forms.CharField(label='1er Choix', max_length=100, widget=forms.Select(choices=CODE_CHOICES, attrs={'style': 'width:120px'}))
    choice2 = forms.CharField(label='2eme Choix', max_length=100, widget=forms.Select(choices=CODE_CHOICES, attrs={'style': 'width:120px'}))
    choice3 = forms.CharField(label='3eme Choix', max_length=100, widget=forms.Select(choices=CODE_CHOICES, attrs={'style': 'width:120px'}))
    choice4 = forms.CharField(label='4eme Choix', max_length=100, widget=forms.Select(choices=CODE_CHOICES, attrs={'style': 'width:120px'}))
    choice5 = forms.CharField(label='5eme Choix', max_length=100, widget=forms.Select(choices=CODE_CHOICES, attrs={'style': 'width:120px'}))
    choice6 = forms.CharField(label='6eme Choix', max_length=100, widget=forms.Select(choices=CODE_CHOICES, attrs={'style': 'width:120px'}))
