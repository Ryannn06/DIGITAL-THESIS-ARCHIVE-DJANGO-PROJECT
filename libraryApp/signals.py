from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Authors, thesisDB
from django.shortcuts import get_object_or_404

from django.contrib.sites.shortcuts import get_current_site

import calendar


@receiver(post_save, sender=thesisDB)
@receiver(post_save, sender=Authors)
def generate_citations(sender, instance, created, *args, **kwargs):

	#get the thesis and authors for that thesis
	thesis = get_object_or_404(thesisDB, thesis_id = instance.thesis_id)
	authors = Authors.objects.filter(thesis__thesis__thesis_id=thesis.thesis_id).distinct()
	
	#extract year from datefield column of the thesis
	year = str(thesis.published_date.year)

	month_number = int(thesis.published_date.month)
	month_name = str(calendar.month_name[month_number])

	#format authors according to diff. cititaions
	apa_formatted_author = apa_format_author(authors)
	mla_formatted_author = mla_format_author(authors)
	chicago_formatted_author = chicago_format_author(authors)

	site = get_current_site(request=None)
	domain = site.domain
	retrieved_url = str(domain + '/repository/view/' + thesis.slug)

	#print(apa_formatted_author)
	#print(mla_formatted_author)
	#print(chicago_formatted_author)

	#generate citations
	apa = str(apa_formatted_author + ' (' + year + '). ' + thesis.title + '. Retrieved from ' + retrieved_url + '.' )
	mla = str(mla_formatted_author + ' "' + thesis.title + '." ' + 'TUPC Digital Thesis Archive, ' + year + '. Web.')
	chicago = str(chicago_formatted_author + ' ' + year + '. "' + thesis.title + '." ' + 'TUPC Digital Thesis Archive. ' + month_name + ' ' + year + '. ' + retrieved_url + '.')

	#save or update citations
	thesisDB.objects.filter(thesis_id = instance.thesis_id).update(apa = apa, mla=mla, chicago=chicago)


#generators
def apa_format_author(authors):
	length = len(authors)
	if length == 1:
		first_name = authors.values()[0]['first_name']
		first_name = list(first_name)[0]
		last_name = authors.values()[0]['last_name']
		author = str(last_name + ', ' + first_name + '.')
		
	elif length == 2:
		first_name_1 = authors.values()[0]['first_name']
		first_name_1 = list(first_name_1)[0]
		last_name_1 = authors.values()[0]['last_name']

		first_name_2 = authors.values()[1]['first_name']
		first_name_2 = list(first_name_2)[0]
		last_name_2 = authors.values()[1]['last_name']

		author = str(last_name_1 + ', ' + first_name_1 + '. and ' + last_name_2 + ', ' + first_name_2 + '.')

	elif length >= 3:
		first_name = authors.values()[0]['first_name']
		first_name = list(first_name)[0]
		last_name = authors.values()[0]['last_name']

		author = str(last_name + ', ' + first_name + '.,' + ' et al.')

	else:
		author = 'Unknown.'

	return author


def mla_format_author(authors):
	length = len(authors)

	if length == 1:
		first_name = authors.values()[0]['first_name']
		last_name = authors.values()[0]['last_name']
		author = str(first_name + ' ' + last_name + '.')

	elif length == 2:
		first_name_1 = authors.values()[0]['first_name']
		last_name_1 = authors.values()[0]['last_name']

		first_name_2 = authors.values()[1]['first_name']
		last_name_2 = authors.values()[1]['last_name']
		author = str(last_name_1 + ', ' + first_name_1 + ',' + ' and ' + first_name_2 + ' ' + last_name_2 + '.')

	elif length >= 3:
		first_name = authors.values()[0]['first_name']
		last_name = authors.values()[0]['last_name']

		author = str(last_name + ', ' + first_name + ', et al.')

	else:
		author = 'Unknown.'

	return author


def chicago_format_author(authors):
	length = len(authors)

	if length == 1:
		first_name = authors.values()[0]['first_name']
		last_name = authors.values()[0]['last_name']
		author = str(last_name + ', ' + first_name + '.')

	elif length == 2:
		first_name_1 = authors.values()[0]['first_name']
		last_name_1 = authors.values()[0]['last_name']

		first_name_2 = authors.values()[1]['first_name']
		last_name_2 = authors.values()[1]['last_name']

		author = str(first_name_1 + ' ' +last_name_1 + ' and ' + first_name_2 + ' ' + last_name_2 + '.')

	elif length == 3:
		first_name_1 = authors.values()[0]['first_name']
		last_name_1 = authors.values()[0]['last_name']

		first_name_2 = authors.values()[1]['first_name']
		last_name_2 = authors.values()[1]['last_name']

		first_name_3 = authors.values()[2]['first_name']
		last_name_3 = authors.values()[2]['last_name']


		author = str(first_name_1 + ' ' +last_name_1 + ', ' + first_name_2 + ' ' + last_name_2 + ',' + ' and ' + first_name_3 + ' ' + last_name_3 + '.')
	
	elif length >= 4:
		first_name = authors.values()[0]['first_name']
		last_name = authors.values()[0]['last_name']

		author = str(first_name + ' ' + last_name + ' et al.')

	else:
		author = 'Unknown.'

	return author
