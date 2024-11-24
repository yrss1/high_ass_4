from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EmailForm
from .tasks import send_email_task

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save()
            send_email_task.delay(email.id)
            messages.success(request, 'Email is being sent in the background.')
            return redirect('send_email')
    else:
        form = EmailForm()
    return render(request, 'tasks/send_email.html', {'form': form})

