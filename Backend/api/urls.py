from django.urls import path
from userauths import views as userauths_views
from store import views as store_views
# from customer import views as customer_views
# from vendor import views as vendor_views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('user/token/', userauths_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh', TokenRefreshView.as_view()),
    path('user/register/', userauths_views.RegisterView.as_view(), name='auth_register'),
    path('user/password-reset/<email>/', userauths_views.PasswordEmailVerify.as_view(), name='password_reset'),
    path('user/password-change/', userauths_views.PasswordChangeView.as_view(), name='password_change'),

    # Store Endpoints
    path('category/', store_views.CategoryListView.as_view(), name='category'),
    path('products/', store_views.ProductListView.as_view(), name='products'),
    path('products/<slug:slug>/', store_views.ProductDetailView.as_view(), name='brand'),
    path('cart-view/', store_views.CartAPI.as_view(), name='cart-view'),
]
