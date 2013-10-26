from __future__ import unicode_literals

from django.db import models


class APC(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60, blank=True)

    class Meta:
        db_table = 'apcs'

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.name)


class DRG(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60, blank=True)

    class Meta:
        db_table = 'drgs'

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.name)


# TODO: Add field and data for referral region polygons
# This is availbale from Dartmouth Atlas
# http://www.dartmouthatlas.org/tools/downloads.aspx
class ReferralRegion(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=2, blank=True)
    city = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'ref_regions'

    def __unicode__(self):
        return u'%s - %s - %s' % (self.id, self.state, self.city)


class ServiceArea(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=2, blank=True)
    city = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'service_areas'

    def __unicode__(self):
        return u'%s - %s - %s' % (self.id, self.state, self.city)


class ZipRegion(models.Model):
    id = models.IntegerField(primary_key=True)
    zip = models.CharField(max_length=5, unique=True)
    
    hsa = models.ForeignKey(ServiceArea)
    hrr = models.ForeignKey(ReferralRegion)

    class Meta:
        db_table = 'zip_regions'

    def __unicode__(self):
       return u'%s - %s. Region: %s, HSA: %s' % (self.id, self.zip, self.hrr.id, self.hsa.id)


class Provider(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60, blank=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=5)

    class Meta:
        db_table = 'providers'

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.name)

class PaymentInfo(models.Model):
    provider = models.ForeignKey(Provider)
    num_discharged = models.IntegerField(null=True, blank=True)
    avg_charge = models.FloatField(null=True, blank=True)
    avg_payment = models.FloatField(null=True, blank=True)

    class Meta:
        abstract = True

class InpatientPaymentInfo(PaymentInfo):
    id = models.IntegerField(primary_key=True)
    procedure = models.ForeignKey(DRG)
    
    class Meta:
        db_table = 'inpatient_payment_info'

    def __unicode__(self):
        return u'%s. Provider: %s - %s' % (self.id, self.provider.id, self.provider.name)


class OutpatientPaymentInfo(PaymentInfo):
    id = models.IntegerField(primary_key=True)
    procedure = models.ForeignKey(APC)
    
    class Meta:
        db_table = 'outpatient_payment_info'

    def __unicode__(self):
        return u'%s' % (self.id)


