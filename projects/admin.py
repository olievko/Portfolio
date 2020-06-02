from __future__ import unicode_literals
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Images, Project, Comment, PersonalInfo, Skill, Testimonial, Price


@admin.register(PersonalInfo)
class PersonalInfoAdmin(TranslationAdmin):
    list_display = ('first_name', 'last_name', 'career')


@admin.register(Skill)
class SkillAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ('name', )}


class ImagesInline(admin.TabularInline):
    list_display = ('caption', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('caption',)}
    model = Images
    exta = 0


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display = ('title', 'publish', 'status')
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('status', 'added', 'publish')
    search_fields = ('title', 'technology', 'meta_keywords', 'meta_description')
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    inlines = [ImagesInline, ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'body')
    list_filter = ('created', 'updated')
    ordering = ('active', 'updated')


@admin.register(Testimonial)
class TestimonialAdmin(TranslationAdmin):
    pass


@admin.register(Price)
class PriceAdmin(TranslationAdmin):
    list_display = ('type', 'price', 'active')
