"""
URL configuration for remarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from users.views import user_login ,UserRegisterView ,custom_password_reset_view , user_logout

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import RealtorBankDetailsViewSet ,GetLocationPriceTypeNamesAndIds , PropertyListingViewSet , ViewSettlementTransactionDataViewSet , property_search_sort_filter ,landing_page

router = DefaultRouter()
router.register(r'realtor-bank-details', RealtorBankDetailsViewSet)
router.register(r'listing', PropertyListingViewSet)
router.register(r'transactions', ViewSettlementTransactionDataViewSet)



urlpatterns = [
    path("", landing_page , name = 'home'),
    path("admin/", admin.site.urls),

    #User urls  
    path('login', user_login, name='user_login'),
    path('logout', user_logout, name='user_logut'),
    path('register',UserRegisterView.as_view(), name='register'),
    path('reset-password/', custom_password_reset_view, name='reset-password'),

    #CRUB apis bankdetails 
    path('api/', include(router.urls)),

    path('options',GetLocationPriceTypeNamesAndIds.as_view({'get': 'list'}), name='options'),
    path('search/', property_search_sort_filter, name='search')


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns = [
#     # path('listings/', PropertyListView.as_view(), name='property-list'),
#     # path('listings/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
#     path('login/', user_login, name='user_login')
# ]
