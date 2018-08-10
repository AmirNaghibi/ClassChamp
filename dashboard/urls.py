from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    # path('courses/', views.CourseListView.as_view(), name='courses'),
    path('courses/', views.coursesPage, name='courses'),
    path('courses/<int:pk>', views.course_detail_view, name='course-detail'),
    path('courses/<int:pk>/grades', views.grades_detail_view, name='grades-detail'),
    path('addcourse/', views.add_course, name='add-course'),
    path('addgrade/', views.add_grade, name='add-grade'),
    path('courses/<int:pk>/delete/<int:gradeID>', views.delete_grade, name='delete-grade'),
    #path('courses/<int:courseID>/grades/<int:gradeID>', views.delete_assessment, name='delete-assess'),
]