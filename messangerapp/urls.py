from django.urls import path
from .views import UserListView, MessageCreateView, MessageEditView, MessageDeleteView

app_name = 'message'
urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('create-message/<int:user_id>/', MessageCreateView.as_view(), name='create-message'),
    path('edit-message/<int:message_id>/', MessageEditView.as_view(), name='edit-message'),
    path('delete-message/<int:message_id>', MessageDeleteView.as_view(), name='delete-message')

]
