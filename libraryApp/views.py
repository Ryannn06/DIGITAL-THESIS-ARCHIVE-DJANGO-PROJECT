# Create your views here.
#Django Admin Username: Ryan  //  Password: ryan3000
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from django.db import transaction
from register import views

from django.views.static import serve

from django.contrib.auth import get_user_model, update_session_auth_hash
from .forms import *
from . models import *
from . models import thesisDB, RequestPDF
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.core.exceptions import PermissionDenied

from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView
from taggit.models import Tag

from django.urls import reverse_lazy

from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from datetime import datetime

from hitcount.views import HitCountDetailView

from taggit.models import Tag

#permission
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .decorator import *

from django.conf import settings
import os

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django import template
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

import csv


def page_not_found(request, exception):
    return render(request, "errors/404.html", {})

def index(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('admin/dashboard')

        elif request.user.is_student:
            return redirect('/repository')

        else:
            raise PermissionDenied()

    thesis_no = thesisDB.objects.filter(published_status='Approved').count()
    context = {
        'thesis_no':thesis_no
    }
    return render(request, 'Home.html', context)


def auth_login(request):
    if request.user.is_authenticated:
        return redirect('/')

    else:
        if request.method == 'POST':
            form = AuthenticationForm(request.POST)
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username,password=password)

            if user:
                if user.is_admin:
                    login(request,user)
                    return redirect('/admin/dashboard')

                elif user.is_superuser:
                    return redirect('/admin')

                else:
                    login(request,user)
                    return redirect('/')

            else:
                messages.error(request,'Username or password not correct')
                return redirect('/accounts/login')

        else:
            form = AuthenticationForm()
        return render(request,'registration/login.html',{'form':form})


@login_required(login_url='/accounts/login/')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


@login_required
@for_admin
def dashboard(request):
    user = get_user_model()

    new_book = thesisDB.objects.filter(date_created=timezone.now()).count()
    book_available = thesisDB.objects.filter(published_status='Approved').count()

    thesis_pending = thesisDB.objects.filter(published_status='Pending').count()
    thesis_reject = thesisDB.objects.filter(published_status='Rejected').count()

    pdfaccess_pending = RequestPDF.objects.filter(request_status='Pending').count()
    pdfaccess_approved = RequestPDF.objects.filter(request_status='Approved').count()

    new_user = user.objects.filter(date_joined=timezone.now()).count()
    active_user = user.objects.filter(is_active=True).count()

    total_dept = ColDept.objects.all().count()
    total_course = ColCourse.objects.all().count()

    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    content = {
        'new_book':new_book,
        'book_available':book_available,

        'thesis_pending': thesis_pending,
        'thesis_reject':thesis_reject,

        'active_user':active_user,
        'new_user':new_user,

        'total_dept':total_dept,
        'total_course':total_course,

        'pdfaccess_pending':pdfaccess_pending,
        'pdfaccess_approved': pdfaccess_approved,
        }
    return render(request, 'Dashboard.html', content)



@login_required
@for_admin
def manage_approved(request):
    data = thesisDB.objects.filter(published_status='Approved').prefetch_related('thesis')
    approve_no = thesisDB.objects.filter(published_status='Approved').count()

    course = ColCourse.objects.annotate(count = Count('thesisdb', filter=Q(thesisdb__published_status='Approved'))).order_by('course_name')

    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    thesisdetail_ = {
        "thesis_details": data,
        'approve_no':approve_no,
        'course':course,
        }

    return render(request, 'ManageApproved.html', thesisdetail_)


@login_required
@for_admin
def manage_pending(request):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    to_approve = thesisDB.objects.filter(published_status='Pending').prefetch_related('thesis')
    pending_no = thesisDB.objects.filter(published_status='Pending').count()

    course = ColCourse.objects.annotate(count = Count('thesisdb', filter=Q(thesisdb__published_status='Pending'))).order_by('course_name')
    
    thesisdetail_ = {
        "details":to_approve,
        "pending_no":pending_no,
        "course": course,
        }

    return render(request, 'ManagePending.html', thesisdetail_)


