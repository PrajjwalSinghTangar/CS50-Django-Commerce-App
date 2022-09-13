from sqlite3 import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from auctions.models import User,Listing,Category,WatchList,Bidding,Comment
from auctions.forms import create_listing_form

# Create your views here.
def index(request):
    auction_items = Listing.objects.filter(sold=False)

    context = {
        "auction_items" : auction_items
    }

    return render(request, 'auctions/index.html', context)

def auth_login(request):
    if request.method == 'POST':

        # to login
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        #check authentication
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })

    return render(request, 'auctions/login.html')

def auth_register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]

        #Password Check
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password != confirm_password:
            return render(request, 'auctions/register.html', {
                "message" : "Password didn't match!"
            })

        #Attempt creating a new user!
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def auth_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def categories(request):
    category = None
    items = None

    if request.method == "POST":
        category = request.POST["categories"]
        items = Listing.objects.filter(category = category, sold=False)

    context = {
        "categories" : Category.objects.all(),
        "items" : items,
        "category" : Category.objects.get(id=category).category if category is not None else ""
    }


    return render(request, "auctions/categories.html", context)

@login_required
def create_listing_info(request):
    title = request.POST["title"]
    description = request.POST["description"]
    bid = request.POST["bid"]
    image_url = request.POST["image_url"]

    return title,description,bid,image_url

@login_required
def create_listing(request):
    categorylist = Category.objects.all()
    context = {
        "categories" : categorylist
    }   
    
    if request.method == "POST":
        form = create_listing_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            bid = form.cleaned_data["bid"]
            image_url = form.cleaned_data["image_url"]
            user = request.user
            category_id = Category.objects.get(id=request.POST["categories"])
            Listing.objects.create(user = user, title = title, description = description, 
            bid = bid, image_url = image_url, category = category_id)

        return HttpResponseRedirect(reverse('index'))
    
    else:
        return render(request, 'auctions/create_listing.html', context)

#######    ######     ############   ######    ****
##    ###  #######   ############    #######    ****
##     ##  ##    ##       ##        ##    ##
##     ##  ##    ##       ##        ##    ##
##     ##  ########       ##        ########
##     ##  ##    ##       ##        ##    ##
########   ##    ##       ##        ##    ##

@login_required
def listing_data(request,key):
    listing = Listing.objects.get(id=key)
    user = request.user
    is_owner = True if listing.user == user else False
    category = Category.objects.get(category=listing.category)
    watchlist = WatchList.objects.filter(user = user, listing = listing)
    comments = Comment.objects.filter(listing=listing.id).values("comment")
    if watchlist:
        watchlist = WatchList.objects.get(user = user, listing = listing)
        
    return listing, user, is_owner, category,watchlist,comments

# Listing
@login_required(login_url='/login')
def listing(request,key):
    data = listing_data(request,key)
    listing, user, is_owner, category= data[0],data[1],data[2],data[3]

    if request.method == "POST":
        comment = request.POST["comment"]
        if comment is not None:
               Comment.objects.create(user=user,listing=listing,comment=comment)

    return render(request, "auctions/edit_listing.html", {
        "listing" : listing,
        "user" : user,
        "is_owner" : is_owner,
        "category" : category,
        "comments" : Comment.objects.filter(listing=listing.id),
        "watchlist_item_exists" : WatchList.objects.filter(user = user, listing = listing).values('watchlist')
    })

#Bidding

@login_required
def bidding(request,key):
    data = listing_data(request,key)
    listing, user, is_owner, category = data[0],data[1],data[2],data[3]
    if request.method == 'POST':
        bidding_request = request.POST["bid"]
        listing.bid = float(bidding_request)
        listing.save()
        Bidding.objects.create(user = user, bid = bidding_request, listing = listing)

    context = {
        "listing" : listing,
        "user" : user,
        "is_owner" : is_owner,
        "category" : category,
    }

    return render(request, "auctions/edit_listing.html", context)

# WatchList

@login_required
def watchlist(request):
    watchlist = WatchList.objects.filter(user=request.user,watchlist=True).values('listing')
    watchlist_items = Listing.objects.filter(id__in= watchlist)

    return render(request, 'auctions/watchlist.html', {
        'watchlist_items' : watchlist_items
    })

@login_required
def watchlist_item_remove(request,key):
    data = listing_data(request, key)
    watchlist_data = data[4]

    watchlist_data.watchlist = False
    watchlist_data.delete()

    watchlist = WatchList.objects.filter(user=request.user,watchlist=True).values('listing')
    watchlist_items = Listing.objects.filter(id__in= watchlist)

    return render(request, 'auctions/watchlist.html', {
        'watchlist_items' : watchlist_items
    })


@login_required
def watchlist_add(request,key):
    data = listing_data(request, key)
    listing, user, is_owner, category = data[0],data[1],data[2],data[3]

    watchlist_item_exists = WatchList.objects.filter(user=user,listing=listing)
    if watchlist_item_exists:
        watchlist_item_exists= WatchList.objects.get(user=user,listing=listing)
        watchlist_item_exists.watchlist = True
        watchlist_item_exists.save()
    else:
        WatchList.objects.create(user=user,listing=listing,watchlist=True)

    return render(request, 'auctions/edit_listing.html', {
        "listing" : listing,
        "user" : user,
        "is_owner" : is_owner,
        "category" : category,
        "watchlist_item_exists" : WatchList.objects.get(user = user, listing = listing).watchlist
    })
    
@login_required
def watchlist_remove(request,key):
    data = listing_data(request, key)
    listing, user, is_owner, category, watchlist_data = data[0],data[1],data[2],data[3],data[4]

    watchlist_data.watchlist = False
    watchlist_data.delete()

    watchlist = WatchList.objects.filter(user=request.user,watchlist=True).values('listing')
    watchlist_items = Listing.objects.filter(id__in= watchlist)

    return render(request, 'auctions/edit_listing.html', {
        "listing" : listing,
        "user" : user,
        "is_owner" : is_owner,
        "category" : category,
        'watchlist_items' : watchlist_items
    })

@login_required
def bid_close(request,key):
    data = listing_data(request, key)
    listing = data[0]
    listing.sold = True
    listing.save()
    return index(request)

