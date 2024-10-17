from django.urls import path

from propertyapp import views

urlpatterns = [
    path('home',views.home,name='home'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('contact', views.home, name='contact'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('tenant_dashboard',views.tenant_dashboard,name='tenant_dashboard'),
    path('agent_dashboard',views.agent_dashboard,name='agent_dashboard'),
    path('tenant_add', views.tenant_add, name='tenant_add'),
    path('agent_add', views.agent_add, name='agent_add'),
    path('login_view', views.login_view, name='login_view'),
    path('tenant_view', views.tenant_view, name='tenant_view'),
    path('agent_view', views.agent_view, name='agent_view'),
    path('delete/<int:id>/', views.tenant_delete, name='delete'),
    path('agent_delete/<int:id>/', views.agent_delete, name='agent_delete'),
    path('feedback_form', views.save_feedback, name='feedback_form'),
    path('view_tenant_feedback', views.view_tenant_feedback, name='view_tenant_feedback'),
    # path('feedback_delete/<int:id>/', views.feedback_delete,name='feedback_delete'),
    path('tenant_feedback', views.tenant_feedback, name='tenant_feedback'),

    path('update/<int:id>/', views.admin_reply_feedback, name='update'),
    path('addProperty', views.property_agent, name='addProperty'),
    path('viewProperty', views.property_display, name='viewProperty'),
    path('property_delete/<int:id>/', views.property_delete, name='property_delete'),
    path('property_view', views.property_view, name='property_view'),
    path('property_view_general', views.property_view_general, name='property_view_general'),
    path('tenant_property_view', views.tenant_property_view, name='tenant_property_view'),
    path('add_to_wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('viewCart', views.viewCart, name='viewCart'),
    path('deleteItems/<int:id>/', views.deleteItems, name='deleteItems'),
    path('buynow/<int:id>/', views.buynow, name='buynow'),
    path('wishlistbuy/<int:id>/', views.wishlistbuy, name='wishlistbuy'),
    path('payment/<int:id>/', views.paynow, name='payment'),
    path('logout', views.logout_view, name='logout'),
    path('error', views.error, name='error'),
    path('soldProperty', views.soldProperty, name='soldProperty'),
    path('soldListAdmin', views.soldListAdmin, name='soldListAdmin'),
    path('orderedproperty', views.orderedProperty, name='orderedproperty'),


]