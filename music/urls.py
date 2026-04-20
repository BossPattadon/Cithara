from django.urls import path
from music import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_song, name='create_song'),
    path('generate/', views.generate_song, name='generate_song'),
    path('song/<int:song_id>/status/', views.song_status, name='song_status'),
    path('song/<int:song_id>/status/api/', views.check_status_api, name='check_status_api'),
    path('song/<int:song_id>/', views.song_detail, name='song_detail'),
    path('song/<int:song_id>/delete/', views.delete_song, name='delete_song'),
    path('song/<int:song_id>/download/', views.download_song, name='download_song'),
    path('song/<int:song_id>/share/', views.create_share_link, name='create_share_link'),
    path('library/', views.library, name='library'),
    path('share/<uuid:token>/', views.shared_song, name='shared_song'),
]
