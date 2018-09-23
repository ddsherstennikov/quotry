from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from datetime import datetime

from quotry.models import Tag, Quote
from quotry.forms import TagForm, QuoteForm, UserForm, UserProfileForm

from registration.backends.simple.views import RegistrationView

from quotry.bing_search import run_query

#### Intro -----------------------------------------------------------------------------------------

def index(request):
    # test cookies part 1 of 2
    # request.session.set_test_cookie()

    tag_list = Tag.objects.order_by('-favs')[:5]
    quote_list = Quote.objects.order_by('-likes')[:5]
    context_dict = {'tags': tag_list, 'quotes': quote_list, 'visits' : get_visits(request)}

    return render(request,'quotry/index.html', context_dict)


@login_required
def about(request):
    return render(request, 'quotry/about.html', {'visits': get_visits(request)} )


@login_required
def restricted(request):
    #test cookies part 2 of 2
    #if request.session.test_cookie_worked():
    #    print ">>>> TEST COOKIE WORKED!"
    #    request.session.delete_test_cookie()

    return render(request, 'quotry/restricted.html', {'visits': get_visits(request)} )


#### Profile ---------------------------------------------------------------------------------------

# Redirects the user to if successful at registration
# Necessary for django-registration-redux
class QuotryRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return 'add_profile'


@login_required
def add_profile(request):

    # HTTP POST => process data from forms
    if request.method == 'POST':

        user = request.user
        profile_form = UserProfileForm(data=request.POST)

        if profile_form.is_valid():
            # Delay saving the UserProfile model until we're donw w/ integrity problems.
            profile = profile_form.save(commit=False)
            # add link to User instance to UserProfile instance
            profile.user = user

            # If user provided a profile picture, request |--<pic>--> UserProfile obj
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # now UserProfile obj is saved in db
            profile.save()

            # redirect to index
            return HttpResponseRedirect(reverse('index'))

        # Invalid form - error output in quote and term
        else:
            print profile_form.errors

    # HTTP GET => render blank ProfileForm, ready-for-input
    else:
        profile_form = UserProfileForm()

    # Render 'add_profile' template
    return render(request, 'quotry/add_profile.html', {'profile_form': UserProfileForm(), 'visits': get_visits(request)} )


@login_required
def profile(request):
    """ 
    #test cookies part 2 of 2
    if request.session.test_cookie_worked():
        print ">>>> TEST COOKIE WORKED!"
        request.session.delete_test_cookie()
    """
    # init, status quo data
    user = request.user
    profile = user.userprofile

    # HTTP POST => process data from forms
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            if user_form.has_changed():
                user.email = user_form.cleaned_data['email']
                user.save()

            if profile_form.has_changed():
                profile.website = profile_form.cleaned_data['website']
                if request.POST.get('picture-clear') == u'on':
                    profile.picture = None
                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']
                profile.save()
            
            # redirect to index
            return index(request)

        # Invalid form - error output in quote and term
        else:
            print user_form.errors, profile_form.errors

    # HTTP GET => render ProfileForm & UserProfile Forms with what is known
    else:
        uf_data = {'email': user.email}
        user_form = UserForm(uf_data, initial=uf_data)

        pf_data = {'website': profile.website, 
                   'picture': profile.picture}
        profile_form = UserProfileForm(pf_data, initial=pf_data)

    # Render the template depending on the context.
    return render(request, 'quotry/profile.html',
                    {'user_form': user_form, 'profile_form': profile_form, 'visits': get_visits(request) } )


#### Counters --------------------------------------------------------------------------------------

@login_required
def get_visits(request):

    # counters work for auth users only
    if request.user.is_authenticated:

        # get 'visits' counter
        visits = request.session.get('visits')
        if not visits:
            visits = 1

        # get 'last_visit' stamp
        last_visit = request.session.get('last_visit')
        reset_last_visit_time = False

        # has 'last_visit' stamp
        if last_visit:
            last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

            # timedelta between visits is 5m for test
            if (datetime.now() - last_visit_time).days > 1:
                visits += 1
                reset_last_visit_time = True

        # no 'last_visit' stamp
        else:
            # sid cookie 'last_visit' none, CRT it =now()
            reset_last_visit_time = True

        if reset_last_visit_time:
            request.session['last_visit'] = str(datetime.now())
            request.session['visits'] = visits

        return visits

    # everybody else is treated a 1st-timer
    # if he is logged out
    else:
        return 1


