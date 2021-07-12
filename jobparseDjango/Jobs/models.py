from django.db import models

class Jobs(models.Model):
    title = models.TextField('Title of vacancy')
    companyName = models.TextField('Company name of vacancy', blank=True, null=True)
    city = models.TextField('City of vacancy', blank=True, null=True)
    image = models.URLField('URL of vacancy image', max_length=500, blank=True, null=True)
    siteName = models.TextField('Site name of vacancy')
    vacLink = models.URLField('URL of vacancy', max_length=500)
    salaryFrom = models.BigIntegerField('Starts salary of vacancy', blank=True, null=True)
    salaryTo = models.BigIntegerField('Ends salary of vacancy', blank=True, null=True)
    currency = models.TextField('Currency of vacancy', blank=True, null=True)
    idHh = models.TextField('Id of vacancy on hh', blank=True, null=True)
