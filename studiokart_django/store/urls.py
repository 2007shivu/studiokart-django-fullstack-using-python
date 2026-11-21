from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('brand/<str:brand_name>/', views.brand_page, name='brand_page'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/configure/', views.configure_product_action, name='configure_product'),
    path('product/<int:pk>/review/', views.add_review, name='add_review'),
    path('compare/', views.compare_view, name='compare'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:pk>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('login/', views.auth_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/<int:item_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/delete/<int:pk>/', views.delete_product, name='delete_product'),
]
