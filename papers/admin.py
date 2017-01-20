from django.contrib import admin

# Register your models here.

from .models import Paper, Category, Tag, Paper_relation

from pybtex.database import parse_file
import time

class ReferencesInline(admin.TabularInline):
    model = Paper_relation
    fk_name = 'citer'
    extra = 1

class CitersInline(admin.TabularInline):
    model = Paper_relation
    fk_name = 'reference'
    extra = 1

class PaperAdmin(admin.ModelAdmin):
    list_display = ('id', 'doi', 'title', 'author', 'category',)
    list_filter = ('tag', 'category', 'year',)
    filter_horizontal = ('tag',)
    inlines = [
            ReferencesInline,
            CitersInline,
    ]

    def save_model(self, request, obj, form, change):
        if request.FILES.has_key('bib_file'):
            obj.save()

            bib_file = obj.bib_file.path
            #bib_file = request.FILES['bib_file'].

            bib_data = parse_file(bib_file)
            bib = self.extract_bib(bib_data)

            for (key, value) in bib.items():
                setattr(obj, key, value)

            obj.save()
        else:
            obj.save()

    def extract_bib(self, bib_data):
        #bibdict = bib_data.entries.items()
        #bibdict_bibfirst = bibdict[0]
        #bibdict_bibfirst_bibcite = bibdict_bibfirst[0]
        #bibdict_bibfirst_entry = bibdict_bibfirst[1]
        #bibdict_bibfirst_entry_type = bibdict_bibfirst_entry.type
        #bibdict_bibfirst_entry_fieldsdict = bibdict_bibfirst_entry.fields
        #bibdict_bibfirst_entry_personsdict = bibdict_bibfirst_entry.persons.items()
        #bibdict_bibfirst_entry_personsdict_personsfirst = bibdict_bibfirst_entry_personsdict[0]
        #bibdict_bibfirst_entry_personsdict_personsfirst_personslist = bibdict_bibfirst_entry_personsdict_personsfirst[1]

        bibkey = bib_data.entries.items()[0][0]
        bibtype = bib_data.entries.items()[0][1].type
        author = self.flatauthor(bib_data.entries.items()[0][1].persons.items()[0][1])
        organization = bib_data.entries.items()[0][1].fields.get('organization', '')
        title = bib_data.entries.items()[0][1].fields.get('title', '')
        journal = bib_data.entries.items()[0][1].fields.get('journal', '')
        volume = bib_data.entries.items()[0][1].fields.get('volume', '')
        numbers = bib_data.entries.items()[0][1].fields.get('numbers', '')
        pages = bib_data.entries.items()[0][1].fields.get('pages', '')
        #year = bib_data.entries.items()[0][1].fields.get('year', '')
        year = self.year_to_date(bib_data.entries.items()[0][1].fields)
        doi = bib_data.entries.items()[0][1].fields.get('doi', '')
        abstract = bib_data.entries.items()[0][1].fields.get('abstract', '')
        keywords = bib_data.entries.items()[0][1].fields.get('keywords', '')

        bib = {
                'bibcite': bibkey,
                'bibtype': bibtype,
                'author': author,
                'organization': organization,
                'title': title,
                'journal': journal,
                'volume': volume,
                'numbers': numbers,
                'pages': pages,
                'year': year,
                'doi': doi,
                'abstract': abstract,
                'keywords': keywords,
        }

        return bib

    def flatauthor(self, bib_personlist):
        space = ' '
        comma = ', '
        author_list = []

        for person in bib_personlist:
            # Join contens in each part of whole name.
            first_name = space.join(person.first_names)
            middle_name = space.join(person.middle_names)
            prelast_name = space.join(person.prelast_names)
            last_name = space.join(person.last_names)
            singleauthor = [first_name, middle_name, prelast_name, last_name]

            # Join each part of whole name, and remove redundant space due to some part of whole name is empty.
            singleauthor = space.join(singleauthor).replace('  ', ' ')
            author_list.append(singleauthor)

        flatauthor = comma.join(author_list)

        return flatauthor

    def year_to_date(self, fieldsdict):
        if 'year' in fieldsdict:
            if self.is_valid_date(fieldsdict['year']):
                date = fieldsdict['year'] + '-01-01'
            else:
                date = ''
        else:
            date = ''

        return date


    def is_valid_date(self, str):
        try:
            time.strptime(str, "%Y")
            return True
        except:
            return False


class Paper_relationAdmin(admin.ModelAdmin):
    list_display = ('id', 'citer', 'reference', 'cite_number',)

admin.site.register(Paper, PaperAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Paper_relation, Paper_relationAdmin)
