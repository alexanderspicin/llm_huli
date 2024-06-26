from django.urls import path

from .api.views import TextUploadView, TextFileDetailView
from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path('upload/', TextUploadView.as_view(), name='text-upload'),
    path('files/<int:pk>/', TextFileDetailView.as_view(), name='file-detail')
]