@login_required
def fav_tag(request):
    #add: track and record user favs here

    tag_id = None
    if request.method == 'GET':
        tag_id = request.GET['tag_id']

    favs = 0
    if tag_id:
        tag = Tag.objects.get(id=int(tag_id))
        if tag:
            favs = tag.favs + 1
            tag.favs = favs
            tag.save()

    return HttpResponse(favs)

#### Payload ---------------------------------------------------------------------------------------

@login_required
def tag(request, tag_name_slug):

    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None

    # de-comissioned bing search functionality
    #if request.method == 'POST':
    #    query = request.POST.get('query')
    #    if query:
    #        # Run our Bing function to get the results list!
    #        result_list = run_query(query.strip())
    #        context_dict['result_list'] = result_list
    #        context_dict['query'] = query

    try:
        # Try find a tag name slug with the given name => instance or exc.
        tag = Tag.objects.get(slug=tag_name_slug)
        context_dict['tag_name'] = tag.name

        # Retrieve all (>= 1) of the associated quotes instances
        quotes = Quote.objects.filter(tag=tag)
        context_dict['quotes'] = quotes

        # add tag object from db, use in templ. to verify tag exists
        context_dict['tag'] = tag

        # just in case
        context_dict['tag_name_slug'] = tag_name_slug

    except Tag.DoesNotExist:
        # template displays the "no tag" message for us
        pass

        context_dict['visits'] = get_visits(request)

        # de-comissioned bing search functionality
        #if not context_dict['query']:
        #    context_dict['query'] = tag.name

    return render(request, 'quotry/tag.html', context_dict)


@login_required
def add_tag(request):
    # A HTTP POST => create new tag from data, if valid
    if request.method == 'POST':
        form = TagForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)

        else:
            # print form errors to term
            print form.errors

    # A HTTP GET => show blank form for client to fill w/ tag info
    else:
        form = TagForm()

    # Render the form with error messages (if any).
    return render(request, 'quotry/add_tag.html', {'form': form, 'visits': get_visits(request)})


@login_required
def add_quote(request, tag_name_slug):
    try:
        current_tag = Tag.objects.get(slug=tag_name_slug)
    except Tag.DoesNotExist:
        current_tag = None

    # A HTTP POST => create new quote from data, if valid
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        
        if form.is_valid():
            if current_tag:
                quote = form.save(commit=False)
                quote.tag = current_tag
                quote.likes = 0
                quote.save()

                return tag(request, tag_name_slug)
        # print form errors to term
        else:
            print form.errors

    # A HTTP GET => show blank form for client to fill w/ quote info
    else:
        form = QuoteForm()

    context_dict = {'form':form, 'tag': current_tag,
                    'tag_name_slug': tag_name_slug, 
                    'visits': get_visits(request) }

    return render(request, 'quotry/add_quote.html', context_dict)


@login_required
def add_quote_custom(request):

    # A HTTP POST => create new quote from data, if valid
    if request.method == 'POST':
        form = QuoteForm(request.POST)

        selected_tag_name = request.POST.get('selected_tag')
        if selected_tag_name:
            selected_tag = Tag.objects.filter( name=selected_tag_name )[0]
        # print tag error to term
        else:
            print 'Tag unrecognized'

        if form.is_valid():
            if selected_tag:
                quote = form.save(commit=False)
                quote.tag = selected_tag
                quote.likes = 0
                quote.save()

                return tag(request, selected_tag.slug)
        # print form errors to term
        else:
            print form.errors

    # A HTTP GET => show blank form for client to fill w/ quote info
    else:
        form = QuoteForm()

    tag_list = Tag.objects.all()
    context_dict = {'form':form, 'visits': get_visits(request), 'tags': tag_list }

    return render(request, 'quotry/add_quote_custom.html', context_dict)


#### Utils -----------------------------------------------------------------------------------------

def get_tag_list(max_results=0, starts_with=''):
    if starts_with:
        tag_list = Tag.objects.filter(name__istartswith=starts_with)
    else:
        tag_list = Tag.objects.all()

    if max_results > 0:
        if len(tag_list) > max_results:
            tag_list = tag_list[:max_results]

    return tag_list


def suggest_tag(request):
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    tag_list = get_tag_list(10, starts_with)

    return render(request, 'quotry/tags.html', {'tags': tag_list })