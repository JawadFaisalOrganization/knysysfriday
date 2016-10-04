from django.shortcuts import render
from django.contrib import auth
from django.core.urlresolvers import reverse
from djoser_jac.models import CustomUser
from djoser_jac.models import Area, Parish
from django.shortcuts import get_object_or_404
from ad_rotation.models import *
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django import forms
from django.core.mail import EmailMessage
from django.db import IntegrityError
from djoser_jac.models import Area, Parish
from django.core.urlresolvers import reverse
from ad_rotation.models import Subcategory
from jac_api.models import Post
from jac_api.models import Posting
from jac_api.models import Subcategory2
from jac_api.models import Formfield
from django.core import serializers
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from ad_rotation.models import *
from ad_rotation.views import *

def index(request):
  return render(request, 'web/index.html', {})

def input_new_password(request, uid, token):
                
  return render(request, 'web/input_new_password.html', {'uid': uid, 'token': token,})

def thankyou(request):
      return render(request, 'web/thank-you.html', {})

def categorytable_view(request):
  #http://stackoverflow.com/questions/30997666/how-to-work-with-django-rest-framework-in-the-templates
  return render(request, 'web/categorytable.html')

def info_page(request):
    query_parish_results = Parish.objects.all().order_by('name')
    query_area_results = Area.objects.all().order_by('name')
    errors = []
    form = []
    if request.method == 'POST':
        score = ''
        url = ''
        try:
            for value in request.POST['inlineRadioOptions']:
                score = score + value
            emailString = '\n First Name : '+ str(request.POST['fname']) +\
            '\n Last Name : '+ str(request.POST['lname'])+\
            '\n Business Name : '+ str(request.POST['bname'])+\
            '\n Business Category : '+ str(request.POST['bcategory'])+\
            '\n Business Address : '+ str(request.POST['baddress'])+\
            '\n Unit No : '+ str(request.POST['sunitno'])+\
            '\n Parish : '+ str(request.POST['uparish'])+\
            '\n Kignston : '+ str(request.POST['area'])+\
            '\n Cell Phone # 01 : '+ str(request.POST['cellphone1'])+\
            '\n Cell Phone # 02 : '+ str(request.POST['cellphone2'])+\
            '\n Email Address : '+ str(request.POST['emailaddress'])+\
            '\n SUnit No : '+ str(request.POST['ssunit'])+\
            '\n User Name : '+ str(request.POST['username'])+\
            '\n Password : '+ str(request.POST['password'])+\
            '\n App Name : '+ str(request.POST['appname'])+\
            '\n AppIcone Name : '+ str(request.POST['appiconname'])+\
            '\n Website : '+ str(request.POST['website'])+\
            '\n C Email APPI : '+ str(request.POST['cemailappi'])+\
            '\n App Description : '+ str(request.POST['appdesc'])+\
            '\n App Price : '+ str(request.POST['appprice'])+\
            '\n Amount : '+ str(request.POST['amount_1'])+\
            '\n Billing Address First Name : '+ str(request.POST['bafname'])+\
            '\n Billing Address Last Name : '+ str(request.POST['balname'])+\
            '\n Billing Address : '+ str(request.POST['baAddress'])+\
            '\n Apt Unit : '+ str(request.POST['aptunit'])+\
            '\n Billing Address Parish : '+ str(request.POST['bparish'])+\
            '\n Billing Address Kingston : '+ str(request.POST['bakingston'])+\
            '\n Billing Address City : '+ str(request.POST['bacity'])+\
            '\n Billing Address State : '+ str(request.POST['bastate'])+\
            '\n Billing Address zip : '+ str(request.POST['bazip'])+\
            '\n Credit Card Name : '+ str(request.POST['creditcardname'])+\
            '\n Payment Type : '+ str(score)+\
            '\n Credit Card Number : '+ str(request.POST['creditcardnmber'])+\
            '\n Expire Date : '+ str(request.POST['expdate'])+\
            '\n Security Code : '+ str(request.POST['seccode'])+\
            '\n Bill zip : '+ str(request.POST['billzip'])+\
            '\n Bill Address Country : '+ str(request.POST['bacountry']);
        except Exception, e:
            error = 'Invalid Input'
            form_data = request.POST
            return  render(request,'web/info_page.html',\
            {"Error":error, "parish":query_parish_results,"area":query_area_results, "form_data":form_data})    
    
        # TODO-Create a separate function for inserting data to the db
        parish = get_object_or_404(Parish, pk=request.POST.get('uparish'))
        area = get_object_or_404(Area, pk= int(request.POST.get('area')))
        try:
            advertiser = Advertiser(email = request.POST.get('emailaddress'),area = area, parish = parish, username = request.POST.get('username'), password = request.POST.get('password'), company_name = request.POST.get('bname'), 
            company_address = request.POST.get('baddress'), unit = request.POST.get('sunitno'), business_category = request.POST.get('bcategory'))
            advertiser.set_password(request.POST.get('password'))
            advertiser.save()
        except:
            error = 'A user with that email is already exists'
            form_data = request.POST
            return  render(request,'web/info_page.html',\
            {"Error":error, "parish":query_parish_results,"area":query_area_results, "form_data":form_data})    

        contact = Contact(email = request.POST.get('emailaddress'), first_name = request.POST.get('fname'),
        last_name = request.POST.get('lname'), phone1 = request.POST.get('cellphone1'), phone2 = request.POST.get('cellphone2'), advertiser_id = advertiser.id)
        contact.save()
        try:
          send_mail(
              ' ',
              emailString,
              ' ',
              ['developer1.jac@gmail.com'],
          )
          my_paypal_email = "urehman.knysys-facilitator@gmail.com"                                                               
          return_page = "http://192.168.0.159:8000/"
          notify_page = "http://192.168.0.159:8000/thank-you/"
          cancel_page = "http://192.168.0.159:8000/"
          item_price = str(request.POST['amount_1'])
          item_name = "Payment"
          item_quantity = "1"
          item_cod = "T100"
          currency_type = "USD"  
          url = ''
         # url += "https://www.paypal.com/xclick/"
          url += "https://www.sandbox.paypal.com/us/cgi-bin/webscr"
          url += "?cmd=_xclick"
          url += "&business=" + my_paypal_email
          url += "&return=" + return_page
          url += "&notify_url=" + notify_page
          url += "&cancel_return=" +  cancel_page
          url += "&quantity=" + item_quantity
          url += "&item_name=" + item_name
          url += "&item_number=" + item_cod
          url += "&amount=" + item_price
          url += "&no_shipping=1"
          url += "&no_note=0"
          url += "&currency_code=" + currency_type 
          return HttpResponseRedirect(url)
        except Exception, err: 
            return HttpResponse(str(err))
    return render(request, 'web/info_page.html', {"parish":query_parish_results,"area":query_area_results,"form": form})
    
