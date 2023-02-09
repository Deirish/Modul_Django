from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.http import HttpResponseRedirect
from config.settings import RETURN_TIME_LIMIT


from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from myapp.forms import UserCreateForm, PurchaseCreateForm, ReturnCreateForm
from myapp.models import Product, Purchase, Return



class SuperuserRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('home')


class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        valid = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return valid


class ProductListView(ListView):
    model = Product
    template_name = 'index.html'
    extra_context = {'form': PurchaseCreateForm}
    paginate_by = 3


class ProductCreateView(SuperuserRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'image', 'description', 'price', 'available']
    template_name = 'product.html'
    success_url = reverse_lazy('product')


class ProductUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'image', 'description', 'price', 'available']
    template_name = 'product_change.html'
    success_url = reverse_lazy('home')


class PurchaseListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Purchase
    template_name = 'purchase.html'
    extra_context = {'form': ReturnCreateForm}
    paginate_by = 3

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = Purchase.objects.filter(customer=self.request.user)
            return queryset
        queryset = Purchase.objects.all()
        return queryset


class ReturnCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    form_class = ReturnCreateForm
    template_name = 'purchase.html'
    success_url = reverse_lazy('returns')

    def form_valid(self, form):
        obj = form.save(commit=False)
        purchase_id = self.kwargs.get('pk')
        purchase = Purchase.objects.get(id=purchase_id)
        check_time = timezone.now() - purchase.date
        if check_time.seconds > RETURN_TIME_LIMIT:
            messages.error(self.request, 'Impossible to issue. Time is up!')
            return HttpResponseRedirect('/purchases')
        obj.purchase = purchase
        obj.save()
        return super().form_valid(form)


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    form_class = PurchaseCreateForm
    template_name = 'include/main.html'
    success_url = reverse_lazy('purchases')

    def form_valid(self, form):
        obj = form.save(commit=False)
        product_id = self.kwargs.get('pk')
        product = Product.objects.get(id=product_id)
        client = self.request.user
        ordered_available = int(self.request.POST['available'])
        if ordered_available > product.available:
            messages.error(self.request, 'Not enough goods in stock')
            return HttpResponseRedirect('/')
        purchase_amount = product.price * ordered_available
        if purchase_amount > client.cash:
            messages.error(self.request, 'Not enough funds to make a purchase')
            return HttpResponseRedirect('/')
        obj.product = product
        obj.client = client
        product.available -= ordered_available
        client.deposit -= purchase_amount

        with transaction.atomic():
            obj.save()
            product.save()
            client.save()

        return super().form_valid(form)


class ReturnListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Return
    template_name = 'return.html'
    paginate_by = 3

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = Return.objects.filter(purchase__client=self.request.user)
            return queryset
        queryset = Return.objects.all()
        return queryset


class ReturnDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Return
    success_url = reverse_lazy('returns')


class PurchaseDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Purchase
    success_url = reverse_lazy('returns')

    def form_valid(self, form):
        purchase = self.get_object()
        client = purchase.client
        product = purchase.product
        client.cash += purchase.purchase_amount
        product.available += purchase.available

        with transaction.atomic():
            client.save()
            product.save()
            purchase.delete()
        return HttpResponseRedirect(self.success_url)




