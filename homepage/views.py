from django.shortcuts import render, redirect, get_object_or_404
from databases.models import Restaurant, Deal, Location, Customer
from .forms import RestaurantForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request, 'index.html', {})


def is_valid_queryparam(param):
    return param != '' and param is not None

def foodDeals(request):
    count = Restaurant.objects.count()
    allRestaurants = Restaurant.objects.all()
    allDeals= Deal.objects.all().values()
    allLocations = Location.objects.all().values()

    loc = request.GET.get('loc')
    deal = request.GET.get('deal')
    search = request.GET.get('search-bar')

    # print(loc)
    # print(deal)
    # print(search)

    if is_valid_queryparam(loc):
        allRestaurants = allRestaurants.filter(rest_location__location_name = loc)

    if is_valid_queryparam(deal):
        allRestaurants = allRestaurants.filter(deals__deal_name = deal)

    if is_valid_queryparam(search):
        allRestaurants = allRestaurants.filter(rest_name__icontains = search)

    return render(request, 'food-deals.html', {'varAllRestaurants': allRestaurants,
                                               'varAllDeals': allDeals,
                                               'varAllLocations': allLocations,
                                               'varTotalCount': count,
                                               })
def favorites(request):
    count = Restaurant.objects.count()
    allRestaurants = Restaurant.objects.all()
    allDeals= Deal.objects.all().values()
    return render(request, 'favorites.html', {'varAllRestaurants': allRestaurants,
                                               'varAllDeals': allDeals,
                                               'totalCount': count
                                               })

def about(request):
    return render(request, 'about.html', {})

def FAQ(request):
    return render(request, 'FAQ.html', {})

def login_required_view(request):
    return render(request, 'login_required.html')

# @login_required
@login_required(login_url='login-required')
def create_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            new_restaurant = form.save(commit=False)
            new_restaurant.save()
            request.user.customer.favorite_rest.add(new_restaurant)
            # return redirect('create-rest.html', pk=new_restaurant.pk)
            return redirect('food-deals')
    else:
        form = RestaurantForm()
    return render(request, 'create-rest.html', {'form': form})

@login_required(login_url='login-required')
def add_to_favorites(request, id):
    #fav = get_object_or_404(Restaurant, id=id)
    x = get_object_or_404(Customer, id=request.user.id)
    if x.favorite_rest.filter(id=id).exists():
        x.favorite_rest.remove(id)
    else:
        x.favorite_rest.add(id)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