def jac_api(request):
  return render(request, 'web/jac_api.html', {})

def contact(request):
    errors = []
    if request.method == 'POST':

          subjectString = 'Inquiry';
          relatedToString = '';

          if(request.POST.get('placingAd')=='on'):
              relatedToString = relatedToString + '\n* Placing an Ad on the JAC app';
          if(request.POST.get('consumerAccount')=='on'):
              relatedToString = relatedToString + '\n* Consumer Account';
          if(request.POST.get('jacAPI')=='on'):
              relatedToString = relatedToString + '\n* JAC API';
          if(request.POST.get('businessAccount')=='on'):
              relatedToString = relatedToString + '\n* Business Account';
          if(request.POST.get('businessMobileApp')=='on'):
              relatedToString = relatedToString + '\n* Business Mobile App';
          if(request.POST.get('other')=='on'):
              relatedToString = relatedToString + '\n* Other';

          if(relatedToString): 
              relatedToString = 'Related to :-\n' + relatedToString + '\n\n';


          emailString = relatedToString + 'Name : '+str(request.POST['firstName'])+\
          ' '+str(request.POST['lastName'])+\
          '\nCompany Name : '+str(request.POST['companyName'])+\
          '\nEmail : '+str(request.POST['senderEmail'])+\
          '\nCell : '+str(request.POST['cellNumber'])+\
          '\nCompany Telephone Number : '+str(request.POST['companyTelephoneNumber'])+\
          '\nComments : '+str(request.POST['comments']);

          try:
            mail = EmailMessage(subjectString, emailString,request.POST['senderEmail'], ['developer1.jac@gmail.com'])
            mail.send()

            return render(request,'web/contact.html',{"successMsg":"Thank You! Your form has been submitted successfully"})
          except Exception, err: 
            return HttpResponse(str(err))
    return render(request, 'web/contact.html', {'errors': errors})

