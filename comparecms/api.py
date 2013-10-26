import re
from django.conf.urls import url
from tastypie import fields
from tastypie.resources import ModelResource
from comparecms.models import (APC, DRG, ReferralRegion,
    ServiceArea, Provider, InpatientPaymentInfo,
    OutpatientPaymentInfo, ZipRegion)


class GetOnly:
    allowed_methods = ['get']


class APCResource(ModelResource):
    class Meta(GetOnly):
        queryset = APC.objects.all()


class DRGResource(ModelResource):
    class Meta(GetOnly):
        queryset = DRG.objects.all()


class ReferralRegionResource(ModelResource):
    class Meta(GetOnly):
        queryset = ReferralRegion.objects.all()
        resource_name = 'hrr'


class ServiceAreaResource(ModelResource):
    class Meta(GetOnly):
        queryset = ServiceArea.objects.all()
        resource_name = 'hsa'


class ProviderResource(ModelResource):
    class Meta(GetOnly):
        queryset = Provider.objects.all()


class InpatientPaymentInfoResource(ModelResource):
    drg = fields.ForeignKey(DRGResource, 'procedure', 
        full=True, null=True)

    provider = fields.ForeignKey(ProviderResource, 'provider',
        full=True, null=True)

    class Meta(GetOnly):
        queryset = InpatientPaymentInfo.objects.all()
        resource_name = 'paymentinfo/inpatient'


class OutpatientPaymentInfoResource(ModelResource):
    apc = fields.ForeignKey(APCResource, 'procedure', 
        full=True, null=True)

    provider = fields.ForeignKey(ProviderResource, 'provider',
        full=True, null=True)

    class Meta(GetOnly):
        queryset = OutpatientPaymentInfo.objects.all()
        resource_name = 'paymentinfo/outpatient'


class ZipRegionResource(ModelResource):
    hsa = fields.ForeignKey(ServiceAreaResource, 'hsa', 
        full=True, null=True)

    hrr = fields.ForeignKey(ReferralRegionResource, 'hrr', 
        full=True, null=True)

    class Meta(GetOnly):
        queryset = ZipRegion.objects.all()
        # list_allowed_methods = []
        resource_name = 'zip'

    def dehydrate(self, bundle):
        # Change 'resource_uri' to use zip code b/c
        # of the prepend_urls modification below to key
        # off of zip
        old_uri = bundle.data['resource_uri']
        new_uri = re.sub(r'\d{5}', bundle.data['zip'], old_uri)
        bundle.data['resource_uri'] = new_uri
        return bundle

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/(?P<zip>\d{5})/$' % self._meta.resource_name, 
                self.wrap_view('dispatch_detail'), name='api_dispatch_detail'),
        ]
