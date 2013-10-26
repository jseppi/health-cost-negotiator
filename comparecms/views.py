import pprint
import json

from django.utils import simplejson
from django.core import serializers
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

from comparecms.models import *


def home(request):

    drgs = DRG.objects.all().values('id', 'name')
    apcs = APC.objects.all().values('id', 'name')

    context = {
        'drgList': list(drgs),
        'apcList': list(apcs)
    }

    return render(request, 'index.html', context)


def _get_payment_average(payment_infos):
    if len(payment_infos) == 0:
        return 0
    return float(sum([pmt.avg_payment for pmt in payment_infos])) / len(payment_infos)


def _get_charge_average(payment_infos):
    if len(payment_infos) == 0:
        return 0
    return float(sum([pmt.avg_charge for pmt in payment_infos])) / len(payment_infos)


def _get_payment_infos_for_type(apc_or_drg, apc_drg_id, filter_query={}):
    id_filter = {'procedure_id__exact': apc_drg_id}

    filter_dict = dict(id_filter.items() + filter_query.items())

    if apc_or_drg == 'drg':
        return InpatientPaymentInfo.objects.filter(**filter_dict)
    elif apc_or_drg == 'apc':
        return OutpatientPaymentInfo.objects.filter(**filter_dict)


def get_price_data(request):
    # Using GET requests because ajax post is broken in IE10
    
    zipcode = request.GET['zip']  # Zip Code
    apc_or_drg = request.GET['type']  # Type ('apc' or 'drg')
    apc_drg_id = request.GET['id']  # APC or DRG Id

    if apc_or_drg != 'drg' and apc_or_drg != 'apc':
        raise Http404

    zip_region = get_object_or_404(ZipRegion,
        zip__exact = zipcode)

    referral_region = zip_region.hrr

    # Get InpatientPayments for providers in the same region as provider.zip

    # First get all zipcodes in the referral region
    zips_in_region = ZipRegion.objects.filter(
        hrr__exact = referral_region.id)

    payment_infos_region = _get_payment_infos_for_type(apc_or_drg,
       apc_drg_id,
       {'provider__zip__in': [z.zip for z in zips_in_region]})

    pmt_avg_region = _get_payment_average(payment_infos_region)
    charge_avg_region = _get_charge_average(payment_infos_region)

    # Get averages payment for State
    payment_infos_state = _get_payment_infos_for_type(apc_or_drg,
      apc_drg_id,
      {'provider__state__exact': referral_region.state})

    pmt_avg_state = _get_payment_average(payment_infos_state)
    charge_avg_state = _get_charge_average(payment_infos_state)

    # Get averages nationally
    payment_infos_natl = _get_payment_infos_for_type(apc_or_drg, apc_drg_id)

    pmt_avg_natl = _get_payment_average(payment_infos_natl)
    charge_avg_natl = _get_charge_average(payment_infos_natl)

    # Get High and Low nationally
    charge_high_natl = max([pmt.avg_charge for pmt in payment_infos_natl])
    charge_low_natl = min([pmt.avg_charge for pmt in payment_infos_natl])

    
    # List for table display of payment info for providers in referral region
    region_pmt_info = [{
        'name': p.provider.name,
        'zip': p.provider.zip,
        'charge_avg': p.avg_charge,
        'pmt_avg': p.avg_payment
    } for p
        in payment_infos_region]


    procedure_name = payment_infos_natl[0].procedure.name

    result = {
        'type': apc_or_drg,
        'id': int(apc_drg_id),
        'name': procedure_name,
        'zip': zip_region.zip,
        'state': referral_region.state,
        'hrr_id': referral_region.id,
        'pmt_avg_region': pmt_avg_region,
        'pmt_avg_state': pmt_avg_state,
        'pmt_avg_natl': pmt_avg_natl,
        'charge_avg_region': charge_avg_region,
        'charge_avg_state': charge_avg_state,
        'charge_avg_natl': charge_avg_natl,
        'charge_high_natl': charge_high_natl,
        'charge_low_natl': charge_low_natl,
        'region_pmt_info':  region_pmt_info
    }

    return HttpResponse(json.dumps(result),
                        content_type="application/json")
