from django.contrib import admin
from django.urls import path, re_path

from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import thesisDetailView, ThesisCreate, ThesisUpdate, AdminThesisCreate, AdminThesisUpdate

from register import views as v

urlpatterns = [
    path('', views.index, name='home'),
    path('activate/<uidb64>/<token>/',v.activate, name='activate'),
    path('password_reset', v.password_reset_request, name="password_reset"),

    #Admin URLS
    path('admin/manageApproved/', views.manage_approved, name='manageApproved'),

    path('admin/uploadProject', AdminThesisCreate.as_view(), name='add'),
    path('admin/updateProject/<slug:slug>', AdminThesisUpdate.as_view(), name='edit_thesis'),
    path('admin/viewApproved/<slug:slug>', views.view_thesis, name='view_thesis'),
    path('admin/viewRejected/<slug:slug>', views.view_thesisreject, name='view_thesisreject'),

    path('admin/managePending/', views.manage_pending, name='managePending'),
    path('admin/evaluate/<slug:slug>', views.evaluate, name='evaluate'),

    path('admin/manageRejected/', views.manage_rejected, name='manageRejected'),

    path('admin/dashboard/', views.dashboard, name='dashboard'),

    path('admin/manageRequests/', views.manage_request, name='manageRequests'),
    path('admin/evaluateRequests/<request_id>', views.evaluate_request, name='evaluateRequests'),

    path('admin/registeredAccounts/', views.regAccounts, name='regAccounts'),
    path('admin/accountDetails/<user_id>', views.acc_details, name='acc_details'),

    path('admin/manageDepartment/', views.manage_dept, name='manage_dept'),
    path('admin/manageCourse/', views.manage_course, name='manage_course'),
    path('admin/editDepartment/<slug:slug>', views.edit_dept, name='edit_dept'),
    path('admin/editCourse/<slug:slug>', views.edit_course, name='edit_course'),

    path('profile_staff/', views.profile_staff, name='profile_staff'),

    #User URLS
    path('repository/', views.thesis, name='thesis'),
    path('repository/view/<slug:slug>/', thesisDetailView.as_view(), name='view_studthesis'),
    #path('repository/view/<project_id>', views.view_studthesiss, name='view_studthesis'),
    path('repository/tag/<slug:slug>/', views.tagged, name="tagged"),
    path('repository/course/<slug:slug>', views.course_sort, name='course_sort'),

    path('submit/', ThesisCreate.as_view(), name='submission'),
    path('resubmit/<slug:slug>', ThesisUpdate.as_view(), name='resubmit'),

    path('viewPDF/<slug:slug>', views.viewPDF, name='viewPDF'),
    path('profile/', views.profile, name='profile'),
    path('personal_repository/', views.personal_repo, name='personal_repo'),

    re_path(r'^media/(?P<path>.*)$', views.protected_serve, {'document_root': settings.MEDIA_ROOT}),

    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)