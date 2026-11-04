from django import forms
from .models import Product, Category, BlogPost, BlogCategory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'price', 'discount_price', 'stock',
            'weight', 'main_image', 'full_description', 'is_flash_deal',
            'focus_keyword', 'meta_title', 'meta_description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'category': forms.Select(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'price': forms.NumberInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'discount_price': forms.NumberInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'stock': forms.NumberInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'weight': forms.NumberInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'main_image': forms.FileInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg'}),
            'full_description': forms.Textarea(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high', 'rows': 4}),
            'focus_keyword': forms.TextInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'meta_title': forms.TextInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'meta_description': forms.Textarea(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high', 'rows': 2}),
            'is_flash_deal': forms.CheckboxInput(attrs={'class': 'w-5 h-5 accent-primary'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'parent': forms.Select(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'image': forms.FileInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg'}),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'category', 'image', 'content', 'focus_keyword', 'meta_title', 'meta_description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'slug': forms.TextInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'category': forms.Select(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'image': forms.FileInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg'}),
            'content': forms.Textarea(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high', 'rows': 8}),
            'focus_keyword': forms.TextInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'meta_title': forms.TextInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'meta_description': forms.Textarea(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high', 'rows': 2}),
        }

class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
            'slug': forms.TextInput(attrs={'class': 'w-full bg-surface p-2.5 rounded-lg border border-surface-container-high'}),
        }