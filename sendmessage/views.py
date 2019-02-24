from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib import auth
from .forms import UserForm, SendMessageForm
from django.views.generic import FormView
from django.core.mail import send_mail
from .models import Message
from django.contrib import messages
from django.contrib.auth.models import User


class ShowLoginForm(FormView):
    form_class = UserForm
    template_name = 'login_form.html'
    success_url = '../message'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('../message')
        else:
            return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        login = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=login, password=password)
        if user is not None:
            auth.login(request, user)
            return self.form_valid(self.form_class)
        else:
            messages.error(request, 'Неверный пользователь или пароль.')
            return self.form_invalid(self.form_class)


class ShowRegistrationForm(FormView):
    form_class = UserForm
    template_name = 'registration_form.html'
    success_url = '../login'

    def post(self, request, *args, **kwargs):
        login = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=login).exists():
            messages.error(request, 'Пользователь с таким именем уже существует.')
            return self.form_invalid(self.form_class)
        else:
            User.objects.create_user(login, password=password)
            return self.form_valid(self.form_class)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class ShowSendMessageForm(FormView):
    form_class = SendMessageForm
    template_name = 'send_message_form.html'
    success_url = '../message'

    def post(self, request, *args, **kwargs):
        message = request.POST['message']
        admin_email = request.POST['email']
        if send_mail('', message, 'test@test.com', [admin_email]):
            new_message = Message(user=request.user, email=admin_email,  message=message)
            new_message.setstatus(admin_email)
            new_message.save()
            messages.success(request, f'Cообщение отправлено на адрес {admin_email}.')
            return self.form_valid(self.form_class)
        else:
            messages.error(request, 'Ошибка отправки сообщения')
            return self.form_invalid(self.form_class)


def logout(request):
    auth.logout(request)
    return redirect('../login')
