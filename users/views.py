from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from users.models import Location, Tour
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

@login_required
def save_tour(request):
    if request.method == "POST":
        tour_data = request.POST.get('tourData')
        # Process or save the 'tour_data' as needed
        return redirect('thank_you')  # Redirect to the Thank You page

@login_required
def thank_you(request):
    return render(request, 'users/thank_you.html')

def search_locations(request):
    query = request.GET.get('q')

    if query:
        locations = Location.objects.filter(name__icontains=query)
    else:
        locations = Location.objects.all()

    return render(request, 'users/locations.html', {'locations': locations, 'query': query})

def location_detail(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    context = {'location': location}
    return render(request, 'users/location_detail.html', context)


@login_required
def rate_location(request, pk):
    location = get_object_or_404(Location, pk=pk)

    if request.method == 'POST':
        if request.user in location.voters.all():
            messages.error(request, "You've already voted for this location.")
        else: 
            rating = float(request.POST.get('rating'))            
            newrating = ((location.rating * location.votes) + rating) / (location.votes + 1)
            newrating = round(newrating, 2)
            location.rating = newrating
            location.votes +=1
            location.voters.add(request.user)
            location.save()
            messages.success(request, "Thank you for voting!")
            return HttpResponseRedirect(reverse('location_detail', args=[pk]))

    return render(request, 'users/location_detail.html', {'location': location})

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'

    def post(self, request, *args, **kwargs):
        selected_tour_id = int(request.POST.get('selectedTour'))

        if selected_tour_id:
            try:
                tour = Tour.objects.get(id=selected_tour_id)

                form_action = request.POST.get('formAction', None)
                if form_action == "Approve":
                    tour.premade = True
                    tour.admin = False
                    tour.save()
                    return redirect('discovery')
                elif form_action == "Deny":
                    tour.admin = False
                    tour.save()
                    return redirect('home')
                elif form_action == "Delete":
                    tour.admin = False
                    tour.selected = False
                    tour.save()
                elif form_action == "Submit":
                    tour.admin = True
                    tour.save()

            except (ValueError, Tour.DoesNotExist):
                pass

        return redirect('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tours = Tour.objects.filter(selected=True, user_name=self.request.user.username)
        context['tours'] = tours
        context['tours_serial'] = serializers.serialize("json", tours)
        location_pks = tours.values_list('locations', flat=True).distinct()
        locations = Location.objects.filter(pk__in=location_pks)
        locations_serial = serializers.serialize("json", locations)
        context['locations_serial'] = locations_serial
        return context


class MyView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'


def home(request):
    if request.user.is_authenticated:
        
        # Check if user is an admin
        if request.user.is_staff or request.user.is_superuser:
            tours = Tour.objects.all()     
            tours = Tour.objects.filter(admin=True)
            return render(request, 'users/admin.html', {'user': request.user, 'tours': tours})
        else:
            return render(request, 'users/home.html', {'user': request.user})
    else:
        return HttpResponseForbidden("You must be logged in to access this content.")


@login_required
def create_tours(request):
    if request.method == 'POST':
        # Extract selected location names from the form submission
        tour_data = request.POST.get('tourData')
        tour_name = request.POST.get('tourName')

        # Parse the JSON data
        import json
        tour_data = json.loads(tour_data)

        tour = Tour.objects.create(tour_name=tour_name, premade=False, selected = True, user_name = request.user.username)
        for location in tour_data:
            name = location['name']
            vicinity = location['vicinity']
            try:
                location = Location.objects.get(name=name)
                tour.locations.add(location)
            except Location.DoesNotExist:
                new_location = Location.objects.create(name=name,address = vicinity)
                new_location.save()
                tour.locations.add(new_location)
            tour.save()
        return redirect('thank_you')

    locations = Location.objects.filter(discovery=True)
    # Split the locations into two separate lists
    num_locations = len(locations)
    half_num_locations = num_locations // 2
    first_half = locations[:half_num_locations]
    second_half = locations[half_num_locations:]
    context = {
        'user':request.user,
        'locations_first_half':first_half,
        'locations_second_half':second_half,
        'locations_serial':serializers.serialize("json",locations)
    }

    return render(request, 'users/create_tours.html', context)

class DiscoveryView(LoginRequiredMixin, TemplateView):
    template_name = 'users/discovery.html'

    def post(self, request, *args, **kwargs):
        # Handle the POST request here
        selected_tour_id = int(request.POST.get('selectedTour'))

        if selected_tour_id:
            try:
                tour = Tour.objects.get(id=selected_tour_id)
                tour.selected = True
                tour.save()
            except (ValueError, Tour.DoesNotExist):
                pass    
        
        return redirect('dashboard')
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tours = Tour.objects.filter(premade = True)
        tours_serial = serializers.serialize("json",tours)
        context['tours_serial'] = tours_serial
        context['tours'] = tours
        location_pks = tours.values_list('locations', flat=True).distinct()
        locations = Location.objects.filter(pk__in=location_pks)
        locations_serial = serializers.serialize("json",locations)
        context['locations_serial'] = locations_serial
        return context

def start_tour(request, tour_id):

    tour = Tour.objects.get(id = tour_id)
    locations = tour.locations.all()

    context = {
        'locations': locations,
        'locations_serial': serializers.serialize("json",locations),
        'tour':tour,
        'tour_serial':serializers.serialize("json",[tour])
    }

    return render(request, 'users/start_tour.html', context)

@login_required
def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    if request.method == "POST":
        tour.delete()
        return redirect('dashboard')
    else:
        return redirect('dashboard')