@login_required
def consumer_user_landing_page(request):
  sub_cate_dict = {}

  categories = Category.objects.all().order_by('name')
  for category in categories:
    sub_categories  = Subcategory.objects.filter(category_id=category.id)
    sub_cate_dict[category.id] = sub_categories

  #print request.uid,'request.user'
  current_user = request.user
  user_id = current_user.id

  orderby = request.GET.get('orderby')
  if orderby == 'date':
    order_by='post__posted_on'
  elif  orderby == 'category':
    order_by='post__category__name'
  else:
    order_by = 'post__id'

  condition = request.GET.get('list')

  if condition=='post':
    my_listing = Posting.objects.filter(post__owner=user_id, post__is_posted=True).select_related().order_by(order_by)
  elif condition =='unpost':
    my_listing = Posting.objects.filter(post__owner=user_id, post__is_posted=False).select_related().order_by(order_by)
  else:
    my_listing = Posting.objects.filter(post__owner=user_id).select_related().order_by(order_by)

  paginator = Paginator(my_listing, 50)

  page = request.GET.get('page')
  try:
    my_listing_data = paginator.page(page)
  except PageNotAnInteger:
      # If page is not an integer, deliver first page.
      my_listing_data = paginator.page(1)
  except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
      my_listing_data = paginator.page(paginator.num_pages)

  return render(request, 'web/categorytable.html', {"categories":categories,"sub_categories":sub_cate_dict,\
    'my_listing':my_listing_data, 'record':len(my_listing)})

@require_http_methods(['POST'])
def get_sub_subcategory(request):
  data=request.POST
  sub_sub_categories  = Subcategory2.objects.filter(subcategory_id=data['sub_cate_id'])
  data = serializers.serialize('json', sub_sub_categories)
  query_parish_results = Parish.objects.all().order_by('name')
  query_area_results = Area.objects.all().order_by('name')
  p = serializers.serialize('json', query_parish_results)
  a = serializers.serialize('json', query_area_results)
  print p
  print a
  print 'HAHAHAHAHAHAHAHAHAHHAHAHAHAHAHAHAAHHAAHAHAH'
  print data + p + a
  print 'HAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAH'
  return HttpResponse(a)
  #return HttpResponse({"data": data, "parish": p, "area": a})

@require_http_methods(['POST'])
def get_listing_category(request):
  data = request.POST
  form_fields = []
  is_featured = True if data['featured'] == '1' else False
  if data['cate_type'] == 'sub_cate':
      # parish = get_object_or_404(Parish)
      # area = get_object_or_404(Area)
      form_fields  = Formfield.objects.filter(subcategory=data['cate_id'], featured=is_featured).order_by('field_type')
  elif data['cate_type'] == 'sub_sub_cate':
    form_fields  = Formfield.objects.filter(subcategory2=data['cate_id'], featured=is_featured).order_by('field_type')
  data = serializers.serialize('json', form_fields)

  # return HttpResponse({"data":data, "parish":p ,"area":a})
  return HttpResponse(data)


# def my_listing(self):
#         order_by_clause = self.request.GET.get('order_by', '-posted_on')
#         return models.Post.objects.filter(owner=CustomUser.get_user(self.request.user)).order_by(order_by_clause)

def consumer_login(request):
    if request.user.is_authenticated():
        return render(request, 'web/index.html')

    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        login_user = auth.authenticate(email=email, password=password)

        if login_user is not None:
            try:
                CustomUser.get_user(login_user)
                auth.login(request, login_user)
                return HttpResponseRedirect(reverse('consumer_user_landing_page'))
            except:
                auth.logout(request)
                return HttpResponseRedirect(reverse('index'))

        else:
            return HttpResponseRedirect(reverse('index'), {'error': 'the login was unsuccessful, user auth failed'})

    return render(request, 'web/index.html')

def create_business_account(request):
  query_parish_results = Parish.objects.all().order_by('name')
  query_area_results = Area.objects.all().order_by('name')
  if request.method == 'POST':
     parish = get_object_or_404(Parish, pk=request.POST.get('parish'))
     area = get_object_or_404(Area, pk= int(request.POST.get('area')))
     try:
        advertiser = Advertiser(email = request.POST.get('user_email'),area = area, parish = parish, username = request.POST.get('user_name'), company_name = request.POST.get('business_name'),
        company_address = request.POST.get('address'), unit = request.POST.get('unit'), business_category = request.POST.get('business_category'))
        advertiser.set_password(request.POST.get('password'))
        advertiser.save()
     except IntegrityError as e:
        error = 'A user with that email already exists'
        form_data = request.POST
        return  render(request,'web/create_business_account.html',\
        {"Error":error, "parish":query_parish_results,"area":query_area_results, "form_data":form_data})
  
     contact = Contact(email = request.POST.get('user_email'), first_name = request.POST.get('first_name'),
     last_name = request.POST.get('last_name'), phone1 = request.POST.get('phone_no'), phone2 = request.POST.get('phone_no2'), advertiser_id = advertiser.id)
     contact.save()
     return HttpResponseRedirect(reverse('index'))
  else:
     return render(request, 'web/create_business_account.html',{"parish":query_parish_results,"area":query_area_results})

