from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from authentication.models import MobUser
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class User(models.Model):
	related_field_name = 'user'
	mob_user = models.OneToOneField(
		settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=100, null=True, blank=True)
	avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
	balance = models.IntegerField(max_length=11, default=0)
	recent_obtain_name = models.CharField(max_length=100, null=True, blank=True)
	recent_obtain_mob = models.CharField(max_length=20, null=True, blank=True)
	recent_storage = models.ForeignKey('Storage', on_delete=models.SET_NULL, null=True)
	create_time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return '%s(%s)' % (self.name, self.id)

class Reseller(models.Model):
	related_field_name = 'reseller'
	mob_user = models.OneToOneField(
		settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=100, null=True, blank=True)
	avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
	tail = models.CharField(max_length=255, blank=True)
	state = models.IntegerField(max_length=11, default=0)
	create_time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.name if self.name else 'None'
	
class Dispatcher(models.Model):
	related_field_name = 'dispatcher'
	mob_user = models.OneToOneField(
		settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=100, null=True, blank=True)
	avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
	tail = models.CharField(max_length=255, blank=True)
	create_time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.name

class Storage(models.Model):
	address = models.TextField()
	mob = models.CharField(max_length=100, null=True, blank=True)
	opening_time = models.IntegerField(max_length=11, null=True, blank=True)
	closing_time = models.IntegerField(max_length=11, null=True, blank=True)
	create_time = models.DateTimeField(auto_now=True)
	is_custom = models.BooleanField(default=False)
	reseller = models.ForeignKey('Reseller', null=True, blank=True)
	def __unicode__(self):
		return self.address

