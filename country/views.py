import operator

import django_filters
from django.contrib import messages
from django.core import management
from django.db.models import Sum
from django.http.response import HttpResponseRedirect, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from country.models import ImportBatch
from country.tasks import store_in_temp_table
from vizualization.views import add_filter_args

from .models import Buyer, Country, Language, OverallSummary, Supplier, Tender
from .serializers import (
    BuyerSerializer,
    CountrySerializer,
    LanguageSerializer,
    OverallStatSummarySerializer,
    SupplierSerializer,
    TenderSerializer,
)


class TenderPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "limit"
    max_page_size = 1000


class CountryView(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "slug"
    extensions_auto_optimize = True

    def get_queryset(self):
        return Country.objects.all()

    @action(detail=False, methods=["get"])
    def choices(self, request):
        countries = Country.objects.all().order_by("name")
        serializer = self.get_serializer(countries, many=True)
        country_id_and_name = [{"id": country["id"], "name": _(country["name"])} for country in serializer.data]

        return Response(country_id_and_name)


class LanguageView(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    extensions_auto_optimize = True


class TenderView(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering = ["-id"]
    serializer_class = TenderSerializer
    ordering_fields = (
        "contract_title",
        "procurement_procedure",
        "supplier",
        "status",
        "contract_value_usd",
        "buyer",
        "contract_value_local",
        "country",
        "contract_date",
    )
    filterset_fields = {
        "country__country_code_alpha_2": ["exact"],
    }
    extensions_auto_optimize = True

    def get_queryset(self):
        country = self.request.GET.get("country", None)
        buyer = self.request.GET.get("buyer", None)
        supplier = self.request.GET.get("supplier", None)
        product_id = self.request.GET.get("product", None)
        status = self.request.GET.get("status", None)
        procurement_procedure = self.request.GET.get("procurement_procedure", None)
        title = self.request.GET.get("title", None)
        date_from = self.request.GET.get("date_from", None)
        date_to = self.request.GET.get("date_to", None)
        contract_value_usd = self.request.GET.get("contract_value_usd", None)
        value_comparison = self.request.GET.get("value_comparison", None)
        equity_id = self.request.GET.get("equity_id", None)
        filter_args = {}
        exclude_args = {}
        annotate_args = {}
        if equity_id:
            filter_args["equity_category__id"] = equity_id
        if country:
            filter_args["country__country_code_alpha_2"] = country
        if buyer:
            filter_args = add_filter_args("buyer", buyer, filter_args)
        if supplier:
            filter_args = add_filter_args("supplier", supplier, filter_args)
        if product_id:
            filter_args["goods_services__goods_services_category"] = product_id
        if title:
            filter_args["contract_title__icontains"] = title
        if date_from and date_to:
            filter_args["contract_date__range"] = [date_from, date_to]
        if contract_value_usd and value_comparison:
            if value_comparison == "gt":
                annotate_args["sum"] = Sum("goods_services__contract_value_usd")
                filter_args["sum__gte"] = contract_value_usd
            elif value_comparison == "lt":
                annotate_args["sum"] = Sum("goods_services__contract_value_usd")
                filter_args["sum__lte"] = contract_value_usd
        if status == "others":
            exclude_args["status__in"] = ["active", "canceled", "completed"]
        elif status in ["active", "canceled", "completed"]:
            filter_args["status"] = status
        if procurement_procedure == "others":
            exclude_args["procurement_procedure__in"] = ["open", "limited", "direct", "selective"]
        elif procurement_procedure in ["open", "limited", "direct", "selective"]:
            filter_args["procurement_procedure"] = procurement_procedure
        return (
            Tender.objects.prefetch_related("buyer", "supplier", "country")
            .annotate(**annotate_args)
            .filter(**filter_args)
            .exclude(**exclude_args)
        )


class BuyerFilter(FilterSet):
    product = django_filters.NumberFilter(field_name='goods_services__goods_services_category')
    country = django_filters.CharFilter(field_name='tenders__country__country_code_alpha_2')
    buyer_name = django_filters.CharFilter(field_name='buyer_name')

    class Meta:
        model = Buyer
        fields = ['product', 'country', 'buyer_name']


class BuyerView(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend, ]
    filter_class = BuyerFilter
    serializer_class = BuyerSerializer
    filter_fields = ('buyer_name',)
    ordering_fields = [
        "tender_count",
        "supplier_count",
        "product_category_count",
        "buyer_name",
        "country_name",
        "amount_usd",
        "amount_local",
    ]
    ordering = ["-id"]
    extensions_auto_optimize = True

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        instance = Buyer.objects.filter(id=pk)[0]
        return Response(self.get_serializer(instance).data)

    def list(self, request):
        order = 'DESC'
        country = 'MD'

        raw_query = f" SELECT \
                        country_buyer.id \
                        , max( country_country.name) as country_name \
                        , max(country_buyer.buyer_name) as buyer_name  \
                        , sum(country_goodsservices.contract_value_usd) as amount_usd \
                        , sum(country_goodsservices.contract_value_local) as amount_local \
                        , count(distinct(country_goodsservices.contract_id)) as tender_count \
                        , count(distinct(country_goodsservices.goods_services_category_id)) as product_category_count \
                        , count(country_tender_red_flag.id) as red_flag_count \
                        , count(distinct(country_tender_red_flag.tender_id)) as red_flag_tender_count \
                        , case when (count(country_tender_red_flag.id) > 0 ) then (count(distinct(country_tender_red_flag.tender_id)) /  \
                                                                                   count(country_tender_red_flag.id)) else 0 end as red_flag_tender_percentage \
                        FROM country_buyer \
                        JOIN country_tender on country_tender.buyer_id = country_buyer.id \
                        JOIN country_goodsservices on country_tender.id = country_goodsservices.contract_id \
                        LEFT JOIN country_country on country_country.id = country_tender.country_id \
                        LEFT JOIN country_tender_red_flag on country_tender_red_flag.tender_id = country_tender.id \
                        WHERE 1=1 \
                        AND country_country.country_code_alpha_2 = '{country}' \
                        GROUP BY country_buyer.id \
                        ORDER BY amount_usd  \
                        {order} "
        queryset = Buyer.objects.raw(raw_query)
        paginator = LimitOffsetPagination()
        result = paginator.paginate_queryset(queryset, request)
        serializer = BuyerSerializer(result, many=True, context={'request': request})
        # data = JSONRenderer().render(serializer.data)
        return JsonResponse(serializer.data, safe=False)

    def get_queryset(self):
        order = 'ASC'
        raw_query = f" SELECT \
                                    country_buyer.id \
                                    , max(country_buyer.buyer_name) as buyer_name \
                                    , sum(country_goodsservices.contract_value_usd) as amount_usd \
                                    , sum(country_goodsservices.contract_value_local) as amount_local \
                                    , sum(distinct(country_goodsservices.contract_id)) as tender_count \
                                    FROM country_buyer \
                                    JOIN \
                                    country_tender \
                                    ON \
                                    country_tender.buyer_id = country_buyer.id \
                                    JOIN \
                                    country_goodsservices \
                                    ON \
                                    country_tender.id = country_goodsservices.contract_id \
                                    WHERE \
                                    country_tender.country_id = 6 \
                                    GROUP \
                                    BY \
                                    country_buyer.id \
                                    ORDER \
                                    BY amount_usd \
                                    {order} \
                                    limit 20 "
        queryset = Buyer.objects.raw(raw_query)
        serializer = BuyerSerializer(queryset, many=True)
        # data = JSONRenderer().render(serializer.data)
        return Response(serializer.data)


class SupplierView(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    filter_backends = [OrderingFilter]
    serializer_class = SupplierSerializer
    ordering_fields = [
        "tender_count",
        "buyer_count",
        "product_category_count",
        "supplier_name",
        "country_name",
        "amount_usd",
        "amount_local",
    ]
    ordering = ["-id"]
    extensions_auto_optimize = True

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        instance = Supplier.objects.filter(id=pk)[0]
        return Response(self.get_serializer(instance).data)

    def get_queryset(self):
        #    country, buyer name, value range, red flag range
        country = self.request.GET.get("country", None)
        supplier_name = self.request.GET.get("supplier_name", None)
        product_id = self.request.GET.get("product", None)
        filter_args = {}
        annotate_args = {}
        if country:
            filter_args["tenders__country__country_code_alpha_2"] = country
        if supplier_name:
            filter_args["supplier_name__icontains"] = supplier_name
        if product_id:
            filter_args["tenders__goods_services__goods_services_category"] = product_id
        contract_value_usd = self.request.GET.get("contract_value_usd", None)
        value_comparison = self.request.GET.get("value_comparison", None)
        if contract_value_usd and value_comparison:
            if value_comparison == "gt":
                annotate_args["sum"] = Sum("tenders__goods_services__contract_value_usd")
                filter_args["sum__gte"] = contract_value_usd
            elif value_comparison == "lt":
                annotate_args["sum"] = Sum("tenders__goods_services__contract_value_usd")
                filter_args["sum__lte"] = contract_value_usd
        return Supplier.objects.annotate(**annotate_args).filter(**filter_args).distinct()


class OverallStatSummaryView(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    queryset = OverallSummary.objects.all()
    serializer_class = OverallStatSummarySerializer
    extensions_auto_optimize = True


class DataImportView(APIView):
    def get(self, request):
        country = self.request.GET.get("country", None)
        # filename =  self.request.GET.get('filename',None)
        data_import_id = self.request.GET.get("data_import_id", None)
        validated = self.request.GET.get("validated", None)

        if validated:
            if data_import_id:
                try:
                    import_batch_instance = ImportBatch.objects.get(data_import_id=data_import_id)
                    batch_id = import_batch_instance.id
                    # management.call_command('import_tender_excel', country, file_path)
                    management.call_command("import_tender_from_id", country, batch_id)
                    messages.info(request, "Your import has started!")
                    return HttpResponseRedirect("/admin/content/dataimport")

                except:
                    messages.error(request, "Your import has failed!")
                    return HttpResponseRedirect("/admin/content/dataimport")
            else:
                # messages.error(request, 'Your import failed because it only supports .xlsx and .xls file!')
                messages.error(request, "Your import failed!")
                return HttpResponseRedirect("/admin/content/dataimport")
        else:
            messages.error(
                request,
                "Your data import file is not validated, please upload file with all necessary headers and try "
                "importing again.",
            )

            return HttpResponseRedirect("/admin/content/dataimport")


class DataEditView(APIView):
    def get(self, request):
        data_import_id = self.request.GET.get("data_import_id", None)

        return HttpResponseRedirect("/admin/country/tempdataimporttable/?import_batch__id__exact=" + data_import_id)


class DataValidateView(APIView):
    def get(self, request):
        instance_id = self.request.GET.get("data_import_id", None)
        if instance_id is not None:
            try:
                store_in_temp_table.apply_async(args=(instance_id,), queue="covid19")
                messages.info(request, "Validation is in progress!! Please wait for a while")
                return HttpResponseRedirect("/admin/content/dataimport")

            except:
                messages.error(request, "Your import has failed!")
                return HttpResponseRedirect("/admin/content/dataimport")
        else:
            # messages.error(request, 'Your import failed because it only supports .xlsx and .xls file!')
            messages.error(request, "Your import failed !!")
            return HttpResponseRedirect("/admin/content/dataimport")
