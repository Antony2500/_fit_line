from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login

from cart.models import Cart
from . import templates
from authentication.forms import LoginForm, RegisterForm
from django.views.generic import TemplateView, CreateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.


def log_in_user(request):
    # Initialize the context with an empty login form
    # Ініціалізуємо контекст із порожньою формою для входу
    context = {'login_form': LoginForm()}

    # Check if the request method is POST, which means a login form has been submitted
    # Перевіряємо, чи метод запиту є POST, що означає, що була надіслана форма для входу
    if request.method == 'POST':
        # Create an instance of the LoginForm with the data from the POST request
        # Створюємо екземпляр LoginForm із даними з POST запиту
        login_form = LoginForm(request.POST)

        # Check if the form data is valid
        # Перевіряємо, чи дані з форми є коректними
        if login_form.is_valid():
            # Extract the cleaned data from the form
            # Отримуємо очищені дані із форми
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # Authenticate the user with the provided username and password
            # Аутентифікуємо користувача за вказаним ім'ям користувача та паролем
            user = authenticate(username=username, password=password)

            # If authentication is successful, log in the user and redirect to the 'index' page
            # Якщо аутентифікація пройшла успішно, логуємо користувача та перенаправляємо на сторінку 'index'
            if user:
                login(request, user)
                try:
                    cart = Cart.objects.get(session_id=request.session["nonuser"], completed=False)
                    if Cart.objects.filter(user=request.user, completed=False).exists():
                        cart.user = None
                        cart.save()

                    else:
                        cart.user = request.user
                        cart.save()


                except:
                    print("omooooooooooo")

                return redirect('index')
            else:
                # If authentication fails, update the context with the login form and an attention message
                # Якщо аутентифікація не вдалася, оновлюємо контекст із формою для входу та повідомленням про помилку
                context = {
                    'login_form': login_form,
                    'attention': f'The user with username {username} and password was not found :('
                }
        else:
            # If the form data is not valid, update the context with the login form
            # Якщо дані з форми некоректні, оновлюємо контекст із формою для входу
            context = {
                'login_form': login_form,
            }



    # Render the 'log_in.html' template with the appropriate context
    # Рендеримо шаблон 'log_in.html' із відповідним контекстом
    return render(request, 'authentication/log_in.html', context)

# def log_in_user2(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#
#             return redirect('home')
#         else:
#
#             error_message = "Invalid username or password. Please try again."
#             return render(request, 'authentication/log_in.html', {'error_message': error_message})
#
#     return render(request, 'authentication/log_in.html')


class RegisterView(CreateView):
    template_name = 'authentication/sign_up.html'
    form_class = RegisterForm

    # URL to redirect the user after successful registration
    # (URL для перенаправлення користувача після успішної реєстрації)
    success_url = reverse_lazy("successfully_completed")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()

        # Authenticate the user (Аутентифікує користувача)
        login(self.request, user)

        return response

# class RegisterView2(TemplateView):
#     template_name = 'authentication/sign_up.html'
#
#     def get(self, request):
#         user_form = RegisterForm()
#         context = {'user_form': user_form}
#         return render(request, 'authentication/sign_up.html', context)
#
#     def post(self, request):
#         user_form = RegisterForm(request.POST)
#         if user_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             login(request, user)
#             return redirect('index')
#
#         context = {'user_form': user_form}
#         return render(request, 'authentication/sign_up.html', context)


def successfully_completed(request):
    return render(request, 'authentication/successfully_completed.html')


def logout_user(request):
    logout(request)
    return redirect('index')


# class ProfileView(View):
#     def get(self, request):
#         form = CustomerProfileForm()
#         context = {
#             'form': form,
#         }
#         return render(request, 'authentication/profile.html', context)
#
#     def post(self, request):
#         form = CustomerProfileForm(request.POST)
#         context = {
#             'form': form,
#         }
#         if form.is_valid():
#             user = request.user
#             name = form.cleaned_data['name']
#             city = form.cleaned_data['city']
#             locality = form.cleaned_data['locality']
#             branch_number = form.cleaned_data['branch_number']
#             mobile = form.cleaned_data['mobile']
#             state = form.cleaned_data['state']
#             zipcode = form.cleaned_data['zipcode']
#             comment = form.cleaned_data['comment']
#
#             reg = Customer(user=user, name=name, city=city, locality=locality, branch_number=branch_number,
#                            mobile=mobile, state=state, zipcode=zipcode, comment=comment)
#             reg.save()
#             messages.success(request, "Вітаю! Профіль успішно збережено")
#         else:
#             messages.warning(request, "Неправильні вхідні дані")
#         return render(request, 'authentication/profile.html', context)


# def address(request):
#     addresses = Customer.objects.filter(user=request.user)
#     context = {
#         'addresses': addresses,
#     }
#     return render(request, 'authentication/address.html', {'addresses': addresses})
#
#
# class UpdateAddress(View):
#     def get(self, request, pk):
#         add = Customer.objects.get(pk=pk)
#         form = CustomerProfileForm(instance=add)
#
#         return render(request, 'authentication/update_address.html', {'form': form})
#
#     def post(self, request, pk):
#         add = Customer.objects.get(pk=pk)
#         form = CustomerProfileForm(request.POST, instance=add)
#
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Адресу успішно оновлено")
#             return redirect('address')  # перенаправление на страницу адресов или другую нужную страницу
#         else:
#             messages.warning(request, "Неправильні вхідні дані")
#         return render(request, 'authentication/update_address.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('successfully_completed')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'authentication/change_password.html', {'form': form})