@login_required
@for_admin
def manage_rejected(request):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    rejected = thesisDB.objects.filter(published_status='Rejected').prefetch_related('thesis')
    reject_no = thesisDB.objects.filter(published_status='Rejected').count()
    course = ColCourse.objects.annotate(count = Count('thesisdb', filter=Q(thesisdb__published_status='Rejected'))).order_by('course_name')

    thesisdetail_ = {
        'rejected':rejected,
        'reject_no':reject_no,
        'course': course,
        }

    return render(request, 'ManageReject.html', thesisdetail_)


@login_required
@for_admin
def view_thesis(request, slug):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    detail = get_object_or_404(thesisDB.objects.prefetch_related('thesis'), slug=slug, published_status='Approved')
    return render(request, 'AdminThesisDetails.html', {'detail':detail,})


@login_required
@for_admin
def view_thesisreject(request, slug):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    detail = get_object_or_404(thesisDB.objects.prefetch_related('thesis'), slug=slug, published_status='Rejected')
    return render(request, 'AdminThesisDetails.html', {'detail':detail,})


@login_required
@for_admin
def evaluate(request, slug):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    details =  get_object_or_404(thesisDB.objects.prefetch_related('thesis'), slug=slug, published_status='Pending')

    form = EvaluateThesisForm(request.POST or None, instance = details)
    if form.is_valid():
        form.save()
        if form.instance.published_status == 'Approved':
            message_window = "Thesis entitled %s has been approved successfully!" % (form.instance.title)
        elif form.instance.published_status == 'Rejected':
            message_window = "Thesis entitled %s has been rejected successfully!" % (form.instance.title)
        else:
            message_window = "Something went wrong."

        to_email = form.instance.uploaded_by.email
        user = form.instance.uploaded_by.first_name
        thesis_title = form.instance.title
        result = form.instance.published_status

        current_site = get_current_site(request)

        mail_subject = 'Your Thesis Project Has Been %s' % result

        plaintext = template.loader.get_template('tostudent_emails/evaluation_result_email.txt')
        htmltemp = template.loader.get_template('tostudent_emails/evaluation_result_email.html')

        message = {
            'user': user,
            'thesis': thesis_title,
            'result': result,
            'domain': current_site.domain,
            'protocol': 'http',
        }

        text_content = plaintext.render(message)
        html_content = htmltemp.render(message)

        email = EmailMultiAlternatives(
                    mail_subject, text_content,"Thesis Archive <do_not_reply@domain.example>", to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        messages.success(request, message_window )
        return redirect ('/admin/managePending/')

    return render(request, 'EvaluateProject.html', {'detail': details, 'form':form,})


@login_required
@for_admin
def regAccounts(request):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    user = get_user_model()
    account = user.objects.filter(is_superuser=False)

    context = {
        'account':account,
    }
    return render(request, 'ManageRegisteredAccounts.html', context)



@login_required
@for_admin
def manage_course(request):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    data = ColCourse.objects.all()

    if request.method == "POST":
        form = courseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            message = "%s course has been added successfully!" % form.instance.course_name
            messages.success(request, message )
            return redirect('/admin/manageCourse')
    else:
        form = courseForm()

    context = {
                'form':form,
                'course':data,
    }
    return render(request,'AdminManageCourse.html', context )



@login_required
@for_admin
def edit_course(request, slug):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    detail = get_object_or_404(ColCourse, slug=slug)
    form = courseForm(request.POST or None, instance = detail)
    if form.is_valid():
        form.save()
        message = "%s course has been updated successfully!" % form.instance.course_name
        messages.success(request, message )
        return redirect ('/admin/manageCourse')
    return render(request, 'AdminEditCourse.html', {'detail': detail, 'form':form })


@login_required
@for_admin
def delete_course(request, slug):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    course = get_object_or_404(ColCourse, slug=slug)
    thesis = thesisDB.objects.filter(course= course.id)
    course_name = course.course_name
    
    if thesis.exists():
        message = "You cannot delete %s as %s manuscript/s is/are found registered under this." % (course_name, str(len(thesis)))
        messages.error(request, message)
    else:
        course.delete()
        message = "The %s has successfully been deleted." % (course_name)
        messages.success(request, message)

    return redirect ('/admin/manageCourse')


@login_required
@for_admin
def manage_dept(request):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    data = ColDept.objects.all() #readd

    if request.method == "POST":  #add
        form = departmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            message = "%s department has been added successfully!" % form.instance.department_name
            messages.success(request, message )
            return redirect('/admin/manageDepartment')
    else:
        form = departmentForm()

    context = {
                'form':form,
                'department':data,
    }
    return render(request,'AdminManageDepartment.html', context )


@login_required
@for_admin
def edit_dept(request, slug):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    detail = get_object_or_404(ColDept, slug=slug)
    form = departmentForm(request.POST or None, instance = detail)
    if form.is_valid():
        form.save()

        message = "%s department has been updated successfully!" % form.instance.department_name
        messages.success(request, message )
        return redirect ('/admin/manageDepartment')
    return render(request, 'AdminEditDepartment.html', {'detail': detail, 'form':form })


@login_required
@for_admin
def delete_dept(request, slug):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    department = get_object_or_404(ColDept, slug=slug)
    course = ColCourse.objects.filter(coldep_id= department.id)
    department_name = department.department_name
    
    if course.exists():
        message = "You cannot delete the department of %s as %s course/s is/are found registered under this." % (department_name, str(len(course)))
        messages.error(request, message)
    else:
        department.delete()
        message = "The department of %s has successfully been deleted." % (department_name)
        messages.success(request, message)

    return redirect ('/admin/manageDepartment')


@login_required
@for_admin
def profile_staff(request):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    if request.method == 'POST':
        user_form = UpdateUserStaffForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully!" )
            return redirect('/profile_staff')
    else:
        user_form = UpdateUserStaffForm(instance=request.user)

    return render(request, 'StaffProfile.html', {'user_form':user_form})



@login_required
@for_admin
def manage_request(request):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    requests = RequestPDF.objects.filter(request_status='Pending')
    approved = RequestPDF.objects.filter(request_status='Approved')
    declined = RequestPDF.objects.filter(request_status='Declined')

    context = {
        'details':requests,
        'approved':approved,
        'declined':declined,
    }
    return render(request, 'ManageRequests.html', context)


@login_required
@for_admin
def evaluate_request(request, request_id):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    current_time = datetime.now()
    requests = get_object_or_404(RequestPDF.objects.prefetch_related('thesis'), id=request_id, request_status='Pending')

    form = EvaluateRequestForm(request.POST or None, instance=requests)
    if form.is_valid():
        form.instance.date_evaluated = current_time
        post = form.save()

        to_email = form.instance.user.email
        user = form.instance.user.first_name
        thesis_title = form.instance.thesis.title
        slug = form.instance.thesis.slug
        result = form.instance.request_status

        current_site = get_current_site(request)

        plaintext = template.loader.get_template('tostudent_emails/pdfrequest_result_email.txt')
        htmltemp = template.loader.get_template('tostudent_emails/pdfrequest_result_email.html')

        mail_subject = 'Your PDF Access Request Has Been %s' %result
        message = {
            'user': user,
            'thesis': thesis_title,
            'result': result,
            'domain': current_site.domain,
            'protocol': 'http',
            'slug':slug,
        }

        text_content = plaintext.render(message)
        html_content = htmltemp.render(message)

        email = EmailMultiAlternatives(
                    mail_subject, text_content,"Thesis Archive <do_not_reply@domain.example>", to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        message = "The pdf access request of %s for the thesis %s has been %s successfully!" % (user, thesis_title, result)
        messages.success(request, message )
        return redirect('/admin/manageRequests')

    return render(request, 'EvaluateRequests.html', {'details':requests,'form':form,})


@login_required
@for_admin
def acc_details(request, user_id):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    account = get_user_model()
    reg_acc = get_object_or_404(account, pk=user_id)
    submitted_projects = thesisDB.objects.filter(uploaded_by=user_id)

    content = {
        'reg_acc': reg_acc,
        'projects': submitted_projects
    }

    return render(request, 'AdminAccDetails.html', content)


@login_required
@for_admin
def disable_account(request, user_id):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    accounts = get_user_model()
    
    user = get_object_or_404(accounts, id=user_id, is_active=True, is_staff=False)
    user.is_active = False
    user.save()

    messages.success(request, 'Account has successfully been deactivated!')
    return redirect('/admin/registeredAccounts')


@login_required
@for_admin
def reactivate_account(request, user_id):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    accounts = get_user_model()
    
    user = get_object_or_404(accounts, id=user_id, is_verified=True, is_active=False)
    user.is_active = True
    user.save()

    messages.success(request, 'Account has successfully been reactivated!')
    return redirect('/admin/registeredAccounts')


@login_required
@for_students
def thesis(request):
    datas = thesisDB.objects.filter(published_status='Approved').order_by('-published_year', 'published_month').prefetch_related('thesis')

    course_thesiscount = ColCourse.objects.annotate(no_of_thesis = Count('thesisdb', filter=Q(thesisdb__published_status='Approved'))).order_by('course_name')
    popular_thesis = thesisDB.objects.filter(published_status='Approved').order_by('-hit_count_generic__hits')[:5]
    latest_thesis =  thesisDB.objects.filter(published_status='Approved').order_by('-date_created')[:5]

    search_bar = request.GET.get('search_paper')

    if search_bar != '' and search_bar is not None:
        datas = datas.filter(Q(title__icontains=search_bar)|  Q(thesis__first_name__icontains=search_bar) |  Q(thesis__last_name__icontains=search_bar) | Q(adviser__icontains=search_bar)  |  Q(abstract__icontains=search_bar) |  Q(published_year__icontains=search_bar)).distinct()

    tags = Tag.objects.annotate(no_of_thesis = Count('thesisdb', filter=Q(thesisdb__published_status='Approved')))

    context = {
        "department" : course_thesiscount,
        "popular_thesis": popular_thesis,
        "thesis_details_latest": latest_thesis,
        "tags":tags,
        "search_paper": search_bar,
        "result": datas,
        }
    return render(request, 'Thesis.html', context)


@login_required
@for_students
def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    post = thesisDB.objects.filter(tags=tag, published_status='Approved').order_by('-published_year', 'published_month').prefetch_related('thesis')

    search_bar = request.GET.get('search_paper')

    if search_bar != '' and search_bar is not None:
        post = post.filter(Q(title__icontains=search_bar)|  Q(thesis__first_name__icontains=search_bar) |  Q(thesis__last_name__icontains=search_bar) | Q(adviser__icontains=search_bar)  |  Q(abstract__icontains=search_bar) |  Q(published_year__icontains=search_bar)).distinct()

    page = request.GET.get('page', 1)

    paginator = Paginator(post, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'tag':tag,
        'thesis_details':posts,
        'search_paper':search_bar,
    }
    return render(request, 'TaggedThesis.html', context)


@login_required
@for_students
def course_sort(request, slug):
    datas = thesisDB.objects.filter(course_id__slug = slug, published_status='Approved').order_by('-published_year', 'published_month').prefetch_related('thesis')

    course_what = get_object_or_404(ColCourse, slug=slug)

    search_bar = request.GET.get('search_paper')

    if search_bar != '' and search_bar is not None:
        datas = datas.filter(Q(title__icontains=search_bar)|  Q(thesis__first_name__icontains=search_bar) |  Q(thesis__last_name__icontains=search_bar) | Q(adviser__icontains=search_bar)  |  Q(abstract__icontains=search_bar) |  Q(published_year__icontains=search_bar)).distinct()

    page = request.GET.get('page', 1)

    paginator = Paginator(datas, 10)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    context = {
        "thesis_course_details": data,
        "course_what": course_what,
        "search_paper":search_bar,
        }

    return render(request, 'CourseThesis.html', context)


@method_decorator([login_required, for_students], name='dispatch')
class thesisDetailView(HitCountDetailView):

    model = thesisDB
    template_name = 'ThesisDetails.html'
    context_object_name = 'detail'

    # set to True to count the hit
    count_hit = True

    #Check if thesis to view is approved
    def get_object(self, queryset=None):
        obj = super(thesisDetailView, self).get_object(queryset)
        if obj.published_status != 'Approved':
            raise PermissionDenied()
        else:
            return obj

    def get_context_data(self, **kwargs):
        context = super(thesisDetailView, self).get_context_data(**kwargs)
        print(self.get_object().thesis_id)
        context.update({
        'authors': Authors.objects.filter(thesis=self.get_object().thesis_id)
        #'other_published' : thesisDB.objects.filter(uploaded_by=self.get_object().uploaded_by, published_status='Approve').exclude(thesis_id=self.get_object().thesis_id).order_by('published_date'),
        #'department' : ColCourse.objects.all().order_by('course_name'),
        #'thesis_details_latest' :  thesisDB.objects.filter(published_status='Approve').order_by('published_date')[:5],
        })
        return context


@login_required
@for_students
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully!" )
            return redirect('/')
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'MyProfile.html', {'user_form':user_form})



@login_required
@for_students
def personal_repo(request):
    thesis = thesisDB.objects.filter(uploaded_by=request.user).prefetch_related('thesis').order_by('-date_created')

    context = {
        'thesis':thesis,
    }

    return render(request, 'my_repo.html', context)


@login_required
@for_students
def viewPDF(request, slug):

    #get thesis project
    project = get_object_or_404(thesisDB, slug=slug, published_status='Approved' )

    if request.user == project.uploaded_by:
            return render(request,'PDFViewer.html', {'detail':project})

    else:
        try:
            requestPDF = RequestPDF.objects.filter(user=request.user.pk, thesis=project.thesis_id).order_by('-request_date')[:1].get()

            if requestPDF.request_status == 'Pending':
                return render(request,'PendingRequestPDF.html', {'detail':project})

            elif requestPDF.request_status == 'Approved':
                return render(request,'PDFViewer.html', {'detail':project})

            elif requestPDF.request_status == 'Declined':
                messages.error(request, "Your request to access this pdf file has been declined may due to your invalid reason. Submit a new request with valid reason if you wish so." )

                if request.method == 'POST':
                    form = SendRequestForm(request.POST)
                    if form.is_valid():
                        form.instance.user = request.user
                        form.instance.thesis = project
                        post = form.save()
                        messages.success(request, "Request has been submitted successfully! We will notify you through email once the request is evaluated" )
                        return redirect('/repository')
                else:
                    form = SendRequestForm()
                return render(request,'SendRequestPDF.html',{'form':form, 'detail':project})

            else:
                raise PermissionDenied()

        except (RequestPDF.DoesNotExist) :
            #allow user to submit request if not then
            if request.method == 'POST':
                form = SendRequestForm(request.POST)
                if form.is_valid():
                    form.instance.user = request.user
                    form.instance.thesis = project
                    post = form.save()
                    messages.success(request, "Request has been submitted successfully! We will notify you through email once the request is evaluated" )
                    return redirect('/repository')
            else:
                form = SendRequestForm()
            return render(request,'SendRequestPDF.html',{'form':form, 'detail':project})


@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):

    user = request.user

    if user.is_staff and user.is_admin:
        return serve(request, path, document_root, show_indexes)

    else:
        path_new = f"pdf/{path}"
        print('this is the path:', path)
        thesis = get_object_or_404(thesisDB, pdf=path)

        if user == thesis.uploaded_by:
            return serve(request, path, document_root, show_indexes)

        else:
            try:
                pdf_status = RequestPDF.objects.filter(user=request.user.pk, thesis=thesis.thesis_id).order_by('-request_date')[:1].get()

                if pdf_status.request_status == 'Approved':
                    return serve(request, path, document_root, show_indexes)

                else:
                    raise PermissionDenied()

            except (pdf_status.DoesNotExist):
                raise PermissionDenied()


