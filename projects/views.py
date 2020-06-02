from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PersonalInfo, Project, Testimonial, Skill, Price
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from .forms import CommentForm, ContactForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.decorators import ajax_required

import os
import redis
from django.conf import settings

# r = redis.StrictRedis(host=settings.REDIS_HOST,
#                       port=settings.REDIS_PORT,
#                       db=settings.REDIS_DB)


r = redis.from_url(os.environ.get("REDIS_URL"))


def index(request):
    template = "project_index.html"
    personal_info = PersonalInfo.objects.all()
    skills = Skill.objects.all()
    testimonials = Testimonial.objects.all()
    prices = Price.objects.all()
    object_list = Project.published.all()
    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            contact_email = form.cleaned_data['contact_email']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = ['dozorinnet@gmail.com']
            if cc_myself:
                recipients.append(contact_email)
            try:
                send_mail(subject,
                          message,
                          contact_email,
                          recipients)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
        return redirect('message_sent')
    else:
        form = ContactForm()
    context = {
        'personal_info': personal_info,
        'testimonials': testimonials,
        'prices': prices,
        'skills': skills,
        'page': page,
        'projects': projects,
        'form': form,
    }
    return render(request, template, context)


def project_detail(request, pk, slug):
    template = 'project_detail.html'
    personal_info = PersonalInfo.objects.all()[:1]
    skills = Skill.objects.all()
    projects = Project.published.all()
    project = get_object_or_404(Project, pk=pk, slug=slug)
    meta_keywords = project.meta_keywords
    meta_description = project.meta_description
    images = project.images.all()
    testimonials = Testimonial.objects.all()
    prices = Price.objects.all()
    total_views = r.incr('project:{}:views'.format(project.pk))
    r.zincrby('project_ranking', 1, project.pk)
    project_ranking = r.zrange('project_ranking', 0, -1, desc=True)[:6]
    project_ranking_pks = [int(pk) for pk in project_ranking]
    most_viewed = list(Project.published.filter(pk__in=project_ranking_pks))
    most_viewed.sort(key=lambda x: project_ranking_pks.index(x.pk))
    comments = project.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST' and 'add' in request.POST:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.project = project
            new_comment.save()
    else:
        comment_form = CommentForm()
    if request.method == 'POST' and 'send' in request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            contact_email = form.cleaned_data['contact_email']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = ['dozorinnet@gmail.com']
            if cc_myself:
                recipients.append(contact_email)
            try:
                send_mail(subject,
                          message,
                          contact_email,
                          recipients)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
        return redirect('message_sent')
    else:
        form = ContactForm()
    context = {
        'personal_info': personal_info,
        'skills': skills,
        'projects': projects,
        'project': project,
        'meta_keywords': meta_keywords,
        'meta_description': meta_description,
        'testimonials': testimonials,
        'prices': prices,
        'images': images,
        'total_views': total_views,
        'most_viewed': most_viewed,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'form': form,
    }
    return render(request, template, context)


def message_sent(request):
    personal_info = PersonalInfo.objects.all()[:1]
    skills = Skill.objects.all()
    projects = Project.published.all()
    testimonials = Testimonial.objects.all()
    message_success = 'message_success'
    context = {
        'personal_info': personal_info,
        'testimonials': testimonials,
        'skills': skills,
        'projects': projects,
        'message_success': message_success,
    }
    return render(request, "includes/message_success.html", context)


@ajax_required
@login_required
@require_POST
def project_like(request):
    project_id = request.POST.get('id')
    action = request.POST.get('action')
    if project_id and action:
        try:
            project = Project.objects.get(id=project_id)
            if action == 'like':
                project.users_like.add(request.user)
            else:
                project.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ok'})

