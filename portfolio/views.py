from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from django.http import HttpResponse
from django.template.loader import get_template
from easy_pdf.rendering import render_to_pdf
from django.views.generic import View

# Create your views here.

now = timezone.now()
def home(request):
   return render(request, 'portfolio/home.html',
                 {'portfolio': home})

@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'portfolio/customer_list.html',
                  {'customers': customer})

@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customer})
   else:
        # edit
       form = CustomerForm(instance=customer)
   return render(request, 'portfolio/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('portfolio:customer_list')

@login_required
def stock_list(request):
   stocks = Stock.objects.filter()
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})

@login_required
def stock_new(request):
   if request.method == "POST":
       form = StockForm(request.POST)
       if form.is_valid():
           stock = form.save(commit=False)
           stock.created_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter()
           return render(request, 'portfolio/stock_list.html',
                         {'stocks': stocks})
   else:
       form = StockForm()
       # print("Else")
   return render(request, 'portfolio/stock_new.html', {'form': form})

@login_required
def stock_edit(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   if request.method == "POST":
       form = StockForm(request.POST, instance=stock)
       if form.is_valid():
           stock = form.save()
           # stock.customer = stock.id
           stock.updated_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
   else:
       # print("else")
       form = StockForm(instance=stock)
   return render(request, 'portfolio/stock_edit.html', {'form': form})

@login_required
def stock_delete(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   stock.delete()
   return redirect('portfolio:stock_list')

@login_required
def investment_list(request):
    investments = Investment.objects.filter()
    return render(request, 'portfolio/investment_list.html', {'investments': investments})

@login_required
def investment_new(request):
   if request.method == "POST":
       form = InvestementForm(request.POST)
       if form.is_valid():
           investment = form.save(commit=False)
           investment.created_date = timezone.now()
           investment.save()
           investments = Investment.objects.filter()
           return render(request, 'portfolio/investment_list.html',
                         {'investments': investments})
   else:
       form = InvestementForm()
       # print("Else")
   return render(request, 'portfolio/investment_new.html', {'form': form})

@login_required
def investment_edit(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    if request.method == "POST":
       form = InvestementForm(request.POST, instance=investment)
       if form.is_valid():
           investment = form.save()
           # stock.customer = stock.id
           investment.updated_date = timezone.now()
           investment.save()
           investments = Investment.objects.filter()
           return render(request, 'portfolio/investment_list.html', {'investments': investments})
    else:
       # print("else")
       form = InvestementForm(instance=investment)
    return render(request, 'portfolio/investment_edit.html', {'form': form})

@login_required
def investment_delete(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    investment.delete()
    return redirect('portfolio:investment_list')

@login_required
def mutualfund_list(request):
    mutualfunds = Mutualfund.objects.filter()
    return render(request, 'portfolio/mutualfund_list.html' , {'mutualfunds': mutualfunds})


@ login_required
def mutualfund_new(request):
    if request.method == "POST" :
        form = MutualfundForm(request.POST)
        if form.is_valid():
            mutualfund = form.save(commit=False)
            mutualfund.created_date = timezone.now()
            mutualfund.save()
            mutualfunds = Mutualfund.objects.filter()
            return render(request, 'portfolio/mutualfund_list.html', {'mutualfunds': mutualfunds})
    else :
        form = MutualfundForm()
        # print("Else")
        return render(request, 'portfolio/mutualfund_new.html', {'form': form})


@ login_required
def mutualfund_edit(request, pk):
    mutualfund = get_object_or_404(Mutualfund, pk=pk)
    if request.method == "POST":
        form = MutualfundForm(request.POST, instance=mutualfund)
        if form.is_valid():
            mutualfund = form.save()
           # investment.customer = investment.id
            mutualfund.updated_date = timezone.now()
            mutualfund.save()
            mutualfunds = Mutualfund.objects.filter()
            return render(request, 'portfolio/mutualfund_list.html', {'mutualfunds': mutualfunds})
    else:
        # print("else")
        form = MutualfundForm(instance=mutualfund)
        return render(request, 'portfolio/mutualfund_edit.html', {'form': form})


@ login_required
def mutualfund_delete(request, pk):
    mutualfund = get_object_or_404(Mutualfund, pk =pk)
    mutualfund.delete()
    mutualfunds = Mutualfund.objects.filter()
    return render(request, 'portfolio/mutualfund_list.html', { 'mutualfunds': mutualfunds})

@login_required
def portfolio(request,pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments =Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    mutualfunds = Mutualfund.objects.filter(customer=pk)
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
    sum_mutual_acquired_value = Mutualfund.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
    sum_mutual_recent_value = Mutualfund.objects.filter(customer=pk).aggregate(Sum('recent_value'))
   #overall_investment_results = sum_recent_value-sum_acquired_value
   # Initialize the value of the stocks
    sum_current_stocks_value = 0
    sum_of_initial_stock_value = 0

   # Loop through each stock and add the value to the total
    for stock in stocks:
         sum_current_stocks_value += stock.current_stock_value()
         sum_of_initial_stock_value += stock.initial_stock_value()

    return render(request, 'portfolio/portfolio.html', {'customers': customers,
                                                        'investments': investments,
                                                        'stocks': stocks,
                                                        'mutualfunds': mutualfunds,
                                                        'sum_acquired_value': sum_acquired_value,
                                                        'sum_recent_value': sum_recent_value,
                                                        'sum_current_stocks_value': sum_current_stocks_value,
                                                        'sum_of_initial_stock_value': sum_of_initial_stock_value,
                                                        'sum_mutual_acquired_value': sum_mutual_acquired_value,
                                                        'sum_mutual_recent_value': sum_mutual_recent_value,
                                                        })

# Lists all customers
class CustomerList(APIView):

    def get(self,request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)

@login_required()
def pdf_portfolio(request, pk):
        template = get_template('portfolio/pdf_portfolio.html')
        customer = get_object_or_404(Customer, pk=pk)
        customers = Customer.objects.filter(created_date__lte=timezone.now())
        investments = Investment.objects.filter(customer=pk)
        stocks = Stock.objects.filter(customer=pk)
        mutualfunds = Mutualfund.objects.filter(customer=pk)
        sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
        sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
        sum_mutual_acquired_value = Mutualfund.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
        sum_mutual_recent_value = Mutualfund.objects.filter(customer=pk).aggregate(Sum('recent_value'))
        # overall_investment_results = sum_recent_value-sum_acquired_value
        # Initialize the value of the stocks
        sum_current_stocks_value = 0
        sum_of_initial_stock_value = 0
        for stock in stocks:
            sum_current_stocks_value += stock.current_stock_value()
            sum_of_initial_stock_value += stock.initial_stock_value()
        context = {'customers': customers,
                   'investments': investments,
                   'stocks': stocks,
                   'sum_acquired_value': sum_acquired_value,
                   'sum_recent_value': sum_recent_value,
                   'sum_current_stocks_value': sum_current_stocks_value,
                   'sum_of_initial_stock_value': sum_of_initial_stock_value,
                   'mutualfunds': mutualfunds,
                   'sum_mutual_acquired_value': sum_mutual_acquired_value,
                   'sum_mutual_recent_value': sum_mutual_recent_value,
                   }
        html = template.render(context)

        # 'email_success': email_success})
        pdf = render_to_pdf('portfolio/pdf_portfolio.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = 'pdf_portfolio_' + str(customer.name) + '.pdf'
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("not found")


@login_required
def generate_portfolio_pdf(request, pk, context):
    customer = get_object_or_404(Customer, pk=pk)
    template = get_template('portfolio/pdf_portfolio.html')

    html = template.render(context)
    pdf = render_to_pdf('portfolio/pdf_portfolio.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename= "pdf_pdf_portfolio_{}.pdf"'.format(customer.name)
        return pdf
    return HttpResponse("Not Found")
