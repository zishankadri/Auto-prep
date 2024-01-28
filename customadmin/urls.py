from django.urls import path, include

from . import views

urlpatterns = [
    # Navigation ->
    #  - Admin Dashboard URL
    path('', views.dashboard_page, name="dashboard"),
    #  - Settings URL
    path('settings/', views.settings_page, name="settings"),


    # Tables (CRUD) ->
    #  - Create table (Create)
    path('create_row/<str:model_name>', views.create_row_page, name="create_row"),
    #  - Show table URL (Read)
    path('table/<str:model_name>', views.show_table_page, name="tables"),
    #  - Edit table URL (Update, Delete)
    path('edit_row/<str:model_name>/<str:id>', views.edit_row_page, name="edit_row"),
    #   - Show history
    path('history/<str:user_id>/', views.history_page, name="edit_row"),
    # path('get_chapters/<str:subject_id>/<str:level_id>', views.get_chapters, name="get_chapters"),
    path('get_chapters/', views.get_chapters, name="get_chapters"),


]