class ThesisInline():
    form_class = thesisForm
    model = thesisDB
    template_name = "StudentSubmitProject.html"

    def get_object(self, queryset=None):
        obj = super(ThesisInline, self).get_object(queryset)
        if obj.published_status == 'Approved':
            raise PermissionDenied()
        else:
            return obj

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        if form.instance.published_status == 'Rejected':
            form.instance.published_status = 'Pending'
            form.instance.date_created = datetime.now()
            form.instance.previous_reason = form.instance.reason
            form.instance.reason = None

        title = form.instance.title
        form.instance.uploaded_by = self.request.user

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()

        if self.object:
            message = "Your thesis entitled %s has been submitted successfully! We will notify you through email if it is once evaluated" % title
        else:
            message = "Your thesis entitled %s has been submitted successfully! We will notify you through email if it is once evaluated" % title

        messages.success(self.request, message )
        return redirect('/personal_repository')

    def formset_variants_valid(self, formset):
           """
           Hook for custom formset saving.Useful if you have multiple formsets
           """
           variants = formset.save(commit=False)  # self.save_formset(formset, contact)
           # add this 2 lines, if you have can_delete=True parameter
           # set in inlineformset_factory func
           for obj in formset.deleted_objects:
               obj.delete()
           for variant in variants:
               variant.thesis = self.object
               variant.save()


