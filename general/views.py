from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .forms import CustomerQueryForm



def contact_page(request):
    form = CustomerQueryForm()
    if request.method == 'POST':
        form = CustomerQueryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your query has been submitted successfully!')
            return redirect('store:store')
    else:
        return render(request, 'contact.html', {'form': form})

# Create your views here.
def aboutUs(request):
    return render(request, 'about-us.html')