from django.conf.urls import url

from . import views

app_name = 'papers'
urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^paper/(?P<paper_id>[0-9]+)/$', views.paper, name='paper'),
    url(r'^get_paper_file/(?P<paper_id>[0-9]+)/$', views.get_paper_file, name='get_paper_file'),
    url(r'^get_bib_file/(?P<paper_id>[0-9]+)/$', views.get_bib_file, name='get_bib_file'),
    url(r'^category/(?P<category_id>[0-9]+)/$', views.category, name='category'),
    url(r'^categories/$', views.categories, name='categories'),
    url(r'^tag/(?P<tag_id>[0-9]+)/$', views.tag, name='tag'),
    url(r'^tags/$', views.tags, name='tags'),
]