@method_decorator([login_required, for_students], name='dispatch')
class ThesisCreate(ThesisInline, CreateView):
    def get_context_data(self, **kwargs):
        ctx = super(ThesisCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'variants': AuthorFormSet(prefix='variants'),
            }
        else:
            return {
                'variants': AuthorFormSet(self.request.POST or None, self.request.FILES or None, prefix='variants'),
            }


@method_decorator([login_required, for_students], name='dispatch')
class ThesisUpdate(ThesisInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(ThesisUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'variants': AuthorFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='variants'),
        }


class AdminThesisInline():
    form_class = AdminthesisForm
    model = thesisDB
    template_name = "AddProject.html"

    def get_object(self, queryset=None):
        obj = super(AdminThesisInline, self).get_object(queryset)
        if obj.published_status == 'Rejected' or obj.published_status == 'Pending' :
            raise PermissionDenied()
        else:
            return obj

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))


        form.instance.published_status = 'Approved'
        form.instance.submission_agreement = True

        title = form.instance.title
        if not self.object:
            form.instance.uploaded_by = self.request.user
        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()

        if self.object:
            message = "Thesis project entitled %s has been updated successfully!" % title
        else:
            message = "Thesis project entitled %s has been uploaded successfully!" % title

        messages.success(self.request, message )
        return redirect('/admin/manageApproved')

    def formset_variants_valid(self, formset):
           """
           Hook for custom formset saving.Useful if you have multiple formsets
           """
           variants = formset.save(commit=False)  # self.save_formset(formset, contact)
           # add this 2 lines, if you have can_delete=True parameter
           # set in inlineformset_factory func
           for obj in formset.deleted_objects:
               obj.delete()
           for variant in variants:
               variant.thesis = self.object
               variant.save()

