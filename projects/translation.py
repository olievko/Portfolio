from modeltranslation.translator import register, TranslationOptions
from .models import PersonalInfo, Skill, Project, Testimonial, Price


@register(PersonalInfo)
class PersonalInfoTranslationOptions(TranslationOptions):
    fields = (
        'first_name',
        'last_name',
        'career',
        'overview',
        'locality',
        'country',
        'meta_keywords',
        'meta_description',
    )


@register(Skill)
class SkillTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'description',
        'technology',
        'meta_keywords',
        'meta_description',
    )


@register(Testimonial)
class TestimonialShotsTranslationOptions(TranslationOptions):
    fields = (
        'first_name_client',
        'last_name_client',
        'position_client',
        'body',
    )


@register(Price)
class PriceShotsTranslationOptions(TranslationOptions):
    fields = ('description', )