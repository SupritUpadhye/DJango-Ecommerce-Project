from django.urls import path
from authentication import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('address/', views.address, name="address" ),
    path('skip_address/', views.skip_address, name='skip_address'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('profileEdit/<uid>/', views.profileEdit, name="profileEdit"),
    path('delete_account/', views.delete_account, name="delete_account"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)