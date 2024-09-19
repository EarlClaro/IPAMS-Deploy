from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class Classification(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PSCEDClassification(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PublicationLevel(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AuthorRole(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ConferenceLevel(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BudgetType(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CollaborationType(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RecordType(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Record(models.Model):
    title = models.CharField(max_length=100)
    year_accomplished = models.CharField(max_length=30) #Year Started
    year_completed = models.CharField(max_length=30, default='', null=True, blank=True)
    abstract = RichTextField()
    classification = models.ForeignKey(Classification, on_delete=models.DO_NOTHING)
    psced_classification = models.ForeignKey(PSCEDClassification, on_delete=models.DO_NOTHING)

    # abstract_filename and abstract_filesize is supposed to be use when there will be a cloud storage
    # to be used in saving the files to prevent uploading the
    # file itself to the default django storage
    abstract_filename = models.CharField(max_length=150, default='', null=True, blank=True)
    abstract_filesize = models.IntegerField(default=0, null=True, blank=True)

    abstract_file = models.FileField(upload_to='abstract/', default='', null=True, blank=True)  # WHOLE RESEARCH PAPER
    is_ip = models.BooleanField(default=False)
    for_commercialization = models.BooleanField(default=False)
    community_extension = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    adviser = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, null=True, blank=True)
    record_type = models.ForeignKey(RecordType, on_delete=models.DO_NOTHING, null=True, blank=True, default=3)
    representative = models.CharField(max_length=100)
    code = models.CharField(max_length=100, default='', null=True, blank=True)
    is_marked = models.BooleanField(default=False) # marked for deletion
    reason = models.TextField() # reason for deleting the record
    access_count = models.IntegerField(default=0)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='created_records',
                                 null=True,
                                 blank=True)

    def setTitle(self, title):
        self.title = title
    def setYearAccomplished(self, year_accomplished):
        self.year_accomplished = year_accomplished

    def setYearCompleted(self, year_completed):
        self.year_completed = year_completed

    def setAbstract(self, abstract):
        self.abstract = abstract

    def setIp(self, is_ip):
        self.is_ip = is_ip

    def setCommercialization(self, for_commercialization):
        self.for_commercialization = for_commercialization

    def setIs_marked(self, is_marked):
        self.is_marked = is_marked

    def setAbstractFile(self, abstract_file):
        self.abstract_file = abstract_file

    def setReason(self, reason):
        self.reason = reason

    def setAdviser(self, adviser):
        self.adviser = adviser

    def setClassification(self, classification):
        self.classification = classification

    def setPscedClassification(self, pscedClassification):
        self.psced_classification = pscedClassification

    def setRecordType(self, recordType):
        self.record_type = recordType

    def setRecordFile(self, abstract_file):
        self.abstract_file = abstract_file

    def setAbstractFileSize(self, file_size):
        self.abstract_filesize = file_size
    def setAbstractFileName(self, file_name):
        self.abstract_filename = file_name

    def setRepresentative(self, representative):
        self.representative = representative

    def __str__(self):
        return self.title

class ResearchRecord(models.Model):
    proposal = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='proposal')
    research = models.ForeignKey(Record, on_delete=models.SET_NULL, related_name='research', null=True, blank=True)

    # def __str__(self):
    #     return self.research

class CheckedRecord(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    checked_by = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.record.title
    
class CheckedRecordComment(models.Model):
    checked_record = models.ForeignKey(CheckedRecord, on_delete=models.CASCADE)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

class Publication(models.Model):
    name = models.CharField(max_length=200, default='', null=True, blank=True)
    isbn = models.CharField(max_length=50, default='', null=True, blank=True)
    issn = models.CharField(max_length=50, default='', null=True, blank=True)
    isi = models.CharField(max_length=50, default='', null=True, blank=True)
    year_published = models.CharField(max_length=50, default='', null=True, blank=True)
    publication_level = models.ForeignKey(PublicationLevel, on_delete=models.DO_NOTHING, null=True, blank=True)
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    author_role = models.ForeignKey(AuthorRole, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Conference(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    venue = models.CharField(max_length=100)
    conference_level = models.ForeignKey(ConferenceLevel, on_delete=models.DO_NOTHING)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Budget(models.Model):
    budget_allocation = models.FloatField()
    funding_source = models.CharField(max_length=100)
    budget_type = models.ForeignKey(BudgetType, on_delete=models.DO_NOTHING)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.funding_source

class Collaboration(models.Model):
    industry = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    collaboration_type = models.ForeignKey(CollaborationType, on_delete=models.DO_NOTHING)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.institution

class Upload(models.Model):
    name = models.CharField(max_length=100)
    record_type = models.ForeignKey(RecordType, default=1, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class RecordUploadStatus(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RecordUpload(models.Model):
    file = models.FileField(upload_to='documents/', null=True, blank=True)

    # filename is supposed to be use when there will be a cloud storage
    # to be used in saving the files to prevent uploading the
    # file itself to the default django storage
    filename = models.CharField(max_length=150, default='')

    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    record_upload_status = models.ForeignKey(RecordUploadStatus, on_delete=models.CASCADE)
    is_ip = models.BooleanField(default=False)
    for_commercialization = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    version = models.PositiveIntegerField(default=1)
    is_approved = models.BooleanField(default=False)
    is_declined = models.BooleanField(default=False)

    @property
    def representative(self):
        return self.record.representative
    def __str__(self):
        return self.record.title + " - " + self.upload.name

class CheckedUpload(models.Model):
    comment = models.TextField()
    checked_by = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING)
    record_upload = models.ForeignKey(RecordUpload, on_delete=models.CASCADE)
    date_checked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.checked_by.username


class RecordDownloadRequest(models.Model):
    sent_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    is_marked = models.BooleanField(default=False) # if request is approved
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sent_by.username

class RecordAuthenticationPin(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='authentication_pins')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='authentication_pins_as_user')
    email = models.CharField(max_length=60, null=True)
    role = models.ForeignKey('accounts.UserRole', on_delete=models.CASCADE, default=7)
    pin = models.CharField(max_length=6)

    def __str__(self):
        return self.pin


class RecordFile(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, default=None, null=True, blank=True)
    record_file_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.file)
    

from django.db import models
from datetime import datetime, timedelta

class SubscriptionPlan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=50, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    duration_months = models.IntegerField(null=True)

    def __str__(self):
        return self.plan_name

class Subscription(models.Model):
    sub_id = models.AutoField(primary_key=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    user_id = models.ForeignKey('accounts.User', on_delete=models.CASCADE, default=None)
    plan_id = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, default=1)
    locked_plan_name = models.CharField(max_length=50)  # New field to lock plan name
    status = models.CharField(max_length=50, default='active')

    def __str__(self):
        return str(self.sub_id)

    def renew(self):
        self.start_date = datetime.now().date()
        if self.plan_id and self.plan_id.duration_months:
            self.end_date = self.start_date + timedelta(days=self.plan_id.duration_months * 30)
        else:
            self.end_date = self.start_date + timedelta(days=180)  # default to 6 months if no plan specified
        # Update locked plan name only during renewal
        self.locked_plan_name = self.plan_id.plan_name  
        self.status = 'active'
        self.save()
    def save(self, *args, **kwargs):
    
        if not self.locked_plan_name:
            self.locked_plan_name = self.plan_id.plan_name
        super().save(*args, **kwargs) 

    def is_near_end(self):
        return self.end_date <= datetime.now().date() + timedelta(days=7)

    class Meta:
        db_table = 'subscription'