@method_decorator([login_required, for_admin], name='dispatch')
class AdminThesisCreate(AdminThesisInline, CreateView):
    def get_context_data(self, **kwargs):
        ctx = super(AdminThesisCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'variants': AuthorFormSet(prefix='variants'),
            }
        else:
            return {
                'variants': AuthorFormSet(self.request.POST or None, self.request.FILES or None, prefix='variants'),
            }

@method_decorator([login_required, for_admin], name='dispatch')
class AdminThesisUpdate(AdminThesisInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(AdminThesisUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'variants': AuthorFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='variants'),
        }
        

@login_required
@for_students
def personal_access(request):
    appdf_access = RequestPDF.objects.filter(request_status='Approved', user=request.user).prefetch_related('thesis')
    pendpdf_access = RequestPDF.objects.filter(request_status='Pending', user=request.user).prefetch_related('thesis')

    context = {
        'pendpdf_access': pendpdf_access,
        'appdf_access': appdf_access,
    }

    return render(request, 'MyAccess.html', context)


@login_required
@for_admin
def approvedprojects_csv(request):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)

    writer.writerow(['Title', 'Authors', 'Adviser', 'Course', 'Published Year', 'Published Month', 'Date Uploaded', 'Uploadeder'])

    projects = thesisDB.objects.filter(published_status='Approved').prefetch_related('thesis').values_list('title', 'thesis__last_name',  'adviser', 'course', 'published_year', 'published_month', 'date_created', 'uploaded_by').order_by('title')
    
    for project in projects:  
        writer.writerow(project)
    
    response['Content-Disposition'] =  'attachment; filename = "Approved_Thesis_Projects.csv"'
    return response


@login_required
@for_admin
def regaccs_csv(request):
    request.session['pending_thesis'] = thesisDB.objects.filter(published_status='Pending').count()
    request.session['pending_pdfrequest'] = RequestPDF.objects.filter(request_status='Pending').count()
    
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)

    writer.writerow(['First Name', 'Last Name', 'Email', 'Email Verified', 'Date Joined'])

    users = get_user_model()
    accounts = users.objects.filter(is_student=True).values_list('first_name', 'last_name', 'email', 'is_active', 'date_joined').order_by('first_name')
    
    for account in accounts:  
        writer.writerow(account)
    
    response['Content-Disposition'] =  'attachment; filename = "Registered_Accounts.csv"'
    return response


@login_required
@for_students
def delete_thesis(request, slug):
    thesis = get_object_or_404(thesisDB, Q(published_status='Pending') | Q(published_status='Rejected'), uploaded_by=request.user, slug=slug) 
    thesis.delete()

    message = "Thesis has successfully been deleted!"
    messages.success(request, message)

    return redirect('/personal_repository')