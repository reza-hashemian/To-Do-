from django.urls import path, include

urlpatterns = [
    # path('blog/', include(('django_project.blog.urls', 'blog')))
    path('todo/', include(('django_project.ToDo.urls', 'Todo'))),
    path('auth/', include(('django_project.authentication.urls', 'blog'))),

]