class Category(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	receive_mode = models.IntegerField(max_length=11, default=2)
	def __unicode__(self):
		return self.name

class BulkProduct(models.Model):
	bulk = models.ForeignKey('Bulk')
	product = models.ForeignKey('Product')
	seq = models.IntegerField(max_length=11, default=0)

class Product(models.Model):
	title = models.CharField(max_length=200)
	desc = models.TextField()
	category = models.ForeignKey('Category', null=True, blank=True)
	unit_price = models.IntegerField(max_length=11)
	market_price = models.IntegerField(max_length=11)
	tag = models.CharField(max_length=20, null=True, blank=True)
	tag_color = models.CharField(max_length=20, null=True, blank=True)
	spec = models.CharField(max_length=100)
	spec_desc = models.CharField(max_length=100)
	cover = models.ImageField(upload_to='images/product/%Y/%m/%d')
	create_time = models.DateTimeField(auto_now=True)
	limit = models.IntegerField(max_length=11, null=True)
	stock = models.IntegerField(max_length=11, default=0)
	purchased = models.IntegerField(max_length=11, default=0)
	def __unicode__(self):
		return self.title

class ProductDetails(models.Model):
	product = models.ForeignKey('Product')
	image = models.ImageField(upload_to='images/product_details/%Y/%m/%d')
	plain = models.TextField()
	seq = models.IntegerField(max_length=11)
	create_time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return '%s[%s]' % (self.product.title, self.seq)
	class Meta:
		verbose_name = 'Product details'
		verbose_name_plural = 'Product details'

class Bulk(models.Model):
	title = models.CharField(max_length=200)
	category = models.ForeignKey('Category')
	details = models.TextField()
	reseller = models.ForeignKey('Reseller')
	storages = models.ManyToManyField('Storage')
	products = models.ManyToManyField('Product', through='BulkProduct')
	start_time = models.DateTimeField()
	dead_time = models.DateTimeField()
	arrived_time = models.CharField(max_length=100, null=True)
	status = models.IntegerField(max_length=11)
	location = models.CharField(max_length=100)
	receive_mode = models.IntegerField(max_length=11, default=2)
	seq = models.IntegerField(max_length=11, default=0)
	card_title = models.CharField(max_length=100)
	card_desc = models.CharField(max_length=255)
	card_icon = models.ImageField(upload_to='images/card_icon/%Y/%m/%d', blank=True)
	create_time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.title

class Configuration(models.Model):
	bulk_card_title_template = models.TextField(null=True, blank=True)
	bulk_card_desc_template = models.TextField(null=True, blank=True)
	order_card_title_template = models.TextField(null=True, blank=True)
	order_card_desc_template = models.TextField(null=True, blank=True)

class Order(models.Model):
	id = models.CharField(max_length=200, primary_key=True)
	user = models.ForeignKey('User')
	bulk = models.ForeignKey('Bulk')
	receive_mode = models.IntegerField(max_length=11, default=2)
	storage = models.ForeignKey('Storage', null=True)
	receive_name = models.CharField(max_length=200, null=True, blank=True)
	receive_mob = models.CharField(max_length=20, null=True, blank=True)
	receive_address = models.TextField(null=True, blank=True)
	status = models.IntegerField(max_length=11)
	freight = models.IntegerField(max_length=11)
	total_fee = models.IntegerField(max_length=11)
	seq = models.IntegerField(max_length=11, default=0)
	create_time = models.DateTimeField(auto_now=True)
	obtain_name = models.CharField(max_length=100, null=True, blank=True)
	obtain_mob = models.CharField(max_length=20, null=True, blank=True)
	is_delete = models.BooleanField(default=False)
	comments = models.TextField(null=True, blank=True)
	def __unicode__(self):
		return '%s(User: %s, Date: %s)' % (
			self.bulk.title, self.user.name, self.create_time)

class Goods(models.Model):
	order = models.ForeignKey('Order')
	user = models.ForeignKey('User', null=True)
	product = models.ForeignKey('Product')
	quantity = models.IntegerField(max_length=11)
	def __unicode__(self):
		return self.product.title
	class Meta:
		verbose_name = 'Goods'
		verbose_name_plural = 'Goods'

class ShippingAddress(models.Model):
	user = models.ForeignKey('User')
	name = models.CharField(max_length=200)
	mob = models.CharField(max_length=20)
	address = models.TextField()
	def __unicode__(self):
		return self.address

# Views

class BulkSummary(models.Model):
	product = models.ForeignKey('Product', primary_key=True,
		on_delete=models.DO_NOTHING)
	bulk = models.ForeignKey('Bulk',
		on_delete=models.DO_NOTHING, null=True)
	total_price = models.IntegerField(max_length=11)
	quantity = models.IntegerField(max_length=11)
	spec = models.CharField(max_length=100)

	class Meta:
		managed = False
		db_table = 'view_bulk_summary'

class PurchasedProductHistory(models.Model):
	order = models.ForeignKey('Order', primary_key=True,
		on_delete=models.DO_NOTHING)
	product = models.ForeignKey('Product',
		on_delete=models.DO_NOTHING, null=True)
	bulk = models.ForeignKey('Bulk',
		on_delete=models.DO_NOTHING, null=True)
	user = models.ForeignKey('User', 
		on_delete=models.DO_NOTHING, null=True)
	name = models.CharField(max_length=100, null=True, blank=True)
	quantity = models.IntegerField(max_length=11)
	spec = models.CharField(max_length=100)
	create_time = models.DateTimeField()

	class Meta:
		managed = False
		db_table = 'view_history_purchased_products'


class BulkDetails(models.Model):
	bulk = models.ForeignKey('Bulk',primary_key=True,
		on_delete=models.DO_NOTHING)
	reseller = models.ForeignKey('Reseller',
		on_delete=models.DO_NOTHING, null = True)

	reseller_name = models.CharField(max_length=100, null=True, blank=True)
	reseller_mob = models.CharField(max_length=20, null=True, blank=True)
	bulk_title = models.CharField(max_length=200)

	start_time = models.DateTimeField(null=False)
        dead_time = models.DateTimeField()
	
	bulk_status = models.IntegerField(max_length=11)
	bulk_receive_mode = models.IntegerField(max_length=11)
	countsize = models.CharField(max_length=200)
	class Meta:
		managed = False
		db_table = 'view_bulk_reseller'

class OrderDetails(models.Model):
	order = models.ForeignKey('Order',primary_key=True,
		on_delete=models.DO_NOTHING)
	bulk = models.ForeignKey('Bulk',
                on_delete=models.DO_NOTHING, null=True)
        user = models.ForeignKey('User',
                on_delete=models.DO_NOTHING, null=True)
	receive_mode = models.IntegerField(max_length=11, default=2)
	total_fee = models.IntegerField(max_length=11)
	status = models.IntegerField(max_length=11,null=False)
	pay_status = models.IntegerField(default=0)
	third_party_fee = models.IntegerField(default=0)
	balance_fee = models.IntegerField(default=0)
	third_party_order_id = models.CharField(max_length=200)
	create_time = models.DateTimeField()
	product = models.CharField(max_length=200)
	receive_address = models.CharField(max_length=200, null = True)
	location = models.CharField(max_length=200)
	obtain_mob = models.CharField(max_length=20, null=True,blank = True)
	obtain_name = models.CharField(max_length=200, null = True)
	receive_mob = models.CharField(max_length=20, null=True,blank = True)
	receive_name = models.CharField(max_length=200, null = True)
	comments = models.CharField(max_length=200,null=True, blank=True)
	class Meta:
		managed = False
		db_table = 'view_bulk_order'


class PayRequest(models.Model):
	order = models.OneToOneField('Order', on_delete=models.CASCADE)
	third_party_order_id = models.CharField(max_length=200)
	third_party_fee = models.IntegerField(default=0)
	balance_fee = models.IntegerField(default=0)
	use_balance = models.IntegerField(default=0)
	status = models.IntegerField(default=0)

class Slide(models.Model):
	source = models.CharField(max_length=200)
	key = models.IntegerField(max_length=11, null=True, blank=True)
	image = models.ImageField(upload_to='images/slide/%Y/%m/%d')
	category = models.CharField(max_length=100, null=True, blank=True)
	seq = models.IntegerField(max_length=11)
	create_time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.source

class ExhibitedProduct(models.Model):
	exhibit = models.ForeignKey('Exhibit')
	product = models.ForeignKey('Product')
	cover_2x = models.ImageField(upload_to='images/exhibited_product/%Y/%m/%d', null=True, blank=True)
	cover_3x = models.ImageField(upload_to='images/exhibited_product/%Y/%m/%d', null=True, blank=True)
	seq = models.IntegerField(max_length=11)
	stick = models.BooleanField(default=False)
	def __unicode__(self):
		return self.product.title

class Exhibit(models.Model):
	slides = models.ManyToManyField('Slide')
	hot_bulks = models.ManyToManyField('Bulk')
	hot_products = models.ManyToManyField('Product', through='ExhibitedProduct')
	publish_time = models.DateTimeField()
	create_time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return str(self.publish_time)

class RecipeExhibit(models.Model):
	slides = models.ManyToManyField('Slide')
	publish_time = models.DateTimeField()
	create_time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return str(self.publish_time)

class Step(models.Model):
	recipe = models.ForeignKey('Recipe')
	image = models.ForeignKey('Image', on_delete=models.SET_NULL, null=True, blank=True)
	plain = models.TextField(blank=True)
	seq = models.IntegerField(max_length=11)
	create_time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return '%s[%s]' % (self.recipe.name, self.seq)
	class Meta:
		verbose_name = 'Step details'
		verbose_name_plural = 'Step details'

class Ingredient(models.Model):
	recipe = models.ForeignKey('Recipe')
	name = models.CharField(max_length=200, blank=True)
	seq = models.IntegerField(max_length=11)
	quantity = models.CharField(max_length=200, blank=True)
	def __unicode__(self):
		return self.name

class Recipe(models.Model):
	create_time = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=200, blank=True)
	user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
	desc = models.TextField(blank=True)
	cover = models.ForeignKey('Image', on_delete=models.SET_NULL, null=True, blank=True)
	status = models.IntegerField(max_length=11)
	tag = models.CharField(max_length=200, null=True, blank=True)
	tips = models.ManyToManyField('Tip')
	time = models.CharField(max_length=200, null=True, blank=True)
	def __unicode__(self):
		return self.name

