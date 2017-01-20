from __future__ import unicode_literals

from django.db import models
import os

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=256)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Paper(models.Model):
    paper_file = models.FileField(upload_to='paper/%Y/%m/%d/', blank=True, null=True)
    bib_file = models.FileField(upload_to='bib/%Y/%m/%d/', blank=True, null=True)
    downloaded = models.BooleanField()
    favorite = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tag = models.ManyToManyField(Tag, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    bibtype = models.CharField(max_length=128, blank=True, null=True)
    bibcite = models.CharField(max_length=128, blank=True, null=True)
    author = models.CharField(max_length=256, blank=True, null=True)
    organization = models.CharField(max_length=256, blank=True, null=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    journal = models.CharField(max_length=256, blank=True, null=True)
    volume = models.CharField(max_length=128, blank=True, null=True)
    number = models.CharField(max_length=128, blank=True, null=True)
    pages = models.CharField(max_length=128, blank=True, null=True)
    year = models.DateField(blank=True, null=True)
    doi = models.CharField(max_length=256, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=256, blank=True, null=True)

    # Define this paper model's references property.
    #
    # Take references as the paper's property is better than citers, because
    # a paper's references is a static content, which is suitable for property.
    #
    # The cite order is from reference to citer, so map this model and reference
    # model through 'target' and 'source' fields. Think slowly.
    #
    # When make relate objects query on properties such as references or citers,
    # the added 's' is suitable for the meanning. For insitance:
    #       paper5.references.all()
    # or
    #       paper5.citers.all()
    #
    # But when make query set with filter on this model use another model's
    # propery for objects, the added 's' looks stupid. For example:
    #       Paper.objects.filter(citers=paper3)
    # or
    #       Paper.objects.filter(references=paper3)
    # 
    # Through related_query_name can define 'citers' to 'citer', references
    # still exists. Just use it.
    references = models.ManyToManyField(
            'self',
            related_name='citers',
            related_query_name='citer',
            symmetrical=False,
            through='Paper_relation',
            through_fields=('citer', 'reference'),
    )

    def paper_file_basename(self):
        return os.path.basename(self.paper_file.name)

    def __unicode__(self):
        return self.title

class Paper_relation(models.Model):
    citer = models.ForeignKey(Paper, related_name='as_citer', on_delete=models.CASCADE)
    reference = models.ForeignKey(Paper, related_name='as_reference', on_delete=models.CASCADE)
    cite_number = models.PositiveSmallIntegerField()

    def __unicode__(self):
        #return '%s' % (self.cite_number)
        return '%s' % (self.id)
