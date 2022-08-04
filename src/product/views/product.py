from django.views import generic
from django.views.generic import ListView
from product.models import Variant
from django.shortcuts import render
from product.models import Product, ProductVariantPrice, ProductVariant
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    # I'm sorry I can't react js.  I request you to kindly consider this matter.
    # This is because I am still learning.Here I am unable to run those files- 
    # templates/assets/js/components/CreateProduct.js.I could not run this files 
    # despite my best efforts. Therefore I could not complete any functionality of 
    # CreateProductView class which is under Djangoproduct.py
    # I'll try my level best to be fairly knowledgeable about this topic in the next few days. 
    # Therefore I hope you will give me an opportunity to consider the matter with a little forgiving eye

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


# class BaseVariantView(generic.View):
#     model = Product
#     template_name = 'products/list.html'
#     success_url = '/products/variants'

# Make a list of view page of Products table data
class ProductsView(ListView):
    model = Product
    template_name = 'products/list.html'
    paginate_by = 2

    # def get_context_data(self, **kwargs):
    #     print("++++++++++++++++++++++++++++++++")
    #     if self.request.method == 'POST' or self.request.method == 'GET':
    #         self.status_form = self.request.POST
    #         product_title = self.status_form["title"]
    #         variant = self.status_form["variant"]
    #         price_from = self.status_form["price_from"]
    #         price_to = self.status_form["price_to"]
    #         date = self.status_form["date"]
    #         print("++++++++++++++++++++", product_title, variant, price_from, date, price_to)


    #search product variant function
    def post(self, request):
        self.status_form = self.request.POST
        product_title = self.status_form["title"]
        variant = self.status_form["variant"]
        price_from = self.status_form["price_from"]
        price_to = self.status_form["price_to"]
        date = self.status_form["date"]
        ProductPriceFilterData = []
        products = []
        productVariantPrice = []
        #Data Filter: 7/ Make a product �lter with product title, product variant,price range and date
        if product_title and variant and price_from and price_to and date:
            productVariantPrice = ProductVariantPrice.objects.filter(price__range=(price_from, price_to))
            prods = Product.objects.filter(title__icontains=product_title, created_at__gte=date)
            for p in productVariantPrice:
                for prod in prods:
                    if p.product == prod:
                        try:
                            if varint_filter:
                                products.append(prod)
                        except:
                            products.append(prod)
        elif variant:
            varint_filter = ProductVariant.objects.filter(variant_title=variant)
            for prod in varint_filter:
                ProductPriceFilter  = ProductVariantPrice.objects.filter(product=prod.product.pk)
                products.append(prod.product)
                ProductPriceFilterData.append(ProductPriceFilter)
        productCount = len(products)
        variants = ProductVariant.objects.values("variant_title").distinct()
        date_dict = {
            "products":products,
            "productVariantPrice":productVariantPrice,
            "productCount":productCount,
            "variants":variants,
            'ProductPriceFilterData':ProductPriceFilterData
        }
        return render(request, 'products/list.html', context=date_dict)


    # All product view list function / Data List: 4 / Make a list of view page of Products table data
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProductsView, self).get_context_data(**kwargs)
        list_product = Product.objects.all()
        paginator = Paginator(list_product, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
        context['products'] = file_exams
        context["productVariantPrice"] = ProductVariantPrice.objects.all()
        context["productCount"] = len(context['products'])
        context["variants"] = ProductVariant.objects.values("variant_title").distinct()
        return context