class DishDetails(models.Model):
	dish = models.ForeignKey('Dish')
	image = models.ForeignKey('Image', on_delete=models.SET_NULL, null=True, blank=True)
	plain = models.TextField(blank=True)
	seq = models.IntegerField(max_length=11)
	create_time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return '%s[%s]' % (self.dish.name, self.seq)
	class Meta:
		verbose_name = 'Dish details'
		verbose_name_plural = 'Dish details'

class Tip(models.Model):
	plain = models.TextField(blank=True)
	def __unicode__(self):
		return self.plain

class Dish(models.Model):
	create_time = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=200, blank=True)
	desc = models.TextField(blank=True)
	recipe = models.ForeignKey('Recipe', on_delete=models.SET_NULL, null=True, blank=True)
	cover = models.ForeignKey('Image', on_delete=models.SET_NULL, null=True, blank=True)
	user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
	status = models.IntegerField(max_length=11)
	tag = models.CharField(max_length=200, null=True, blank=True)
	tips = models.ManyToManyField('Tip')
	def __unicode__(self):
		return self.name

class Image(models.Model):
	md5 = models.CharField(max_length=200, primary_key=True)
	create_time = models.DateTimeField(auto_now=True)
	image = models.ImageField(upload_to='images/upload/%Y/%m/%d')
	def __unicode__(self):
		return self.md5
