from django.urls import path
from . import views
urlpatterns = [
    path('',views.BoardListView.as_view(),name='home'),
    path('add_board/', views.add_board, name='add_board'),
    path('boards/<int:board_id>/',views.board_topics,name='board_topics'),
    path('unauthorized_delete/', views.unauthorized_delete, name='unauthorized_delete'),
    path('boards/<int:board_id>/new/',views.new_topic,name='new_topic'),
    path('boards/<int:board_id>/topics/<int:topic_id>', views.topic_posts, name='topic_posts'),
    path('boards/<int:board_id>/topics/<int:topic_id>/reply/', views.reply_topic, name='reply_topic'),
    path('boards/<int:board_id>/topics/<int:topic_id>/posts/<int:post_id>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path('boards/<int:board_id>/topics/<int:topic_id>/edit/', views.edit_topic, name='edit_topic'),
    path('boards/<int:board_id>/topics/<int:topic_id>/delete/', views.delete_topic, name='delete_topic'),
]