def business_login(request):
    if request.user.is_authenticated():
        return render(request, 'web/index.html')

    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        login_user = auth.authenticate(email=email, password=password)

        if login_user is not None:
            try:
                Advertiser.objects.get(profile_ptr_id=login_user.id)
                auth.login(request, login_user)
                return HttpResponseRedirect(reverse('business_user_landing_first_page'))
            except:
                auth.logout(request)
                return HttpResponseRedirect(reverse('index'))

        else:
            return HttpResponseRedirect(reverse('index'),
              {'error': 'the login was unsuccessful, user auth failed'})

    return render(request, 'web/index.html')

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def career(request):
    errors = []
    if request.method == 'POST':

          subjectString = 'Resume : ' + str(request.POST['firstName']) + ' ' +  str(request.POST['lastName']);

          emailString = 'Name : '+str(request.POST['firstName'])+\
          ' '+str(request.POST['lastName'])+\
          '\nEmail : '+str(request.POST['senderEmail'])+\
          '\nCell : '+str(request.POST['cellNumber'])+\
          '\nComments : '+str(request.POST['comments']);

          attachment = request.FILES.get("resumePDF", None)
          
          try:
            mail = EmailMessage(subjectString, emailString,request.POST['senderEmail'], ['developer1.jac@gmail.com'])
            
            if attachment:
              mail.attach(attachment.name, attachment.read(), attachment.content_type)
            
            mail.send()
            
            return render(request,'web/career.html',{"successMsg":"Thank you, the resume has been submitted successfully"})
          
          except Exception, err: 
            return HttpResponse(str(err))
    
    return render(request, 'web/career.html', {'errors': errors})

@login_required
def business_user_landing_first_page(request):

    my_campaigns = get_campaign_stats(request)['my_campaigns']
    total_number_of_campaigns = len(my_campaigns)
    avg_campaign_duration = get_campaign_stats(request)['avg_campaign_duration']
    total_number_of_times_ads_displayed = get_count_ads_area_and_parish(request)['my_ads_displayed_count']
    total_number_of_ad_clicks = get_total_clicks_on_my_ads(request)['my_clicks']
    total_number_of_parishes = get_count_ads_area_and_parish(request)['my_parishes']
    total_number_of_areas = get_count_ads_area_and_parish(request)['my_areas']
    total_number_of_categories = get_total_categories(request)['my_categories']
    total_ad_cost = get_total_ad_cost(request)
    avg_ad_cost = 0 if total_ad_cost == 0 else round(total_ad_cost/total_number_of_campaigns, 2)


    return render(request, 'web/business_user_landing_first_page.html', 
                            {
                              "my_campaigns":my_campaigns,
                              "total_number_of_campaigns":total_number_of_campaigns,
                              "avg_campaign_duration":avg_campaign_duration,
                              "total_number_of_times_ads_displayed":total_number_of_times_ads_displayed,
                              "total_number_of_ad_clicks":total_number_of_ad_clicks,
                              "total_number_of_parishes":total_number_of_parishes,
                              "total_number_of_areas":total_number_of_areas,
                              "total_number_of_categories":total_number_of_categories,
                              "avg_ad_cost":avg_ad_cost,
                              "total_ad_costs":total_ad_cost,
                            })

@require_http_methods(['POST'])
def change_campaign_active_status(request):
    campaign_id = request.POST['id']
    if request.user.is_authenticated():
        my_campaigns = get_campaign_stats(request)['my_campaigns']
        this_campaign = [campaign for campaign in my_campaigns if campaign.id == int(campaign_id)]
        if len(this_campaign) > 0:
            this_campaign = this_campaign[0]
            if this_campaign.is_active:
                this_campaign.is_active = False
            else:
                this_campaign.is_active = True
            this_campaign.save()
    return JsonResponse({'status':'success'})

def delete_campaign(request):
    campaign_id = request.POST['id']
    status = "success"
    if request.user.is_authenticated():
        my_campaigns = get_campaign_stats(request)['my_campaigns']
        this_campaign = [campaign for campaign in my_campaigns if campaign.id == int(campaign_id)]
        if len(this_campaign) > 0:
            this_campaign = this_campaign[0]
            if this_campaign.is_active:
                status = "You must stop this campaign first"
            else:
                this_campaign.delete()
    return JsonResponse({'status':status})

def copy_campaign(request):
    campaign_id = request.POST['id']
    if request.user.is_authenticated():
        my_campaigns = get_campaign_stats(request)['my_campaigns']
        this_campaign = [campaign for campaign in my_campaigns if campaign.id == int(campaign_id)]
        if len(this_campaign) > 0:
            this_campaign = this_campaign[0]
            this_campaign.pk = None
            this_campaign.is_paid = False
            this_campaign.is_active = False
            this_campaign.save()
            data = serializers.serialize('json', [this_campaign])
            return HttpResponse(data, content_type="application/json")
    return JsonResponse({'status':'error'})

def forgot_password(request):
  return render(request, 'web/forgot_password.html', {})

