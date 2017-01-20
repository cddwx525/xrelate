from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from django.http import HttpResponse
from .models import Paper, Paper_relation, Category, Tag
from django.conf import settings
from django.utils.encoding import smart_str
import os

def home(request):
    latest_paper_list = Paper.objects.order_by('-date')[:10]
    context = {'latest_paper_list': latest_paper_list,}
    return render(request, 'papers/index.html', context)

def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    papers = Paper.objects.filter(category=category)
    return render(
            request,
            'papers/category.html',
            {
                'category':     category,
                'papers':       papers,
            }
    )

def categories(request):
    categories = Category.objects.all()

    #def recursive(category_list):
    #    for category in category_list:
    #        print "<ul>"
    #        print "<li><a href=\"papers/category/%s\">%s</a></li>" %(category.id, category.name)
    #        if category.category_set.exists():
    #            recursive(category.category_set.all())
    #    print "</ul>"

    #recursive(Category.objects.filter(parent__isnull=True))

    return render(
            request,
            'papers/categories.html',
            {
                'categories':   categories,
                #'category_level':   category_level,
            }
    )

def tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    papers = Paper.objects.filter(tag=tag)
    return render(
            request,
            'papers/tag.html',
            {
                'tag':          tag,
                'papers':       papers,
            }
    )

def tags(request):
    tags = Tag.objects.all()
    return render(
            request,
            'papers/tags.html',
            {
                'tags':   tags,
            }
    )

def paper(request, paper_id):
    paper = get_object_or_404(Paper, pk=paper_id)

    references_relations = Paper_relation.objects.filter(citer=paper).order_by('cite_number')
    citers = Paper.objects.filter(references=paper).order_by('-year')
    #cociters = 
    #coreferences = 
    return render(
            request,
            'papers/paper.html',
            {
                'paper':                paper,
                'references_relations': references_relations,
                'citers':               citers,
                #'cociters':            cociters,
                #'coreferences':        coreferences,
            }
    )

def view_pdf(request, paper_file_name):
    paper_file_path = os.path.join(settings.MEDIA_ROOT, paper_file_name)
    paper_file_basename = os.path.basename(paper_file_name)
    with open(paper_file_path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename=' + smart_str(paper_file_basename)
        response['Content-Disposition'] = 'inline; filename=' + smart_str(paper_file_basename)

    return response

def get_paper_file(request, paper_id):
    paper = get_object_or_404(Paper, pk=paper_id)

    paper_file_basename = os.path.basename(paper.paper_file.name)
    with open(paper.paper_file.path, 'rb') as paper_file:
        response = HttpResponse(paper_file.read(), content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename=' + smart_str(paper_file_basename)
        response['Content-Disposition'] = 'inline; filename=' + smart_str(paper_file_basename)

    return response

def get_bib_file(request, paper_id):
    paper = get_object_or_404(Paper, pk=paper_id)

    bib_file_basename = os.path.basename(paper.bib_file.name)
    with open(paper.bib_file.path, 'rb') as bib_file:
        #response = HttpResponse(bib_file.read(), content_type='text/x-bibtex')
        response = HttpResponse(bib_file.read(), content_type='text/plain')
        #response['Content-Disposition'] = 'attachment; filename=' + smart_str(bib_file_basename)
        response['Content-Disposition'] = 'inline; filename=' + smart_str(bib_file_basename)

    return response
