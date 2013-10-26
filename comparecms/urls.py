from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView, RedirectView
from tastypie.api import Api 
from comparecms import views
from comparecms.api import (APCResource, DRGResource, ReferralRegionResource,
	ProviderResource, InpatientPaymentInfoResource, ZipRegionResource,
	OutpatientPaymentInfoResource, ServiceAreaResource)

cms_api = Api(api_name='cms')
cms_api.register(APCResource())
cms_api.register(DRGResource())
cms_api.register(ReferralRegionResource())
cms_api.register(ServiceAreaResource())
cms_api.register(ZipRegionResource())
cms_api.register(ProviderResource())
cms_api.register(InpatientPaymentInfoResource())
cms_api.register(OutpatientPaymentInfoResource())

urlpatterns = patterns('',
	url(r'^robots\.txt$', RedirectView.as_view(url='/static/robots.txt')),
	url(r'^humans\.txt$', RedirectView.as_view(url='/static/humans.txt')),
	url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),

    url(r'^$', 'comparecms.views.home', name='home'),
    url(r'^results/.*$', 'comparecms.views.home', name='resultshome'),
    url(r'^about$', TemplateView.as_view(template_name='about.html')),
    
    url(r'^data$', 'comparecms.views.get_price_data', name='get_price_data'),

    url(r'^api/', include(cms_api.urls)),
)
