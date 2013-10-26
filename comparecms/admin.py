from django.contrib import admin
from comparecms.models import (APC, DRG, ReferralRegion,
                               Provider, InpatientPaymentInfo,
                               OutpatientPaymentInfo)

admin.site.register(APC) 
admin.site.register(DRG)
admin.site.register(ReferralRegion)
admin.site.register(Provider)
admin.site.register(InpatientPaymentInfo)
admin.site.register(OutpatientPaymentInfo)
