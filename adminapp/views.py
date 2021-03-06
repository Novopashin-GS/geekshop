from django.contrib.auth.decorators import user_passes_test
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopAdminUserChangeForm, ProductCategoryForm, ProductForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users_list.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserCreationView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'adminapp/user_form.html'
    success_url = reverse_lazy('adminapp:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UsersUpdateView(UpdateView):
    model = ShopUser
    success_url = reverse_lazy('adminapp:users')
    template_name = 'adminapp/user_form.html'
    form_class = ShopAdminUserChangeForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UsersDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('adminapp:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductCategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories_list.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount/100))
        return super().form_valid(form)

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        category_item = get_object_or_404(ProductCategory, pk=category_id)
        context['object_list'] = Product.objects.filter(category__pk=category_item.pk)
        context['category'] = category_item
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductForm

    def get_success_url(self):
        category = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return reverse('adminapp:products', args=[category.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        context_data['category'] = category
        context_data['form'].initial['category'] = context_data['category']
        return context_data

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# ProductUpdateView(UpdateView, ProductCreateView)
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductForm

    def get_success_url(self):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        category_item = product.category
        return reverse('adminapp:products', args=[category_item.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        category_item = product.category
        context_data['category'] = category_item
        return context_data

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        category_item = product.category
        return reverse('adminapp:products', args=[category_item.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        category_item = product.category
        context_data['category'] = category_item
        return context_data

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
