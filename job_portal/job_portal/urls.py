"""
URL configuration for job_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from job import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('login',views.logins,name="login"),
    path('logout',views.logouts,name="logouts"),
    path('adminhome',views.adminhome,name="Adminhome"),
    path('companyhome',views.companyhome,name="Companyhome"),
    path('add_department',views.add_department,name="add_department"),
    path('depart_view',views.department_view,name="depart_view"),
    path('admin_user_view',views.admin_user_view,name="admin_user_view"),
    path('update-profile/<int:pk>/', views.admin_user_edit, name='update_profile'),
    path('delete-profile/<int:pk>/', views.admin_user_delete, name='delete_profile'),
    path('adminapp', views.adminapplic, name="adminapplic"), 
    path('add_company',views.add_company,name="add_company"),
    path('company_user_view',views.company_user_view,name="company_user_view"),
    path('company_view',views.company_view,name="company_view"),
    path('update_company/<int:id>/', views.update_company, name='update_company'),
    path('delete_company/<int:id>/', views.delete_company, name='delete_company'),
    path('userhome',views.userhome,name="userhome"),
    path('user_register',views.user_register,name="user_register"),
    path('user_view',views.user_view,name="user_view"),
    path('user_update',views.user_edit,name="user_edit"),
    path('userdelete',views.user_delete,name="user_delete"),
    path('admin_skill',views.admin_skill,name="admin_skill"),
    path('admin_skill_view',views.admin_skill_view,name="admin_skill_view"),
    path('select_skills',views.user_profile,name="select_skills"),
    path('user_profilsk',views.user_profilsk,name="user_profilsk"),
    path('remove_skill/<int:profile_id>/<int:skill_id>/',views.remove_skill, name='remove_skill'),
    path('create_job/', views.create_job, name="create_job"),
    path('jobs/', views.job_list, name='job_list'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job_view/', views.job_view, name="job_view"),
    path('job/<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
    path('update_job/<int:job_id>/', views.update_job, name='update_job'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('viewjobapply/',views.viewjobapply,name="viewjobapply")
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


