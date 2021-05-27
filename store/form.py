from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('full_name','email','phone','message')
        widgets ={
            'full_name':forms.TextInput(attrs={'class':'contact_form_name input_field', 'placeholder':'Tên của bạn', 'required':'required','data-error':'Tên không được để trống'}),
            'email':forms.TextInput(attrs={'class':'contact_form_name input_field', 'placeholder':'Email của bạn', 'required':'required','data-error':'Tên không được để trống'}),
            'phone':forms.TextInput(attrs={'class':'contact_form_email input_field', 'placeholder':'Số điện thoại của bạn'}),
            'message':forms.Textarea(attrs={'class':'text_field contact_form_message', 'placeholder':'Nội dung', 'required':'required','data-error':'Nội dung không được để trống', 'name':'message','rows':'4'})
        }