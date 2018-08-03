from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    # path('courses/', views.CourseListView.as_view(), name='courses'),
    path('courses/', views.coursesPage, name='courses'),
    path('courses/<int:pk>', views.course_detail_view, name='course-detail'),
    path('courses/<int:pk>/grades', views.grades_detail_view, name='grades-detail'),
    path('addcourse', views.add_course, name='add-course'),  
]