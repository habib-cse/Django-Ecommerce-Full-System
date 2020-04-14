from django.urls import path,include
from . import views
app_name = 'core'
urlpatterns = [ 
    path('', views.HomepageView.as_view(), name="home"),
    path('product-details/<slug>', views.product_details, name="product_details"),
    path("register", views.UserRegistration, name="registration"),
    path("login", views.UserLogin, name="login"),
    path("logout", views.UserLogout, name="logout"),
    path("add-to-card/<int:id>", views.AddToCard, name="addtocard"),
    path("checkout/<int:id>", views.checkout, name="checkout"),
    path("remove_from_card/<int:id>",views.remove_from_card, name="remove_from_card"),
    path("card_update",views.card_update, name="card_update"),
    path("serch",views.product_search, name="serch"),
]