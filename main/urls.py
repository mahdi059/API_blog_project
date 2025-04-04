from django.urls import path
from . import views


app_name = 'main'
urlpatterns = [
    # Blog
    path('blog/create/', views.CraeteBlogView.as_view()),
    path('blog/update/<int:pk>/', views.UpdateBlogView.as_view()),
    path('blog/delete/<int:pk>/', views.DeleteBlogView.as_view()),
    path('blog/list/', views.ListBlogView.as_view()),
    path('blog/GrantAccess/<int:user_id>/', views.GrantAccessToUserView.as_view()),
    path('blog/retrieve/<int:pk>/', views.RetrieveBlogView.as_view()),
    # Comment
    path('comment/create/', views.CreateCommentView.as_view()),
    path('comment/update/<int:pk>/', views.UpdateCommentView.as_view()),
    path('comment/delete/<int:pk>/', views.DeleteCommentView.as_view()),
    # Favorite
    path('favorite/add/<int:blog_id>/', views.AddBlogToFavoriteView.as_view()),
    path('favorite/remove/<int:blog_id>/', views.RemoveFavoriteView.as_view()),
    # search
    path('blog/search/', views.SearchBlogView.as_view(), name='search-blog'),
]
