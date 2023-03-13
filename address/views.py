from django.forms import TextInput
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from orders.models import Address
#from .models import Wallet

app_name = 'address'

class AddressListView(ListView):
    model = Address
    template_name = 'accounts/address_list.html'
    context_object_name = 'addresses'
    paginate_by = 10
    
def addresslist(request):
    address=Address.objects.filter(user=request.user)
    context={
        'addresses':address,
    }
    return render(request,'accounts/address_list.html',context)

class AddressCreateView(CreateView):
    model = Address
    fields = ['first_name', 'last_name', 'phone', 'address_line_1', 'address_line_2', 'city', 'state', 'country', 'zip_code']
    template_name = 'address_form.html'
    success_url = reverse_lazy('address:address_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AddressUpdateView(UpdateView):
    model = Address
    fields = ['first_name', 'last_name', 'phone', 'address_line_1', 'address_line_2', 'city', 'state', 'country', 'zip_code']
    
    template_name = 'accounts/address_form.html'
    success_url = reverse_lazy('address:address_list')
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['first_name'].widget = TextInput(attrs={'placeholder': 'Enter your first name', "class": "form-control", 'label': False})
        form.fields['last_name'].widget = TextInput(attrs={'placeholder': 'Enter your last name', "class": "form-control", 'label': False})
        form.fields['phone'].widget = TextInput(attrs={'placeholder': 'Enter your phone number', 'label': False})
        form.fields['address_line_1'].widget = TextInput(attrs={'placeholder': 'Enter your address line 1', 'label': False})
        form.fields['address_line_2'].widget = TextInput(attrs={'placeholder': 'Enter your address line 2', 'label': False})
        form.fields['city'].widget = TextInput(attrs={'placeholder': 'Enter your city', 'label': False})
        form.fields['state'].widget = TextInput(attrs={'placeholder': 'Enter your state', 'label': False})
        form.fields['country'].widget = TextInput(attrs={'placeholder': 'Enter your country', 'label': False})
        form.fields['zip_code'].widget = TextInput(attrs={'placeholder': 'Enter your zip code', 'label': False})
        return form

class AddressDeleteView(DeleteView):
    model = Address
    template_name = 'address_confirm_delete.html'
    success_url = reverse_lazy('address:address_list')
    
    

