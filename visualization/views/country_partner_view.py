from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView

from content.models import CountryPartner
from visualization.helpers.general import page_expire_period


class CountryPartnerView(APIView):
    @method_decorator(cache_page(page_expire_period()))
    def get(self, request):
        filter_args = {}
        country = self.request.GET.get("country", None)
        if country:
            filter_args["country__country_code_alpha_2"] = country
        try:
            data_provider = CountryPartner.objects.filter(**filter_args)
        except Exception:
            data_provider = [{"error": "Country partner does not exist for this country"}]
        result = []
        if data_provider:
            for i in data_provider:
                data = {
                    "name": i.name,
                    "description": i.description,
                    "email": i.email,
                    "website": i.website,
                    "logo": str(i.logo),
                    "order": i.order,
                    "country": str(i.country),
                }
                result.append(data)
        else:
            result = {"error": "Country Partner not found for this country"}
        return JsonResponse(result, safe=False)
