from django.contrib import admin
from django.urls import path
from . import views

app_name = "file_management"

urlpatterns = [
    path('dashboard/', views.home_view, name='home_view'),
    path('personal-files/', views.personal_files_view, name='personal_files_view'),
    path('ipams-files/', views.ipams_files_view, name='ipams_files_view'),
    path('create_folder/', views.create_folder_view, name='create_folder'),
    # path('move_folder/<int:folder_id>/', views.move_folder_view, name='move_folder'),
    # path('delete_folder/<int:folder_id>/', views.delete_folder_view, name='delete_folder'),
    path('rename-file/<int:record_upload_id>/', views.rename_file, name='rename_file'),
    path('edit_profile/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('file_info/<int:pk>', views.file_info, name='file_info'),
    # path('download_file/<int:file_id>/', views.download_file, name='download_file'),
    path('classification/<int:folder_id>/', views.all_folders, name='all_folders'),
    # path('all-records/', views.view_all_records, name='all_records'),
    path('browse-files/', views.browse_files_view, name='browse_files_view'),
    path('classifications/', views.classification_list, name='classification_list'),
    path('pscedclassification/<int:subfolder_id>/', views.subfolders, name='subfolders'),
    path('all-records/', views.records_table, name='all_records'),
    # path('add-record-files/<int:record_id>/', views.add_record_files, name='add_record_files'),
    path('personal_files/folders/records/<int:record_id>/', views.record_detail, name='record_detail'),
    # path('record_increment_access/<int:record_id>/', views.increment_record_access, name='increment_record_access'),
    path('chart_data/', views.chart_view, name='chart_data'),
    path('psced_chart/', views.psced_chart_view, name='psced_chart'),  # Define the URL for psced_chart_view
    path('audits/', views.audit_logs, name='audits'),
    path('download_all_files/<int:record_id>/', views.download_all_files, name='download_all_files'),
    # path('count-marked-requests/', views.count_marked_requests, name='count-marked-requests'),
    # URL for logging record access
    path('log_record_access/<int:record_id>/', views.log_record_access, name='log_record_access'),
    path('download-abstract/<int:record_id>/', views.download_abstract_file, name='download_abstract_file'),
    path('download_record_file/<int:record_upload_id>/', views.download_record_file, name='download_record_file'),
    path('download_file/<int:record_upload_id>/', views.download_file, name='download_file'),
    path('record-detail/<int:record_id>/delete-file/<int:file_id>/', views.delete_record_file, name='delete_record_file'),
    # path('record-detail/<int:recordID>/increment-delete-count/<int:fileID>/', views.increment_delete_count, name='increment_delete_count'),
    #PersonalFiles
    path('create-folder/', views.add_personal_folder, name='personal_folder'),
    path('personal_files/folders/<int:folder_id>/', views.student_folders, name='student_folders'),
    path('audits/<str:category>/', views.get_events_by_category, name='get_events_by_category'),
    # path('audits/filter_by_date/<str:category>/<str:selected_date>/', views.filter_events_by_date, name='filter_by_date'),
    path('browse_files/', views.browse_file_student, name='browse_files'),
    path('personal_files/', views.personal_files_student, name='personal_files_student'),
    path('student_records/', views.student_records, name='student_records'),
    path('approved-projects/', views.approved_records_view, name='approved_projects'),
    path('declined-projects/', views.unapproved_records_view, name='declined_projects'),
    path('approved_downloads/', views.approved_downloads_view, name='approved_downloads'),
    path('declined_downloads/', views.declined_downloads_view, name='declined_downloads'),
    path('currently-login/', views.currently_login, name='currently_login'),
    path('logout/', views.logout_view, name='logout'),
    path('myrecords/', views.student_all_records, name='student_all_records'),
    path('personal_files/folders/records/attachments/<int:record_id>/', views.attachments_view, name='attachments'),
    path('personal_files/folders/records/attachments/attachment-files/<int:record_id>/<int:upload_id>/', views.attachment_files_view, name='attachment_files'),
    ]

