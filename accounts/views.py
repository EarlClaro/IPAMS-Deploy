from concurrent.futures import thread
from http.client import INTERNAL_SERVER_ERROR
import json
from threading import Thread
import requests
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import signals, authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import redirect
from ipams import settings
from . import forms
from .decorators import authorized_roles
from .models import User, UserRole, RoleRequest, Course, Student, Log, Setting, College, Department, Adviser, UserRecord
from records.models import CheckedRecord, Record, RecordUpload, CheckedUpload
from notifications.models import Notification, NotificationType
from accounts.auxfunctions import EmailThreading, roleRequestStudent, roleRequestAdviser
from django.db.models import Q, Subquery
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from axes.decorators import axes_dispatch
from records.models import Subscription, SubscriptionPlan
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

User = get_user_model()
from .tokens import activation_token
from django.db import connections

from axes.models import AccessAttempt, AccessBase
from axes.utils import reset
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import make_password


#custom function to check the request type since Httpis_ajax(request=request) method is deprecated.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils.crypto import get_random_string

class SignupView(View):
    name = 'accounts/signup.html'

    def get(self, request):
        form = forms.SignupForm()
        return render(request, self.name, {'form': form, 'hide_profile': True})

    def post(self, request):
        if is_ajax(request=request):
            # Handling AJAX requests
            if request.POST.get("get_courses", 'false') == 'true':
                courses = [{'value': course.name, 'id': course.pk} for course in Course.objects.all()]
                return JsonResponse({'courses': courses})
            elif request.POST.get("get_colleges", 'false') == 'true':
                colleges = [{'value': college.name, 'id': college.pk} for college in College.objects.all()]
                return JsonResponse({'colleges': colleges})
            elif request.POST.get("get_departments", 'false') == 'true':
                departments = [{'value': department.name, 'id': department.pk, 'college': department.college.name} for department in Department.objects.all()]
                return JsonResponse({'departments': departments})
            else:
                return JsonResponse({'success': 'false'})
        else:
            # Handling form submission
            form = forms.SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                password = form.cleaned_data.get('password')  # Retrieve the password

                # Generate a random salt for hashing
                salt = get_random_string(12)

                # Hash the password using the same salt
                hashed_password = make_password(password, salt=salt)

                # Set the hashed password for the IPAMS system
                user.password = hashed_password
                user.role = UserRole.objects.get(pk=1)
                user.is_active = False
                user.is_verified = False
                user.save()

                # Save the hashed password to the NALC system
                try:
                    with connections['nalc'].cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO backend_user (name, email, password, is_active, is_superuser, is_staff) VALUES (%s, %s, %s, %s, %s, %s)",
                            [user.username, user.email, hashed_password, 1, 0, 0]
                        )
                except Exception as e:
                    messages.error(request, _('Error occurred while saving user data to the other database: {}').format(str(e)))

                    

                role_id = int(request.POST.get('role', 0))
                if role_id == 2:  # Student
                    student_id = request.POST.get('student_id', None)
                    if not student_id:
                        messages.error(request, 'Student ID is required for student registrations.')
                        return render(request, self.name, {'form': form, 'hide_profile': True})

                    if Student.objects.filter(student_id=student_id).exists():
                        messages.error(request, 'This Student ID is already in use. Please use a different ID.')
                        return render(request, self.name, {'form': form, 'hide_profile': True})

                    try:
                        course_data = json.loads(request.POST.get('course'))
                        course = Course.objects.get(pk=course_data[0]['id'])
                        student = Student(user=user, course=course, student_id=student_id)
                        student.save()
                        roleRequestStudent(request, user.id)

                    except IntegrityError as e:
                        messages.error(request, f'A database error occurred: {str(e)}')
                        return render(request, self.name, {'form': form, 'hide_profile': True})
                  
                elif role_id == 3:  # Adviser
                    college = json.loads(request.POST.get('college'))
                    department = json.loads(request.POST.get('department'))
                    Adviser(user=user, department=Department.objects.get(pk=department[0]['id']),
                            college=College.objects.get(pk=college[0]['id'])).save()
                    roleRequestAdviser(request, user.id)

                # Saving role request
                RoleRequest(user=user, role=UserRole.objects.get(pk=role_id)).save()

                # Sending activation email
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string(
                    'accounts/account_active_email.html', {
                       'user': user,
                       'domain': current_site.domain,
                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                       'token': default_token_generator.make_token(user),
                    }
                )
                to_email = form.cleaned_data.get('email')
                send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=False)
                messages.success(request, 'Activate account by confirming your email address to complete the registration.')

                return redirect('/')
            else:
                error_message = 'Invalid form'
                if not form.cleaned_data.get('username'):
                    error_message = 'Username not available'
                elif not form.cleaned_data.get('email'):
                    error_message = 'That E-mail is already used by another user'
                messages.error(request, error_message)
            return render(request, self.name, {'form': form, 'hide_profile': True})

        
#For activation of user account through email
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist, ConnectionError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_verified = True

        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        messages.success(request, f'Welcome {user.username}. Thank you for your email confirmation. You are now logged in.')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('records-index')


