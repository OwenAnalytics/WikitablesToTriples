from django.db import models

class WikiList(models.Model):
	title = models.CharField(max_length=128)
	base_title = models.CharField(max_length=128)
	html = models.TextField()
	summary = models.TextField()
	url = models.URLField()
	has_tables = models.BooleanField(default=False)

	def __str__(self):
		return self.title

	def url_ref(self):
		return u'<a href="%s">%s</a>' % (str(self.url), str(self.url))
	url_ref.allow_tags = True
	url_ref.short_description = 'Wikipedia URL'

	class Meta:
		verbose_name='Wikipedia List'
		verbose_name_plural='Wikipedia Lists'

class WikiTable(models.Model):
	wiki_list = models.ForeignKey(WikiList)
	title = models.CharField(max_length=128)
	html = models.TextField()
	checked = models.BooleanField(default=False)
	algo_col = models.CharField(max_length=128, blank=True, null=True)
	hum_col = models.CharField(max_length=128, blank=True, null=True)

	def __str__(self):
		return self.title

class RDF(models.Model):
	wiki_list = models.ForeignKey(WikiList)
	statement = models.TextField()

	class Meta:
		verbose_name='RDF statement'
		verbose_name_plural='RDF statements'


class Link(models.Model):
	wiki_list = models.ForeignKey(WikiList)
	link_name = models.CharField(max_length=128)

	class Meta:
		verbose_name='Referenced Link'
		verbose_name_plural='Referenced Links'


