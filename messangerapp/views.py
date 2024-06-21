from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import CustomUser
from .models import Message
from .forms import MessageForm


class UserListView(LoginRequiredMixin, View):
    def get(self, request):
        users = CustomUser.objects.exclude(id=request.user.id)
        context = {
            'users': users
        }
        return render(request, 'index.html', context=context)


class MessageCreateView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        receiver = get_object_or_404(CustomUser, id=user_id)
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=request.user))

        ).order_by('-timestamp')
        form = MessageForm()
        context = {
            'receiver': receiver,
            'messages': messages,
            'form': form
        }
        return render(request, 'message_create.html', context=context)

    def post(self, request, user_id):
        receiver = get_object_or_404(CustomUser, id=user_id)
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('message:create-message', user_id=user_id)
        messages = Message.objects.filter(
            Q(sender=request.user) & Q(receiver=receiver) | (Q(sender=receiver) & Q(receiver=request.user))
        ).order_by('-timestamp')

        return render(request, 'message_create.html', {'receiver': receiver, 'messages': messages, 'form': form})


class MessageEditView(LoginRequiredMixin, View):
    def get(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        form = MessageForm(instance=message)
        context = {
            'message': message,
            'form': form
        }
        return render(request, 'message_edit.html', context=context)

    def post(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        form = MessageForm(request.POST, request.FILES, instance=message)
        if form.is_valid():
            message = form.save(commit=False)
            message.save()
            return redirect('message:create-message', user_id=message.receiver.id)
        context = {
            'message': message,
            'form': form
        }
        return render(request, 'message_edit.html', context=context)


class MessageDeleteView(LoginRequiredMixin, View):
    def get(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        message.delete()
        return redirect('message:create-message', user_id=message.receiver.id)
