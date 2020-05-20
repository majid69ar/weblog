from django.db import models#بارگذاری مدل
from django.urls import reverse
from account.models import User#بارگذاری یوزر
from django.utils.html import format_html#بارگذاری HTML
from django.utils import timezone#بارگذاری زمان
from extensions.utils import jalali_converter#بارگذاری فونت و تقویم جلالی

# my managers
class ArticleManager(models.Manager):#مدیریت مقاله
	def published(self):
		return self.filter(status='p')


class CategoryManager(models.Manager):#مدیریت دسته بندی
	def active(self):
		return self.filter(status=True)


# Create your models here.
class Category(models.Model):#دسته بندی ها
	parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name="زیردسته")
	title = models.CharField(max_length=200, verbose_name="عنوان دسته‌بندی")
	slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس دسته‌بندی")
	status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")
	position = models.IntegerField(verbose_name="موقعیت")

	class Meta:
		verbose_name = "دسته‌بندی"
		verbose_name_plural = "دسته‌بندی ها"
		ordering = ['parent__id', 'position']

	def __str__(self):
		return self.title

	objects = CategoryManager()


class Article(models.Model):#مقاله ها
	STATUS_CHOICES = (
		('d', 'پیش‌نویس'),
		('p', "منتشر شده"),
	)
	author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles', verbose_name="نویسنده")
	title = models.CharField(max_length=200, verbose_name="عنوان مقاله")
	slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس مقاله")
	category = models.ManyToManyField(Category, verbose_name="دسته‌بندی", related_name="articles")
	description = models.TextField(verbose_name="محتوا")
	thumbnail = models.ImageField(upload_to="images", verbose_name="تصویر مقاله")
	publish = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")

	class Meta:
		verbose_name = "مقاله"
		verbose_name_plural = "مقالات"
		ordering = ['-publish']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('account:home')
	

	def jpublish(self):#فونت و تقویم جلالی
		return jalali_converter(self.publish)
	jpublish.short_description = "زمان انتشار"

	def thumbnail_tag(self):#
		return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format('self.thumbnail.url'))
	thumbnail_tag.short_description = "عکس"	

	def category_to_str(self):
		return "، ".join([category.title for category in self.category.active()])
	category_to_str.short_description = "دسته‌بندی"

	objects = ArticleManager()