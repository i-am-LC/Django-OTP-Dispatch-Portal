from django.urls import path

from .views import ClientCreateView, ClientDetailView, \
    ClientUpdateView, ClientDeleteView, AuthRepCreateView, AuthRepUpdateView

urlpatterns = [
    # /client/create/
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('detail/<pk>', ClientDetailView.as_view(), name='client_detail'),
    path('update/<pk>', ClientUpdateView.as_view(), name='client_update'),
    path('delete/<pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('<client>/authorised-representative/create', AuthRepCreateView.as_view(), name='auth_rep_create'),
    path('<client>/authorised-representative/update/<pk>', AuthRepUpdateView.as_view(), name='auth_rep_update'),
    # path('<client>/authorised-representative/delete/<pk>', AuthRepDeleteView.as_view(), name='auth_rep_delete'),
]