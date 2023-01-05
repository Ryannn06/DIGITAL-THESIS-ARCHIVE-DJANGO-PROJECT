from django.db import models
from django.db.models import Model
from django.db.models.functions import Lower

from taggit.managers import TaggableManager

from ckeditor.fields import RichTextField

from django.core.validators import RegexValidator

from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.core.validators import FileExtensionValidator

from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

import string 
from django.utils.text import slugify 
from .utils import unique_slugify

from django.utils import timezone

# Create your models here.
#py manage.py makemigrations
#py manage.py migrate

class ColDept(Model):
	department_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Department', unique=True)
	department_abbreviation = models.CharField(max_length=200, blank=True, null=True)
	slug = models.SlugField(max_length = 250, null = True, blank = True) 

	def save(self, *args, **kwargs):
		self.slug = slugify(self.department_name)
		super().save(*args, **kwargs)

	class Meta:
		db_table = 'col_dept'

	def __str__(self):
		department = str(self.department_name + " (" +self.department_abbreviation + ")")
		return department

class ColCourse(Model):
	course_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Course', unique=True)
	coldep_id = models.ForeignKey(ColDept, on_delete=models.CASCADE)
	slug = models.SlugField(max_length = 250, null = True, blank = True) 

	def save(self, *args, **kwargs):
		self.slug = slugify(self.course_name)
		super().save(*args, **kwargs)

	class Meta:
		db_table = 'col_course'

	def __str__(self):
		return self.course_name


THESIS_DECISION = (
	('Approved', 'Approve'),
	('Rejected', 'Reject')
	)


#my_validator = RegexValidator(r"'^[A-Z]\w+,\s*[A-Z]\.(?:\s+and (?:[A-Z]\w+,\s*[A-Z]\.|et\.\s+al\.))?'gm", "Invalid Format")

class thesisDB(Model):
	thesis_id = models.AutoField(primary_key=True, blank=True, null=False)
	title = models.CharField(max_length=200, blank=True, null=True, unique=True)
	adviser = models.CharField(max_length=200, blank=True, null=True)
	published_date = models.DateField(blank=True, null=True)
	pdf = models.FileField(upload_to='pdf/', blank=True, null=True ,validators=[FileExtensionValidator(['pdf'])],)
	course = models.ForeignKey(ColCourse, default=None, on_delete=models.CASCADE, verbose_name='Course')
	tags = TaggableManager()
	date_created = models.DateField(auto_now_add=True, blank=True, null=True )
	uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
	published_status = models.CharField(max_length=10, choices= THESIS_DECISION, default='Pending')
	abstract = models.TextField(blank=True, null=True)
	hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
	reason = models.TextField(blank=True, null=True)
	slug = models.SlugField(max_length = 250, null = True, blank = True)
	apa = models.CharField(max_length=300, null=True, blank=True)
	mla = models.CharField(max_length=300, null=True, blank=True)
	chicago = models.CharField(max_length=300, null=True, blank=True)
	submission_agreement = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		self.title = self.title.title()
		#self.author = self.author.title()
		self.slug = slugify(self.title + str(self.published_date))
		super().save(*args, **kwargs)
		
	class Meta:
		db_table = 'thesis_storage'
		

REQUEST_DECISION = (
	('Approved', 'Approve'),
	('Declined', 'Decline')
	)

class RequestPDF(Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	thesis = models.ForeignKey(thesisDB, on_delete=models.CASCADE)
	request_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	date_evaluated = models.DateTimeField(blank=True, null=True)
	request_status = models.CharField(max_length=10, choices=REQUEST_DECISION, default='Pending')
	reason = models.TextField(blank=True, null=True)
	slug = models.SlugField(max_length = 250, null = True, blank = True) 


class Registrations(AbstractUser):
	email = models.EmailField(unique=True)
	is_student = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)

	def __str__(self):
		return self.first_name +" "+ self.last_name


class Authors(Model):
	thesis = models.ForeignKey(thesisDB, on_delete=models.CASCADE, related_name='thesis')
	first_name = models.CharField(max_length=200, blank=True, null=True)
	last_name = models.CharField(max_length=200, blank=True, null=True)

	def save(self, *args, **kwargs):
		self.first_name = self.first_name.title()
		self.last_name = self.last_name.title()
		super().save(*args, **kwargs)

