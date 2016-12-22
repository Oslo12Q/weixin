from django.contrib import admin

# Register your models here.

from django import forms
from .models import *

class ProductInline(admin.TabularInline):
	model = Product
	extra = 1

class ResellerAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'state', 'mob', 'create_time',)
	list_filter = ('state',)
	search_fields = ('name',)

	def mob(self, obj):
		if obj.mob_user is not None:
			return obj.mob_user.mob
		else:
			return ''

class BulkProductInline(admin.TabularInline):
	model = BulkProduct
	extra = 1

class BulkAdmin(admin.ModelAdmin):
	# inlines = [
	# 	ProductInline,
	# ]
	filter_horizontal = ('storages', 'products',)
	list_display = ('id', 'title',)
	inlines = [BulkProductInline]

class ProductDetailsInline(admin.TabularInline):
	model = ProductDetails
	extra = 1

class ProductAdmin(admin.ModelAdmin):
	inlines = [
		ProductDetailsInline,
	]

class GoodsInline(admin.TabularInline):
	model = Goods
	extra = 1

class OrderAdmin(admin.ModelAdmin):
	inlines = [
		GoodsInline,
	]

class ExhibitedProductInline(admin.TabularInline):
	model = ExhibitedProduct
	extra = 1

class ExhibitAdmin(admin.ModelAdmin):
	filter_horizontal = ('slides', 'hot_bulks',)
	inlines = [ExhibitedProductInline]

class RecipeExhibitAdmin(admin.ModelAdmin):
	filter_horizontal = ('slides',)

class StepInline(admin.TabularInline):
	model = Step
	extra = 1

class IngredientInline(admin.TabularInline):
	model = Ingredient
	extra = 1

class RecipeAdmin(admin.ModelAdmin):
	inlines = [
		StepInline,
		IngredientInline,
	]
	filter_horizontal = ('tips',)
	list_display = ('id', 'name',)

class DishDetailsInline(admin.TabularInline):
	model = DishDetails
	extra = 1

class DishAdmin(admin.ModelAdmin):
	filter_horizontal = ('tips',)
	inlines = [
		DishDetailsInline,
	]

admin.site.register(User)
admin.site.register(Reseller, ResellerAdmin)
admin.site.register(Dispatcher)

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDetails)
admin.site.register(Bulk, BulkAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Storage)
admin.site.register(Goods)
admin.site.register(ShippingAddress)

admin.site.register(Slide)
admin.site.register(Exhibit, ExhibitAdmin)
admin.site.register(RecipeExhibit, RecipeExhibitAdmin)

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Step)
admin.site.register(Ingredient)
admin.site.register(Dish, DishAdmin)
admin.site.register(DishDetails)
admin.site.register(Tip)
admin.site.register(Image)

admin.site.register(Configuration)
