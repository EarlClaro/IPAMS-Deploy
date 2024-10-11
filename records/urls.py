from django.conf.urls.static import static
from django.urls import path

from ipams import settings
from . import views
from .views import SubscriptionPageView
from .views import PaymentPortalView
from .views import renew_subscription, cancel_subscription
from .views import check_verification_status
from .views import update_api_key
from .views import update_subscription_plan
from .views import fetch_subscriptions
urlpatterns = [
    path('', views.Home.as_view(), name='records-index'),
    path('record/publishedRecords', views.PublishedRecords.as_view(), name='records-publish'),
    path('dashboard', views.Dashboard.as_view(), name='records-dashboard'),
    path('dashboard/manage/documents', views.ViewManageDocuments.as_view(), name='dashboard-manage-documents'),
    path('dashboard/manage/documents/record/<int:record_id>', views.ViewManageDocumentsRecord.as_view(), name='dashboard-manage-documents-record'),
    path('dashboard/manage/records', views.ViewManageRecords.as_view(), name='dashboard-manage-records'),
    path('dashboard/logs', views.LogsView.as_view(), name='dashboard-logs'),
    path('dashboard/manage/records/<int:record_id>', views.DashboardManageRecord.as_view(), name='dashboard-manage-record'),
    path('dashboard/manage/accounts', views.DashboardManageAccounts.as_view(), name='dashboard-manage-accounts'),
    path('dashboard/logs/record/<int:record_id>', views.DashboardLogsRecordView.as_view(), name='dashboard-logs-record'),
    path('record/<int:record_id>', views.ViewRecord.as_view(), name='records-view'),
    path('record/myrecords/<int:record_id>', views.MyRecordView.as_view(), name='records-myrecords-view'),
    
    #Upload Controller
    path('record/uploads/getUploadDocument/', views.UploadController.as_view(), name='get-upload-document'),
    path('record/uploads/createComment/', views.UploadController.as_view(), name='create-comment'),

    #View Record
    path('record/recordFile/<int:record_id>', views.ViewRecordFile.as_view(), name='view-record-file'),

    #Evaluation
    path('record/evaluation/<int:record_id>', views.EvaluationView.as_view(), name='records-evaluation-view'),
    path('record/evaluation/removeRecord/', views.EvaluationController.as_view(), name='remove-record'),
    path('record/evaluation/evaluateRecord/', views.EvaluationController.as_view(), name='evaluate-record'),

    path('record/approved/<int:record_id>', views.ApprovedRecordView.as_view(), name='records-approved-view'),
    path('record/declined/<int:record_id>', views.DeclinedRecordView.as_view(), name='records-declined-view'),

    #Add records URLs
    path('add/', views.AddRecordView.as_view(), name='records-add'),
    path('add/getUserList/', views.AddRecordController.as_view(), name='get-user-list'),
    path('add/getAdviserList/', views.AddRecordController.as_view(), name='get-adviser-list'),
    path('add/createRecord/', views.AddRecordController.as_view(), name='create-record'),
    path('add/createThesis/', views.AddResearchController.as_view(), name='create-thesis'),

    path('add/research/<int:research_record_id>', views.AddResearch.as_view(), name='records-add-research'),
    path('edit/<int:record_id>', views.Edit.as_view(), name='records-edit'),
    path('uploadexcel/', views.ParseExcel.as_view(), name='records-upload'),
    path('downloadformat/', views.download_format, name='records-download-format'),
    path('download/abstract/<int:record_id>', views.download_abstract, name='records-download-abstract'),
    path('download/document/<int:record_upload_id>', views.download_document, name='records-download-document'),

    #My record URLS
    path('records/user/', views.MyRecordsView.as_view(), name='records-myrecords'),
    path('records/user/getMyRecordsList/', views.MyRecordsController.as_view(), name='get-myrecords-list'),
    path('records/user/getComment/', views.MyRecordsController.as_view(), name='get-comments'),

    path('records/pending/', views.PendingRecordsView.as_view(), name='records-pending'),
    path('records/requests/', views.PendingRequestsView.as_view(), name='records-requests'),
    path('records/approved/', views.ApprovedRecordsView.as_view(), name='records-approved'),
    path('records/declined/', views.DeclinedRecordsView.as_view(), name='records-declined'),
    # path('records/approvedAttachments/', views.ApprovedAttachmentsView.as_view(), name='records-approvedAttachments'),
    path('records/approvedAttachments/', views.approve_attachments_view, name='records-approvedAttachments'),
    path('records/declinedAttachments/', views.decline_attachments_view, name='records-declinedAttachments'),
    # path('records/declinedAttachments/', views.DeclinedAttachmentsView.as_view(), name='records-declinedAttachments'),
    path('records/pendingAttachments/', views.pending_attachments_view, name='records-pendingAttachments'),
    # path('records/pendingAttachments/', views.PendingAttachmentsView.as_view(), name='records-pendingAttachments'),
    path('records/approved-attachments/<int:checked_upload_id>/', views.approve_attachments, name='approved-attachments'),
    path('records/declined-attachments/<int:checked_upload_id>/', views.decline_attachments, name='declined-attachments'),
    path('file_management/view_file_content/<int:record_upload_id>/', views.view_file_content, name='view_file_content'),
    path('download_docx_file/<int:record_upload_id>/', views.download_docx_file,
         name='download_docx_content'),
    path('get_file_type/<int:record_upload_id>/', views.get_file_type, name='get_file_type'),

    path('lockout', views.LockoutPage.as_view(), name='lockout-page'),
    path('manage/manageAccounts', views.ManageAccounts.as_view(), name='manage-accounts'),
    path('dashboard/reset/accounts', views.LockedAccountsView.as_view(), name='reset-accounts'),
    path('delete/requests', views.get_all_delete_requests, name="all-delete-requests"),
    path('record/pending/delete/request/<int:record_id>', views.PendingDeleteRecordsView.as_view(), name='pending-delete-view'),
    path('download/requests', views.get_all_download_requests, name="all-download-requests"),
    path('approved/download/request', views.approved_download_requests, name="download-request"),

    #Security - Record Pin
    path('records/pinrecords/<int:record_id>', views.AuthenticationPinView.as_view(), name='records-authentication'),
    path('generate-pin-and-save/', views.generate_pin_and_save_data_view, name='generate-pin-and-save'),

    #Subscribe
    
     path('subscribe/', SubscriptionPageView.as_view(), name='subscribe'),
     path('payment/', PaymentPortalView.as_view(), name='payment_portal'),
     path('create_payment_link/', views.create_payment_link_view, name='create_payment_link'),
     path('get_payment_link_and_check_status/',views.get_payment_link_and_check_status,name='get_payment_link_and_check_status'),
     path('verify_subscription/', views.verify_subscription, name='verify_subscription'),
     path('renew_subscription/', renew_subscription, name='renew_subscription'),
     
     path('cancel_subscription/', cancel_subscription, name='cancel_subscription'),
     path('check-verification-status/', check_verification_status, name='check_verification_status'),
     path('update-price/', views.update_price, name='update_price'),
    # path('subscription-plans/', views.subscription_plans_view, name='subscription_plans'),
    # path('subscribe_view/', views.subscribe_view, name='subscribe_view'),
     #Chatbot
     
     path('update-api-key/', update_api_key, name='update-api-key'),
     path('manage_subscriptions/', views.manage_subscriptions, name='manage_subscriptions'),
     path('subscribed_users/', views.subscribed_users, name='subscribed_users'),
     path('update_subscription_plan/', update_subscription_plan, name='update_subscription_plan'),
     path('fetch_subscriptions/', fetch_subscriptions, name='fetch_subscriptions'),
     path('subscribe/free-trial/', views.subscribe_free_trial, name='subscribe_free_trial'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)