from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

@method_decorator(axes_dispatch, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    name = 'ipams/base.html'

    def get(self, request):
        return render(request, self.name)

    def post(self, request):
        if request.method == 'POST':
            ''' reCAPTCHA validation '''
            # recaptcha_response = request.POST.get('g-recaptcha-response')
            # data = {
            #     'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            #     'response': recaptcha_response
            # }
            # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            # result = r.json()
            result = True
            ''' End reCAPTCHA validation '''

            if result or settings.TEST_FORM:
                form = forms.LoginForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data.get('username')
                    user = authenticate(
                        request=request,
                        username=form.cleaned_data.get('username'),
                        password=form.cleaned_data.get('password'),
                    )

                    if user:
                        if user.is_verified:
                            login(request, user)

                            # Generate JWT token
                            refresh = RefreshToken.for_user(user)
                            access_token = str(refresh.access_token)

                            # Store JWT token in session and as a cookie
                            request.session['jwt_token'] = access_token
                            response = redirect(request.POST.get('next', 'records-index'))
                            #response = JsonResponse({'message': f'Welcome {username}','access_token': access_token})
                            response.set_cookie('jwt_token', access_token, httponly=False, samesite='Strict')

                            # Add role-based notification logic here...
                            if request.user.role.id == 5: # rdco
                                notifications = Notification.objects.filter(Q(to_rdco=True) | Q(recipient=user.id))
                                request.session['notif_count'] = notifications.count()
                            elif request.user.role.id == 4: # ktto
                                notifications = Notification.objects.filter(Q(to_ktto=True) | Q(recipient=user.id))
                                request.session['notif_count'] = notifications.count()
                            elif request.user.role.id == 3: # adviser
                                notifications = Notification.objects.filter(Q(recipient=user.id) | Q(notif_type=NotificationType.objects.get(pk=6)) | Q(notif_type=NotificationType.objects.get(pk=1)) | Q(notif_type=NotificationType.objects.get(pk=2)))
                                request.session['notif_count'] = notifications.count()
                            elif request.user.role.id == 7: # tbi
                                notifications = Notification.objects.filter(Q(to_ktto=True) | Q(recipient=user.id))
                                request.session['notif_count'] = notifications.count()
                            elif request.user.role.id == 2: # student
                                notifications = Notification.objects.filter(recipient=user.id)
                                request.session['notif_count'] = notifications.count()

                            messages.success(request, f'Welcome {username}')
                            return response
                        else:
                            messages.error(request, 'Account is not activated yet. Please check your email address to verify.')
                    else:
                        messages.error(request, 'Invalid Username/Password')
            else:
                messages.error(request, 'Recaptcha is required')
        return redirect('records-index')

def logout(request):
    # IPAMS logout
    auth_logout(request)
    messages.success(request, 'You are now logged out from the system...')

    # Call NALC logout API
    nalc_logout_url = 'http://localhost:8000/api/logout/'
    try:
        response = requests.get(nalc_logout_url, cookies=request.COOKIES)
        if response.status_code == 200:
            print('Successfully logged out from NALC')
        else:
            print('Failed to log out from NALC')
    except Exception as e:
        print('Error logging out from NALC:', e)

    # Clear JWT token from cookies
    response = redirect('/')
    response.delete_cookie('authToken')
    return response


def change_password(request):
    if request.method == 'POST':
        password_old = request.POST.get('password-old', None)
        password_new = request.POST.get('password-new', None)
        if ((password_old is not None or password_old != '') and (password_new is not None or password_new != '')) and len(password_new) >= 8:
            if check_password(password_old, request.user.password):
                request.user.set_password(password_new)
                request.user.save()
                messages.success(request, "Password changed!")
            else:
                messages.error(request, 'Incorrect old password')
        else:
            messages.error(request, 'New password must be 8 characters longer')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@authorized_roles(roles=['adviser', 'ktto', 'rdco', 'itso', 'tbi'])
def get_all_accounts(request):
    if request.method == 'POST':
        accounts = None
        if request.user.role.name == 'Adviser':
            #accounts = User.objects.prefetch_related('role').filter(Q(role=UserRole.objects.get(pk=1)) | Q(role=UserRole.objects.get(pk=2))).prefetch_related('role')
            accounts = User.objects.prefetch_related('role').filter(role__lte=2)
        else:
            accounts = User.objects.prefetch_related('role').all()

        data = []
        for account in accounts:
            role = ''
            role_request = RoleRequest.objects.select_related('role').filter(user=account).first()
            if role_request and role_request.role.pk != 1:
                role = f'<a href="#" onclick="acceptRole({account.pk}, {role_request.role.pk})">{role_request.role.name}</a>'
            data.append([
                '',
                account.pk,
                str(account.username),
                f'{account.last_name}, {account.first_name} {account.middle_name}',
                account.role.name,
                role,
            ])
        return JsonResponse({'data': data})

def save_profile(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        contact_no = request.POST.get('contact_no')
        if first_name != '':
            user.first_name = first_name
        if middle_name != '':
            user.middle_name = middle_name
        if last_name != '':
            user.last_name = last_name
        if contact_no != '':
            user.contact_no = contact_no
        user.save()
    return JsonResponse({'message': 'success'})


@authorized_roles(roles=['adviser', 'ktto', 'rdco', 'tbi'])
def get_pending_count(request):
    if request.method == 'POST':
        if request.user.role.id == 3:
            records_with_adviser = Record.objects.filter(adviser=request.user.pk)
            new_record_rows = records_with_adviser.filter(
                Q(checkedrecord__isnull=True) | Q(checkedrecord__checked_by=request.user.pk, checkedrecord__status='pending')
            ).distinct().values('pk', 'title')
            delete_request_rows = ''
            # Modified part starts here
            # is_approved_count = RecordUpload.objects.filter(is_approved=False)

        elif request.user.role.id == 4 or request.user.role.id == 7:
            ktto_exclude = CheckedRecord.objects.select_related('record').filter(
                Q(checked_by__in=Subquery(User.objects.filter(role=4).values('pk'))) | Q(
                    checked_by__in=Subquery(User.objects.filter(role=7).values('pk')))).exclude(status='pending')
            ktto_include = CheckedRecord.objects.select_related('record').filter(status='approved',
                                                                                    checked_by__in=Subquery(
                                                                                        User.objects.filter(role=3).values(
                                                                                            'pk')))
            new_record_rows = Record.objects.filter(pk__in=Subquery(ktto_include.values('record'))).exclude(
                pk__in=Subquery(ktto_exclude.values('record'))).values('pk', 'title')
            delete_request_rows = Record.objects.filter(is_marked=True)

        elif request.user.role.id == 5:
            rdco_exclude = CheckedRecord.objects.select_related('record').filter(
                checked_by__in=Subquery(User.objects.filter(role=5).values('pk'))).exclude(status='pending')
            rdco_include = CheckedRecord.objects.select_related('record').filter(
                Q(checked_by__in=Subquery(User.objects.filter(role=4).values('pk'))) | Q(
                    checked_by__in=Subquery(User.objects.filter(role=7).values('pk'))), status='approved')
            new_record_rows = Record.objects.filter(pk__in=Subquery(rdco_include.values('record'))).exclude(
                pk__in=Subquery(rdco_exclude.values('record'))).values('pk', 'title')
            delete_request_rows = Record.objects.filter(is_marked=True)


        return JsonResponse({"pending-count": len(new_record_rows) + len(delete_request_rows) })


@authorized_roles(roles=['adviser', 'ktto', 'rdco', 'tbi'])
def get_pending_counts(request):
    if request.method == 'POST':
        pending_rows = CheckedUpload.objects.filter(comment='').count()

        context= {
        "pending-count": pending_rows,
        }

        return JsonResponse(context)


class HelpView(View):
    name = 'help/index.html'

    def get(self, request):
        return render(request, self.name)


class ManualView(View):
    name = 'help/manual.html'

    def get(self, request):
        return render(request, self.name)


class SettingsView(View):
    name = 'accounts/settings.html'

    @method_decorator(authorized_roles(roles=['ktto', 'rdco', 'tbi']))
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        context = {
            'landing_page': Setting.objects.get(name='landing_page'),
            'settings_form': forms.SettingsForm(instance=Setting.objects.get(name='landing_page')),
        }
        return render(request, self.name, context)

    def post(self, request):
        settings_form = forms.SettingsForm(request.POST, instance=Setting.objects.get(name='landing_page'))
        if settings_form.is_valid():
            settings_form.save()
        else:
            print('invalid')
        return redirect('accounts-settings')


@authorized_roles(roles=['adviser', 'ktto', 'rdco', 'itso', 'tbi'])
def get_all_locked_accounts(request):
    if request.method == 'POST':
        accounts = AccessAttempt.objects.all()
        data = []
        for account in accounts:
            data.append([
                '',
                account.attempt_time,
                account.username,
                account.failures_since_start
            ])
        return JsonResponse({'data': data})
    

User = get_user_model()  # Use the custom User model

def check_username_availability(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':  # Check for AJAX
        username = request.POST.get('username', '').strip()
        if User.objects.filter(username=username).exists():
            return JsonResponse({'available': False})  # Username is taken
        return JsonResponse({'available': True})  # Username is available
    return JsonResponse({'error': 'Invalid request'}, status=400)



User = get_user_model()

def check_email_availability(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        email = request.POST.get('email', '').strip()
        if User.objects.filter(email=email).exists():
            return JsonResponse({'available': False})  # Email is already registered
        return JsonResponse({'available': True})  # Email is available
    return JsonResponse({'error': 'Invalid request'}, status=400)



def check_student_id_availability(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        student_id = request.POST.get('student_id', '').strip()
        if Student.objects.filter(student_id=student_id).exists():
            return JsonResponse({'available': False})  # Student ID is already registered
        return JsonResponse({'available': True})  # Student ID is available
    return JsonResponse({'error': 'Invalid request'}, status=400)
