from django.urls import path, include
from django.contrib.auth import views
from .views import Login, UserCreateView, ProductListView, ProductUpdateView, ProductCreateView, ReturnCreateView,\
PurchaseCreateView, PurchaseListView, ReturnDeleteView, PurchaseDeleteView, ReturnListView


urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('product/', ProductCreateView.as_view(), name='product'),
    path('purchase_add/<int:pk>', PurchaseCreateView.as_view(), name='purchase_add'),
    path('product_change/<int:pk>', ProductUpdateView.as_view(), name='product_change'),
    path('purchases/', PurchaseListView.as_view(), name='purchases'),
    path('returns/', ReturnListView.as_view(), name='returns'),
    path('return_add/<int:pk>', ReturnCreateView.as_view(), name='return_add'),
    path('return_del/<int:pk>', ReturnDeleteView.as_view(), name='delete_return'),
    path('purchase_del/<int:pk>', PurchaseDeleteView.as_view(), name='delete_purchase'),
]