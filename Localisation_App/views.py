from django.forms import ValidationError
from Localisation_Project.settings import CACHE_TTL
from .forms import TTSservice, TranslationQuoteForm
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from multiprocessing import context
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .models import *
import random
import requests
from .word_count import crawl_data
from django.contrib.auth.models import User
import uuid
from datetime import date, datetime
from .helpers import *
import json
from bson import json_util
from django.urls import resolve
from django.contrib.auth.decorators import login_required
import logging
from datetime import date
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.core import validators
logger = logging.getLogger('django')
# global str_num
# global url
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
import base64
import logging
import traceback
from django.conf import settings
from django.views.decorators.cache import cache_control
from dateutil import parser
from django.shortcuts import render

# Home Page View Starts

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON HOME PAGE WITH TOP AND FOOTER MENUS.

'''


def home(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        articleData = fetch_all_article_data()
        services_name_data_list = fetch_services_heading_data()
        newsAndEventsData = fetch_all_newsAndEvents_data()
        logger.info("Finally, Home page is getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'ArticleData': articleData,
            'NewsAndEventsData': newsAndEventsData,
            'Servicesdata': services_name_data_list
        }
        return render(request, 'Localisation_App/home.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error(
            "Exception : Error in Home page. redirecting to error page ")
        
# Home Page View Ends

# About Us Page View Starts


''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON ABOUT US PAGE WITH TOP AND FOOTER MENUS.
THIS DYNAMIC CONTENT OF ABOUT US PAGE IS BEING RENDERED FROM 'Article' MODEL.
FOR CHANGING THE CONTENT OF ABOUT US PAGE, CHANGE THE CONTENT IN 'Article' MODEL FROM BACHEND ADMIN.
'''


def aboutus(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        logger.info("About Us URL fetched and set in 'requested_url' session")
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        articleData = fetch_aboutus_data()
        logger.info("Finally, About Us page is getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'ArticleData': articleData,
        }
        return render(request, 'Localisation_App/aboutus.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error(
            "Exception : Error in About Us page. redirecting to error page ")
        # 
    

# About Us Page View Ends

# Faqs Page Views Starts


''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON FAQS PAGE WITH TOP AND FOOTER MENUS.

'''


def faqs(request, data=None):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        if data==None:
            faqs_data = fetch_faqs_data()
            logger.info("Finally, Faqs page getting displayed")
            # print("faqsdata",faqs_data)
            for d in faqs_data:
                print("q",d.FAQs_Question)
                print("a",d.FAQs_Answer)
            context = {
                'data': faqs_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'topmenus': top_menu_items_data,
                'faq_title': 'none'
            }
        
        else:
            chosen_faqs = FAQs.objects.filter(id=data)
            context={
            'data':chosen_faqs,
            'FooterMenuItemsdata':footer_menu_items_data,
            'topmenus':top_menu_items_data,
            'faq_title':'none'
            }
        return render(request,'Localisation_App/faqs.html',context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error(
            "Exception : Error in Faqs page. redirecting to error page ")
        

# Faqs Page Views Ends

# Faqs Serach Page Views Starts


''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON FAQS PAGE AFTER SEARCHED DATA WITH TOP AND FOOTER MENUS.

'''


def faqsSearch(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        if request.method == "POST":
            context = fetch_faqs_searched_data(request,url)
            context["topmenus"] = top_menu_items_data
            context["FooterMenuItemsdata"] = footer_menu_items_data
            logger.info("Finally, Faqs page getting displayed with serached title")
            return render(request, 'Localisation_App/faqs.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error(
            "Error while, faqs search page. redirecting to error page ")
        

# Faqs Serach Page Views Ends


# Terms And Conditions Page Views Starts
''' 
AUTHOR : SHWETA PATIL, SHIVAM SHARMA
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON termsandcondition PAGE WITH TOP AND FOOTER MENUS.

'''


def termsandcondition(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        footer_data = fetch_terms_and_conditions_data()
        logger.info("Finally, Terms and Condition page getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'content': footer_data

        }
        return render(request, 'Localisation_App/footer_links/termsandconditions.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error(
            "Error while,Terms and Condition page. redirecting to error page ")
        

# Terms And Conditions Page Views Ends

# Accessibility Statement Page Views Starts


''' 
AUTHOR : SHWETA PATIL, SHIVAM SHARMA
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON accessibilityStatement PAGE WITH TOP AND FOOTER MENUS.

'''


def accessibilityStatement(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        footer_data = fetch_accessibilityStatement_data()
        logger.info("Finally,accessibility_statement page getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'content': footer_data
        }
        return render(request, 'Localisation_App/footer_links/accessibility_statement.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error(
            "Error while, accessibility_statement page. redirecting to error page ")
        

# Accessibility Statement Page Views Ends


# Website Policies Page Views Start

''' 
AUTHOR : SHWETA PATIL, SHIVAM SHARMA
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON websitepolicy PAGE WITH TOP AND FOOTER MENUS.

'''


def websitepolicy(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        footer_sub_data = fetch_websitepolicy_sub_data()
        content = fetch_websitepolicy_content_data()
        logger.info("Finally, websitepolicy page getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'footer_sub_data': footer_sub_data,
            "content": content
        }
        return render(request, 'Localisation_App/footer_links/websitepolicies.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error(
            "Error while, websitepolicy page. redirecting to error page")
        

# Website Policies Page Views Ends


# Sitemap Page Views Starts

''' 
AUTHOR : SHWETA PATIL, SHIVAM SHARMA
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON sitemap PAGE WITH TOP AND FOOTER MENUS.

'''


def sitemap(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        footer_data = fetch_sitemap_data()
        print("data",footer_data)
        logger.info("Finally, sitemap page getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'content': footer_data
        }
        return render(request, 'Localisation_App/footer_links/sitemap.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error("Error while, sitemap page. redirecting to error page")
        

# Sitemap Page Views Ends


# Help Page Views Starts

''' 
AUTHOR : SHWETA PATIL, SHIVAM SHARMA
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON Help PAGE WITH TOP AND FOOTER MENUS.

'''


def help(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        footer_sub_data = fetch_help_sub_data()
        content = fetch_help_content_data()
        logger.info("Help page getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            "footer_sub_data": footer_sub_data,
            "content": content
        }
        return render(request, 'Localisation_App/footer_links/help.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error("Error while, help page")
        

# Help Page Views Ends


# goTranslate Page Views Starts

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON goTranslate PAGE WITH TOP AND FOOTER MENUS.

'''


def goTranslate(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        logger.info("Finally, goTranslate page is getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            "service": "goTranslate"

        }
        return render(request, 'Localisation_App/services_pages/gotranslate.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error(
            "Error while, goTranslate page. redirecting to error page")
        

# goTranslate Page Views Ends


# Dashboard Page View Starts

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON Dashboard PAGE WITH TOP AND FOOTER MENUS.

'''


def dashboard(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        Total_Tools_DownloadCount = calculate_totaldownloadcount_tools()
        Total_ResourceData_DownloadCount = calculate_totaldownloadcount_resources()
        successStories_CategoryData = fetch_SuccessStories_Category()
        toolsCategory_data = fetch_Tools_Category()
        resourcesCategory_data = fetch_Resources_Category()

        tools_data = fetch_all_tools_data()
        resources_data = fetch_all_resources_data()

        SuccessStoriescategory_name = fetch_SuccessStoriescategory_name_dashboard(
            successStories_CategoryData)
        countOfStoriesWithCategory = fetch_countOfStoriesWithCategory_dashboard(
            successStories_CategoryData)

        toolscategory_name = fetch_toolscategory_name_dashboard(
            toolsCategory_data)
        countOfToolsWithCategory = fetch_countOfToolsWithCategory_dashboard(
            toolsCategory_data)

        resourcescategory_name = fetch_resourcescategory_name_dashboard(
            resourcesCategory_data)
        countOfResourcesWithCategory = fetch_countOfResourcesWithCategory_dashboard(
            resourcesCategory_data)

        tools_id = []
        for tools in tools_data:
            tools_id.append(tools.id)
        toolsName_hitCount_Per_Name = fetch_toolsName_hitCount_Per_Name(
            tools_id)
        toolsName = fetch_toolsName_dashboard(tools_id)

        id_resources = []
        for resource in resources_data:
            id_resources.append(resource.id)
        resourcesName_hitCount_Per_Name = fetch_resourcesName_hitCount_Per_Name(
            id_resources)
        resourcesName = fetch_resourcesName_dashboard(id_resources)

        logger.info("Finally, Dashboard page is getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'name': 'Success Strories Dataset',
            'successStories_CategoryData': SuccessStoriescategory_name,
            'count_Of_Stories_PerCategory': countOfStoriesWithCategory,

            'tools_CategoryData': toolscategory_name,
            'count_Of_Tools_PerCategory': countOfToolsWithCategory,

            'resources_CategoryData': resourcescategory_name,
            'count_Of_Resources_PerCategory': countOfResourcesWithCategory,

            'toolshit_name': toolsName,
            'toolsHitCount': toolsName_hitCount_Per_Name,

            'resourcesshit_name': resourcesName,
            'resourcesHitCount': resourcesName_hitCount_Per_Name,
            'Total_Tools_DownloadCount': Total_Tools_DownloadCount,
            'Total_ResourceData_DownloadCount': Total_ResourceData_DownloadCount
        }
    
        return render(request, 'Localisation_App/Dashboard.html', context)
    except:
        logger.error("Error while, Dashboard page. redirecting to error page")
        

# Dashboard Page View Ends


# Tools Page View Starts

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON Tools PAGE WITH TOP AND FOOTER MENUS.

'''


def toolsPage(request, id=None):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
       
        if id==None:
            tools_Data = fetch_all_tools_data()
            Tools_Category.objects.all().update(Tools_Cat_Status=False)
            toolsCategory_data = fetch_Tools_Category()
            count = ToolsData.objects.all().count()
            page = Paginator(tools_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = tools_Data.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'toolsdata': tools_Data,
                'tools_title': 'none',
                'toolscategory': toolsCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count,
            }
            logger.info("Finally,Tools page getting displayed")
        else:
            tools_Data = ToolsData.objects.filter(id=id)
            Tools_Category.objects.all().update(Tools_Cat_Status=False)
            toolsCategory_data = fetch_Tools_Category()
            count = ToolsData.objects.all().count()
            page = Paginator(tools_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = tools_Data.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'toolsdata': tools_Data,
                'tools_title': 'none',
                'toolscategory': toolsCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count,
            }
        return render(request, 'Localisation_App/tools.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        

# Tools Page View Ends


# Tools Reset Page View Starts

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON Tools PAGE AFTER DOWNLOAD TOOLS WITH TOP AND FOOTER MENUS.

'''


def toolsReset(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        tools_Data = ToolsData.objects.all()
        cache.set("All_tools_data", tools_Data)
        Tools_Category.objects.all().update(Tools_Cat_Status=False)
        toolsCategory_data = Tools_Category.objects.all()
        cache.set("All_tools_Category", toolsCategory_data)
        count = ToolsData.objects.all().count()
        page = Paginator(tools_Data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = tools_Data.count()
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'toolsdata': tools_Data,
            'tools_title': 'none',
            'toolscategory': toolsCategory_data,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count,

        }
        logger.info("Tools page getting displayed")
        # if request.user.is_authenticated:
        #     return render(request, 'Localisation_App/tools.html', context)
        # else:
        return render(request, 'Localisation_App/tools.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        

# Tools Reset Page View Ends


# Tools Search Page View Starts

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON Tools PAGE AFTER SEARCH TOOLS WITH TOP AND FOOTER MENUS.

'''


def toolsSearch(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        toolsCategory_data = fetch_Tools_Category()
        if request.method == "POST":
            tools_title = request.POST.get("toolname")
            request.session["toolname"]=tools_title
            print("title seesion saved")
            context = fetch_tools_searched_data(request, url)
            context["topmenus"] = top_menu_items_data
            context["FooterMenuItemsdata"] = footer_menu_items_data
            context["toolscategory"] = toolsCategory_data
            return render(request, 'Localisation_App/tools.html', context)
        tools_title_Session=request.session.get("toolname")
        print("Title name with session",tools_title_Session)
        context = fetch_tools_searched_data_pagination(request, tools_title_Session, url)
        context["topmenus"] = top_menu_items_data
        context["FooterMenuItemsdata"] = footer_menu_items_data
        context["toolscategory"] = toolsCategory_data
        return render(request, 'Localisation_App/tools.html', context)
    except:
        logger.error(
            "Error while, toolspage page with search. redirecting to error page")    


    # except Exception as e:
    #     logger.error('%s' % type(e))
    #     logger.error(
    #         "Error while, resourcespage page with search. redirecting to error page")
        


# Tools Search Page View Ends


# Tools Filteration Page View Starts

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON Tools PAGE AFTER FILTERATION TOOLS WITH TOP AND FOOTER MENUS.

'''


def tools(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        category_name = []
        pagestatus = False
        filtered_Tools_Data = ToolsData.objects.none()
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        tools_Data = fetch_all_tools_data()
        toolsCategory_data = Tools_Category.objects.all()
        if request.method == "POST":
            context = fetch_tools_data_with_selected_category(request, url)
            context["topmenus"] = top_menu_items_data
            context["FooterMenuItemsdata"] = footer_menu_items_data
            logger.error(
                "Finally,Tools page getting displayed with selected category filteration")
            return render(request, 'Localisation_App/tools.html', context)
        try:
            for category in toolsCategory_data:
                if category.Tools_Cat_Status == True:
                    pagestatus = True
                    category_name.append(category.Tools_CategoryType)
            category_name.append("ToFetch_FilteredTools_With_Cache")
            to_fetch = tuple(category_name)
            filtered_Tools_Data = fetch_filteredToolsdata_for_pagination(
                to_fetch)
            logger.error(
                "Tools page, fetched tools data with selected category for pagination")
        except:
            logger.error(
                "Tools page, for pagination, error in fetching Tools_Data data by selected category name")
            page = Paginator(tools_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = tools_Data.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'toolsdata': tools_Data,
                'tools_title': 'none',
                'toolscategory': toolsCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }
            return render(request, 'Localisation_App/tools.html', context)
        if pagestatus == True:
            toolsCategory_data = Tools_Category.objects.all()
            logger.info(
                "Tools page getting displayed with selected category filteration and pagination")
            page = Paginator(filtered_Tools_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = filtered_Tools_Data.count()
            context = {
                'toolsdata': filtered_Tools_Data,
                "page": page,
                'status_All_Checked': None,
                'Pagination_Type': 'Category_Post',
                'count': count
            }
        else:
            logger.info(
                "Tools page getting displayed with all category filteration and pagination")
            page = Paginator(tools_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = tools_Data.count()
            context = {
                'toolsdata': tools_Data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }
        context["topmenus"] = top_menu_items_data
        context["FooterMenuItemsdata"] = footer_menu_items_data
        context["toolscategory"] = toolsCategory_data
        context["tools_title"] = 'none'
        return render(request, 'Localisation_App/tools.html', context)
    except:
        logger.error(
            "Error while, tools page with filteration. redirecting to error page")
        

# Tools Filteration Page View Ends


# Tools DownloadCount Page View Starts

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS INCREASING DOWMLOAD COUNT OF TOOLS WITH TOP AND FOOTER MENUS.

'''


def toolsDownloadCounter(request, id):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = ''
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        saved_ip = None
        time_posted = request.session.get('tools_Download_time')
        tools_obj = ToolsData.objects.get(pk=id)
        tools_requested_title = tools_obj.ToolsData_HeadingName
        Heading = request.session.get('toolsDownloadCounter_toolHeading')
        savedTimeInSession = None
        time_diff = 0
        logger.info("Inside Tools page, toolsDownloadCounter function checking where saved heading name and requested tools heading name is different or not")
        if tools_requested_title == Heading:
            logger.info(
                "Inside Tools page, toolsDownloadCounter function, saved heading name and requested tools heading name is same")
            if time_posted is not None:
                logger.info(
                    "Tools page, time_posted is saved in tools_Download_time is not none ")
                savedTimeInSession = datetime.fromisoformat(time_posted[:-1])
                dataCurrentTime = datetime.now()
                timediff = dataCurrentTime - savedTimeInSession
                time_diff = timediff.total_seconds()
                logger.info(
                    "Tools page, calculating time difference from saved time with first button click to current button click time")
            else:
                logger.info(
                    "Tools page, time_posted is saved in tools_Download_time is none ")
                logger.info("time_posted none")
        else:
            logger.info(
                "Tools page, checking where saved heading name and requested name is different")
            time_diff = 500

        if time_diff < 300:
            logger.info(
                "Tools page,if time diff. is less than 300 seconds, then it will save requested ip to toolsDownloadCounter_ip for creating session with ip")
            saved_ip = request.session.get('toolsDownloadCounter_ip')
        else:
            logger.info(
                "Tools page,if time diff. is more than 300 seconds, then it will set none to toolsDownloadCounter_ip session for not creating session with ip")
            request.session['toolsDownloadCounter_ip'] = None

        if ip != saved_ip:
            logger.info("Tools page,it will check that within 300 second request is not comming from same ip, it will increase download count, and set toolsDownloadCounter_ip as requested ip and requested time to tools_Download_time ")
            # logger.info("savedTimeInSession inside second not none")
            logger.info("ip is defferent inside second not none")
            # if time_diff < 10:
            logger.info("time is less than 10 seconds inside second not none")
            request.session['toolsDownloadCounter_ip'] = ip
            data = datetime.now()
            data1 = json.dumps(data, default=json_util.default)
            aList = json.loads(data1)
            testdata = aList['$date']
            request.session['tools_Download_time'] = testdata
            logger.info("increase download count second")
            tool_obj = ToolsData.objects.get(pk=id)
            tool_obj.ToolsData_DownloadCounter = tool_obj.ToolsData_DownloadCounter + 1
            tool_obj.save()
            datatotest = ToolsData.objects.get(pk=id)
            request.session['toolsDownloadCounter_toolHeading'] = tool_obj.ToolsData_HeadingName
            logger.info(
                "Finally, redirecting to toolReset view after increasing download count")
            return redirect('Localisation_App:toolsReset')
        else:
            logger.info("Tools page,if within 300 second request is comming from same ip, it will not increase download count, and set toolsDownloadCounter_ip as requested ip and requested time to tools_Download_time ")
            logger.info("ip is same inside second none")
            # request.session['toolsDownloadCounter_ip'] = ip
            tool_obj = ToolsData.objects.get(pk=id)
            # request.session['toolsDownloadCounter_toolHeading'] = tool_obj.ToolsData_HeadingName
            data = datetime.now()
            data1 = json.dumps(data, default=json_util.default)
            aList = json.loads(data1)
            testdata = aList['$date']
            # request.session['tools_Download_time'] = testdata
            logger.info(
                "Finally, redirecting to toolReset view without increasing download count")
            return redirect('Localisation_App:toolsReset')
    except Exception as e:
        logger.error('%s' % type(e))
        

# Tools DownloadCount Page View Ends


# Resources Page View Starts

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON Resources PAGE WITH TOP AND FOOTER MENUS.

'''


def resourcesPage(request, id=None):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        Resources_Category.objects.all().update(Resources_Cat_Status=False)
        resourcesCategory_data = fetch_Resources_Category()
        if id == None:
            resources_Data = fetch_all_resources_data()
            count = ResourceData.objects.all().count()
            page = Paginator(resources_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = resources_Data.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'resoucesdata': resources_Data,
                'resource_title': 'none',
                'resourcescategory': resourcesCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }
            logger.info("Finally, Resources page getting displayed")
        else:
            resources_Data = ResourceData.objects.filter(id=id)
            count = ResourceData.objects.all().count()
            page = Paginator(resources_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = resources_Data.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'resoucesdata': resources_Data,
                'resource_title': 'none',
                'resourcescategory': resourcesCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }
        return render(request, 'Localisation_App/resources.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        

# Resources Page View Ends


# Resources Filteration Page View Starts

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON Resources PAGE AFTER AFTER FILTERATION RESOURCE WITH TOP AND FOOTER MENUS.

'''


def resources(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        category_name = []
        pagestatus = False
        filtered_resources_data = ResourceData.objects.none()
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        resoucesCategory_data = Resources_Category.objects.all()
        resources_Data = fetch_all_resources_data()
        count = ResourceData.objects.all().count()
        if request.method == "POST":
            context = fetch_resources_data_with_selected_category(request, url)
            context["topmenus"] = top_menu_items_data
            context["FooterMenuItemsdata"] = footer_menu_items_data
            logger.error(
                "Finally,Resources page getting displayed with selected category filteration")
            return render(request, 'Localisation_App/resources.html', context)
        try:
            for p in resoucesCategory_data:
                if p.Resources_Cat_Status == True:
                    logger.info("true")
                    pagestatus = True
                    category_name.append(p.Resources_CategoryType)
            category_name.append("ToFetch_FilteredResources_With_Cache")
            to_fetch = tuple(category_name)
            filtered_resources_data = fetch_resources_fultereddata_for_pagination(
                to_fetch)
        except:
            logger.error(
                "resources function, error in getting data with pagination request")
            page = Paginator(resources_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = resources_Data.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'resoucesdata': resources_Data,
                'resource_title': 'none',
                'resourcescategory': resoucesCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }
        if pagestatus == True:
            logger.info(
                "Resources page getting displayed with selected category filteration and pagination")
            page = Paginator(filtered_resources_data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = filtered_resources_data.count()
            context = {
                'resoucesdata': filtered_resources_data,
                "page": page,
                'status_All_Checked': None,
                'Pagination_Type': 'Category_Post',
                'count': count
            }
            context["topmenus"] = top_menu_items_data
            context["FooterMenuItemsdata"] = footer_menu_items_data
            context["resourcescategory"] = resoucesCategory_data
            context["resource_title"] = 'none'
            return render(request, 'Localisation_App/resources.html', context)
        else:
            logger.info(
                "Resources page getting displayed with all category filteration and pagination")
            page = Paginator(resources_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = resources_Data.count()
            context = {
                'resoucesdata': resources_Data,
                'resource_title': 'none',
                "page": page,
                'Pagination_Type': 'All_Data',
                'count': count
            }
            context["topmenus"] = top_menu_items_data
            context["FooterMenuItemsdata"] = footer_menu_items_data
            context["resourcescategory"] = resoucesCategory_data
            context["resource_title"] = 'none'
            return render(request, 'Localisation_App/resources.html', context)

    except Exception as e:
        logger.error('%s' % type(e))
        

# Resources Filteration Page View Ends


# Resources Search Page View Starts

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON Resources PAGE AFTER SEARCH RESOURCE WITH TOP AND FOOTER MENUS.

'''


def resourceSearch(request):
    # try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        resourcesCategory_data = fetch_Resources_Category()
        if request.method == "POST":
            print("url", url)
            resource_title= request.POST.get("resourcename")
            request.session["resourcename"]=resource_title
            context = fetch_resources_searched_data(request, url)
            context["topmenus"] = top_menu_items_data
            context["FooterMenuItemsdata"] = footer_menu_items_data
            context["resourcescategory"] = resourcesCategory_data
            return render(request, 'Localisation_App/resources.html', context)
        resource_title=request.session.get("resourcename")
        context = fetch_resources_serached_data_pagination(request, url, resource_title)
        context["topmenus"] = top_menu_items_data
        context["FooterMenuItemsdata"] = footer_menu_items_data
        context["resourcescategory"] = resourcesCategory_data
        return render(request, 'Localisation_App/resources.html', context)
    # except Exception as e:
    #     logger.error('%s' % type(e))
    #     logger.error(
    #         "Error while, resourcespage page with search. redirecting to error page")
        

# Resources Search Page View Ends


# Resources Reset Page View Starts

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS RENDERING CONTENT ON Resources PAGE AFTER DOWNLOAD RESOURCE WITH TOP AND FOOTER MENUS.

'''


def resourcesReset(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        resources_Data = ResourceData.objects.all()
        cache.set("All_resources_data", resources_Data)
        Resources_Category.objects.all().update(Resources_Cat_Status=False)
        resourcesCategory_data = Resources_Category.objects.all()
        cache.set("All_Resources_Category", resourcesCategory_data)
        count = ResourceData.objects.all().count()
        page = Paginator(resources_Data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = resources_Data.count()
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'resoucesdata': resources_Data,
            'resource_title': 'none',
            'resourcescategory': resourcesCategory_data,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count
        }
        logger.info("Resources page getting displayed")
        return render(request, 'Localisation_App/resources.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        

# Resources Reset Page View Ends


# Resources DownloadCount Page View Starts

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION IS INCREASING DOWMLOAD COUNT OF RESOURCES WITH TOP AND FOOTER MENUS.

'''


def resourceDownloadCounter(request, id):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = ''
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        saved_ip = None
        time_posted = request.session.get('resources_Download_time')
        print("time_posted",time_posted)
        resources_obj = ResourceData.objects.get(pk=id)
        resource_requested_title = resources_obj.ResourceData_HeadingName
        Heading = request.session.get(
            'resourcesDownloadCounter_resourceHeading')
        savedTimeInSession = None
        time_diff = 0
        logger.info("Inside Resources page, resourceDownloadCounter function checking where saved heading name and requested resources heading name is different or not")
        if resource_requested_title == Heading:
            logger.info(
                "Inside Resources page, resourceDownloadCounter function, saved heading name and requested Resources heading name is same")
            if time_posted is not None:
                logger.info(
                    "Resources page, time_posted is saved in resources_Download_time is not none ")
                logger.info("time_posted not none")
                savedTimeInSession = datetime.fromisoformat(time_posted[:-1])
                dataCurrentTime = datetime.now()
                timediff = dataCurrentTime - savedTimeInSession
                time_diff = timediff.total_seconds()
                logger.info(
                    "Resources page, calculating time difference from saved time with first button click to current button click time ")
            else:
                logger.info(
                    "Resources page, time data is saved in resources_Download_time is none ")
                logger.info("time_posted none")
        else:
            logger.info(
                "Resources page,saved heading name and requested name is different")
            time_diff = 500
        if time_diff < 300:
            logger.info(
                "Resources page,if time diff. is less than 300 seconds, then it will save requested ip to resourcesDownloadCounter_ip for creating session ")
            saved_ip = request.session.get('resourcesDownloadCounter_ip')
        else:
            logger.info(
                "Resources page,if time diff. is more than 300 seconds, then it will set none to resourcesDownloadCounter_ip for not creating session ")
            request.session['resourcesDownloadCounter_ip'] = None

        if ip != saved_ip:
            logger.info("Resources page,within 300 second request is not comming from same ip , it will increase download count, and set resourcesDownloadCounter_ip as requested ip and requested time to resources_Download_time ")
            # logger.info("savedTimeInSession inside second not none")
            # if ip != saved_ip:
            logger.info("ip is defferent inside second not none")
            # if time_diff < 10:
            logger.info("time is less than 10 seconds inside second not none")
            request.session['resourcesDownloadCounter_ip'] = ip
            data = datetime.now()
            data1 = json.dumps(data, default=json_util.default)
            aList = json.loads(data1)
            testdata = aList['$date']
            request.session['resources_Download_time'] = testdata
            logger.info("increase download count second")
            resources_obj = ResourceData.objects.get(pk=id)
            resources_obj.ResourceData_DownloadCounter = resources_obj.ResourceData_DownloadCounter + 1
            resources_obj.save()
            request.session['resourcesDownloadCounter_resourceHeading'] = resources_obj.ResourceData_HeadingName
            logger.info(
                "Finally, redirecting to resourcesReset view after increasing download count")
            return redirect('Localisation_App:resourcesReset')
        else:
            logger.info("Resources page,if within 300 second request is comming from same ip, it will not increase download count, and set resourcesDownloadCounter_ip as requested ip and requested time to resources_Download_time ")
            logger.info("ip is same inside second none")
            # request.session['resourcesDownloadCounter_ip'] = ip
            resources_obj = ResourceData.objects.get(pk=id)
            # request.session['resourcesDownloadCounter_resourceHeading'] = resources_obj.ResourceData_HeadingName
            logger.info("same and none ip first")
            data = datetime.now()
            data1 = json.dumps(data, default=json_util.default)
            aList = json.loads(data1)
            testdata = aList['$date']
            # request.session['resources_Download_time'] = testdata
            logger.info(
                "Finally, redirecting to resourcesReset view without increasing download count")
            return redirect('Localisation_App:resourcesReset')
    except Exception as e:
        logger.error('%s' % type(e))
        

# Resources DownloadCount Page View Ends


# Success Stories Page View Starts
 
''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION SUCCESS STORIES DATA WITH TOP AND FOOTER MENUS.

'''

def successstoryPage(request,id=None):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        SuccessStories_Category.objects.update(SuccessStories_Cat_Status=False)
        successStories_CategoryData=fetch_All_SuccessStories_Category_data()
        
        if id==None:
            successStoriesData=fetch_All_SuccessStories_data()
            page = Paginator(successStoriesData, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = successStoriesData.count()
            logger.info("Finally, Success Stories page is getting displayed")
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'SuccessStoriesData': successStoriesData,
                'SuccessStories_CategoryData': successStories_CategoryData,
                'story_title': 'none',
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }
            
        else:
            SuccessStoriesData=SuccessStories.objects.filter(id=id)
            page=Paginator(SuccessStoriesData, 7)
            page_list=request.GET.get('page')
            # page=page.get_page(page_list)
            count=SuccessStoriesData.count()
            print("success story data ",successStories_CategoryData)
            print("filtered success story ",SuccessStoriesData[0])
            context={
                    'topmenus':top_menu_items_data,
                    'FooterMenuItemsdata':footer_menu_items_data,
                    'SuccessStoriesData':SuccessStoriesData,
                    'SuccessStories_CategoryData': successStories_CategoryData,
                    'story_title':SuccessStoriesData[0],
                    "page":page,
                    'satus_All_Checked':'True',
                    'Pagination_Type':'All_Data',
                    'count':count
            }     
        return render(request, 'Localisation_App/successstory.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        

# Success Stories Page View Ends


# Success Stories Page With Category View Starts
 
''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION SUCCESS STORIES DATA WITH FILTERED CATEGORY TOP AND FOOTER MENUS.

'''

def successstory(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        checklist1 = []
        category_name = []
        pagestatus = False
        filtered_SuccessStories_Data = SuccessStories.objects.none()
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        if cache.get("All_successStories_data_data"):
            successStoriesData = cache.get("All_successStories_data_data")
            logger.info("cache data")
        else:
            successStoriesData = SuccessStories.objects.all().order_by('SuccessStories_Priority')
            cache.set("All_successStories_data_data", successStoriesData)
            logger.info("database data")
        # SuccessStrories_Category.objects.update(SuccessStrories_Cat_Status=False)
        successStories_CategoryData = SuccessStories_Category.objects.order_by(
            'SuccessStories_Cat_Priority')
        if request.method == "POST":
            # logger.info("allcheched",request.POST.get('all_checkbox'))
            if request.POST.get('all_checkbox') != 'all_Checked':
                category_name = []
                filtered_SuccessStories_Data = SuccessStories.objects.none()
                # logger.info("dumydata",q)
                checklist = request.POST.getlist('checkbox')
                # logger.info(checklist)
                SuccessStories_Category.objects.all().update(SuccessStories_Cat_Status=False)

                for n in checklist:
                    SuccessStories_Category.objects.filter(
                        pk=int(n)).update(SuccessStories_Cat_Status=True)
                checklist.append(30303030330303030303)
                if cache.get(checklist):
                    successStoriesData_Checked = cache.get(checklist)
                    logger.info("cache data")
                else:
                    successStoriesData_Checked = SuccessStories_Category.objects.filter(
                        id__in=checklist)
                    cache.set(checklist, successStoriesData_Checked)
                    logger.info("database data")

                for n in successStoriesData_Checked:
                    # logger.info('hello',n.SuccessStrories_CategoryType)
                    category_name.append(n.SuccessStories_CategoryType)
                # logger.info("list",category_name)
                # logger.info("tuple",tuple(category_name))
                category_name.append("ToFetch_FilteredStories_With_Cache")
                to_fetch = tuple(category_name)
                if cache.get(to_fetch):
                    filtered_SuccessStories_Data = cache.get(to_fetch)
                    logger.info("cache data")
                else:
                    for cat_name in to_fetch:
                        filtered_SuccessStories_Data = filtered_SuccessStories_Data | SuccessStories.objects.filter(
                            SuccessStories_category__SuccessStories_CategoryType__contains=cat_name).order_by('SuccessStories_category__SuccessStories_Cat_Priority', 'SuccessStories_Priority')
                # logger.info("all data",q)
                    cache.set(to_fetch, filtered_SuccessStories_Data)
                    logger.info("database data")

                count = filtered_SuccessStories_Data.count()
                logger.info("hey", filtered_SuccessStories_Data)
                page = Paginator(filtered_SuccessStories_Data, 8)
                page_list = request.GET.get('page')
                # logger.info("pagenumber",page_list)
                page = page.get_page(page_list)
                count = filtered_SuccessStories_Data.count()
                logger.info(
                    "Success stories page getting displayed with selected category filteration")
                context = {
                    'topmenus': top_menu_items_data,
                    'FooterMenuItemsdata': footer_menu_items_data,
                    'SuccessStoriesData': filtered_SuccessStories_Data,
                    'SuccessStories_CategoryData': successStories_CategoryData,
                    "page": page,
                    'story_title': 'none',
                    'Pagination_Type': 'Category_Post',
                    'status_All_Checked': None,
                    'count': count
                }
                logger.info("inside 1")
                # return render(request,'Localisation_App/successstory.html',context)

            else:
                logger.info(
                    "Success stories page getting displayed with all category filteration")
                page = Paginator(successStoriesData, 8)
                SuccessStories_Category.objects.all().update(SuccessStories_Cat_Status=False)
                page_list = request.GET.get('page')
                page = page.get_page(page_list)
                count = successStoriesData.count()
                context = {
                    'topmenus': top_menu_items_data,
                    'FooterMenuItemsdata': footer_menu_items_data,
                    'SuccessStoriesData': successStoriesData,
                    'SuccessStories_CategoryData': successStories_CategoryData,
                    "page": page,
                    'story_title': 'none',
                    'status_All_Checked': 'True',
                    'Pagination_Type': 'All_Data',
                    'count': count
                }
                logger.info("inside 2")

        for p in successStories_CategoryData:
            if p.SuccessStories_Cat_Status == True:
                logger.info("true")
                pagestatus = True
                category_name.append(p.SuccessStories_CategoryType)
        category_name.append("ToFetch_FilteredStories_With_Cache")
        to_fetch = tuple(category_name)
        if cache.get(to_fetch):
            filtered_SuccessStories_Data = cache.get(to_fetch)
            logger.info("cache data")
        else:
            for cat_name in to_fetch:
                filtered_SuccessStories_Data = filtered_SuccessStories_Data | SuccessStories.objects.filter(
                    SuccessStories_category__SuccessStories_CategoryType__contains=cat_name).order_by('SuccessStories_category__SuccessStories_Cat_Priority', 'SuccessStories_Priority')

            cache.set(to_fetch, filtered_SuccessStories_Data)
            logger.info("database data")

        if pagestatus == True:
            logger.info(
                "Success stories page getting displayed with selected category filteration and pagination")
            page = Paginator(filtered_SuccessStories_Data, 8)
            # SuccessStrories_Category.objects.all().update(SuccessStrories_Cat_Status=False)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = filtered_SuccessStories_Data.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'SuccessStoriesData': filtered_SuccessStories_Data,
                'story_title': 'none',
                'SuccessStories_CategoryData': successStories_CategoryData,
                "page": page,
                'Pagination_Type': 'Category_Post',
                'status_All_Checked': None,
                'count': count
            }

        else:
            logger.info(
                "Success stories page getting displayed with all category filteration and pagination")
            page = Paginator(successStoriesData, 8)
            # SuccessStrories_Category.objects.all().update(SuccessStrories_Cat_Status=False)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = successStoriesData.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'SuccessStoriesData': successStoriesData,
                'story_title': 'none',
                'SuccessStories_CategoryData': successStories_CategoryData,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }

        logger.info("outside")
        return render(request, 'Localisation_App/successstory.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        

# Success Stories Page With Category View Ends


# Success Stories Search Page View Starts
 
''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION SUCCESS STORIES DATA WITH SEARCHED TITLE  WITH TOP AND FOOTER MENUS.

'''
def successstorySearch(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        successStories_CategoryData = SuccessStories_Category.objects.order_by('SuccessStories_Cat_Priority')
        if request.method == "POST":
            story_title = request.POST.get("storyname")
            request.session["storyname"]=story_title
            context=fetch_successstories_searched_data(request,url)
            context["topmenus"]=top_menu_items_data
            context["FooterMenuItemsdata"]=footer_menu_items_data
            context["SuccessStories_CategoryData"]=successStories_CategoryData   
            return render(request, 'Localisation_App/successstory.html', context)
        story_title=request.session.get("storyname")
        context=fetch_success_stories_data_with_pagination(request,url,story_title)
        context["topmenus"]=top_menu_items_data
        context["FooterMenuItemsdata"]=footer_menu_items_data
        context["SuccessStories_CategoryData"]=successStories_CategoryData 
        return render(request, 'Localisation_App/successstory.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        

# Success Stories Search Page View Ends


# Services Page View Start
''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION FETCHING ALL SERVICES DATA WITH TOP AND FOOTER MENUS.

'''


def services(request):
    try:
        print("services")
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        tTS_Form = TTSservice()
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        servicesdata = fetch_all_services_data()
        print("servicesdatra",servicesdata)
        logger.info("Finally, Services page getting displayed with all data")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'Servicesdata': servicesdata,
            'TTS_Form': tTS_Form,
        }
        return render(request, 'Localisation_App/services.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error("Error while, Displaying Services page with all data")
        

# Services Page View Ends


# EnableTyping Page View Start

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION FETCHING EnableTyping PAGE WITH TOP AND FOOTER MENUS.

'''


def srvEnableTyping(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = TopMenuItems.objects.all()
        FooterMenuItemsdata = FooterMenuItems.objects.all()
        if request.method == "POST":
            nameodservice = request.POST.get("nameodservice")
            logger.info("nameeee", nameodservice)
        return render(request, 'Localisation_App/ServicesDemoPage.html')
    except Exception as e:
        logger.error('%s' % type(e))
        

# EnableTyping Page View Ends


# GoTranslateWebLocalizer Page View Start

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION FETCHING GoTranslateWebLocalizer PAGE WITH TOP AND FOOTER MENUS.

'''


def srvGoTranslateWebLocalizer(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        logger.info(
            "Go Translate WebLocalizer page getting displayed with all data")
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            "service": "goTranslate"
        }
        logger.info("srvGoTranslateWebLocalizer page displayed with all data")
        return render(request, 'Localisation_App/services_pages/gotranslate.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error(
            "Error while, Displaying srvGoTranslateWebLocalizer page with all data")
        

# GoTranslateWebLocalizer Page View Ends


# OnscreenKeyboard Page View Start

def srvOnscreenKeyboard(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        if request.method == "POST":
            context = {
                "service": "onscreenkeyboard",
                "data": "onscreenkeyboard",
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
            }
            return render(request, 'Localisation_App/ServicesDemoPage.html', context)
        logger.info("On screen Keyboard page getting displayed with all data")
        context = {
            "service": "onscreenkeyboard",
            "data": "onscreenkeyboard",
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,

        }
        return render(request, 'Localisation_App/ServicesDemoPage.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error(
            "Error while, Displaying srvOnscreenKeyboard page with all data")
        

# OnscreenKeyboard Page View Ends


def srvTTS(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        tTS_Form = TTSservice()
        if request.method == "POST":
            Details = TTSservice(request.POST)
            logger.info("InsidePostMethod")
            if Details.is_valid():
                logger.info('form is valid')
                language = request.POST.get("Select_Language_Pair")
                gender = request.POST.get("Gender")
                inputText = request.POST.get("InputText")
                url = 'http://10.208.39.190:8001/ulca-tts'
                print("lang",language)
                payload = {'source': inputText,
                           'gender': gender, 'modelId': language}
                logger.info("TTS APi getting called with form data")
                r = requests.post(url, data=payload)
                print("response",r)
                if r.status_code == 200:
                    logger.info(
                        "TTS ,Recieved success response, after APi called with form data")
                    data = r.json()
                    print("data",data)
                    context = {
                        'Status': data['status'],
                        'outspeech_filepath': data['outspeech_filepath'][0],
                        "service": "srvTTS",
                        "TTS_Form": tTS_Form,
                        "data": "srvTTS",
                        'topmenus': top_menu_items_data,
                        'FooterMenuItemsdata': footer_menu_items_data,
                    }
                    logger.info(
                        "TTS Page getting displayed with recieved success response, after APi called with form data")
                    logger.info("returned")
                    return render(request, 'Localisation_App/services_pages/ttsService.html', context)
        logger.info("TTS page getting displayed with all data")
        context = {
            "service": "srvTTS",
            "TTS_Form": tTS_Form,
            "data": "srvTTS",
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            "DIVTITLE": "HELLO"
        }
        return render(request, 'Localisation_App/services_pages/ttsService.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error("Error while, Displaying TTS page with all data")
        


# Transliteration Page View Start

def srvTransliteration(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        if request.method == "POST":
            context = {
                "service": "srvTransliteration",
                "data": "srvTransliteration",
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
            }
            return render(request, 'Localisation_App/ServicesDemoPage.html', context)
        logger.info("Transliteration page getting displayed")
        context = {
            "service": "srvTransliteration",
            "data": "srvTransliteration",
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,

        }
        return render(request, 'Localisation_App/services_pages/transliteration_modal.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error(
            "Error while, Displaying Transliteration page with all data")
        

# Transliteration Page View Ends


# Websitepolicies Page View Start

def websitepolicydata(request, id):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        logger.info("id : ", id)
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        footer_sub_data = fetch_all_Websitepolicies_sub_data()
        content = Footer_Links_Info.objects.get(pk=id)
        logger.info(
            "websitepolicy page getting displayed with selected subtitle")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'footer_sub_data': footer_sub_data,
            "content": content
        }
        return render(request, 'Localisation_App/footer_links/websitepolicies.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error("Error while, websitepolicy page with selected subtitle")
        


# Websitepolicies Page View Ends


# Help Page View Start

def helpData(request, id):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        logger.info("id : ", id)
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        footer_sub_data = fetch_help_sub_data_with_id()
        logger.info("Help ", footer_sub_data)
        content = Footer_Links_Info.objects.get(pk=id)
        logger.info("Help page getting displayed with selected subtitle")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            "footer_sub_data": footer_sub_data,
            "content": content
        }
        return render(request, 'Localisation_App/footer_links/help.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error("Error while, help page with selected subtitle")
        

# Help Page View Ends


# Contact Us Page View Starts

''' 
AUTHOR : TANVI PATIL
DATE : 24-07-2022
BELOW FUNCTION FETCHING Contact us PAGE WITH CAPTCHA CODE AND TOP AND FOOTER MENUS.

'''


def contactus(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        logger.info("Contact us page getting displayed")
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        # footer_sub_data = Footer_Links_Info.objects.all().filter(
        #     Footer_Links_Info_MainTitle__Footer_Links_Title__contains="help")
        num = random.randrange(1121, 9899)
        logger.info("random num generated for captcha in contact us page")
        str_num = str(num)
        context = {
            'FooterMenuItemsdata': footer_menu_items_data,
            # 'footer_sub_data': footer_sub_data,
            'topmenus': top_menu_items_data,
            'img': str_num
        }
        return render(request, 'Localisation_App/contactus.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error(
            "Error while, random num generated for captcha in contact us page")
        

# Contact Us Page View Ends


# Contact Us Submit Form Page View Starts

''' 
AUTHOR : TANVI PATIL
DATE : 24-07-2022
BELOW FUNCTION SUBMITING CONTACTFORM DATA TOP AND FOOTER MENUS.

'''


def submit(request, img):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if request.method == "POST":
            name = request.POST.get("name")
            captcha = request.POST.get("captcha")
            email = request.POST.get("email")
            contactNumber = request.POST.get("phone-number")
            option = request.POST.get("option")
            comment = request.POST.get("comment")
            logger.info(name, email, contactNumber, option, comment)
            ins = Contact(name=name, email=email, phone=contactNumber,
                          option=option, comment=comment)
            ins.save()
            if img == captcha:
                try:
                    res = send_mail(option, option+" Recieved",
                                    "tanvip@cdac.in", [email, 'sshivam@cdac.in'])
                    logger.info("Email sent to "+ email)
                    
                except:
                    logger.error("Email not sent to "+ email)
                    pass
                
                
                messages.add_message(request, messages.SUCCESS,
                                     'feedback submitted successfully')
                # logger.info(messages) 
                return redirect('Localisation_App:contactus')
        #    return HttpResponse("form submitted successfully")
            else:
                messages.add_message(request, messages.ERROR,
                                     'Captcha does not matched')
                return redirect('Localisation_App:contactus')
        else:
            messages.add_message(request, messages.ERROR, 'Server error')
            return redirect('Localisation_App:contactus')
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error("Error while, while submiting contact us page")
        

# Contact Us Submit Form Page View Ends


# User Register, Login, Logout, Profile, Forgot Password, Change Password Page View Starts

''' 
AUTHOR : SHWETA PATIL
DATE : 24-07-2022
BELOW FUNCTION User Register, Login, Logout, Profile, Forgot Password, Change Password DATA TOP AND FOOTER MENUS.

'''
import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
def isValid(email):
    if re.fullmatch(regex, email):
        print("Validemail")
        return "Validemail"
    else:
        print("Invalidemail")
        return "Invalidemail"


def ispasswordValid(passwd):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat = re.compile(reg)              
    mat = re.search(pat, passwd)
    print("passwordvalid",mat)
    if mat == None:
        return False
    else:
        return True
   

def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

 

# User Register, Login, Logout, Profile, Forgot Password, Change Password Page View Ends


# Translation Quote Page View Starts

''' 
AUTHOR : SHIVAM SHARMA
DATE : 24-07-2022
BELOW FUNCTION CONTENT FOR translation_quote PAGE TOP AND FOOTER MENUS.

'''


# def translation_quote(request):
#     try:
#         url = resolve(request.path_info).url_name
#         request.session['requested_url'] = url
#         top_menu_items_data = fetch_top_menu_items()
#         footer_menu_items_data = fetch_footer_menu_items()
#         context = {
#             'topmenus': top_menu_items_data,
#             'FooterMenuItemsdata': footer_menu_items_data,
#         }
#         form = TranslationQuoteForm()
#         context['form'] = form
#         if request.method == 'POST':
#             url = request.POST.get('url')
#             company_email = request.POST.get('company_email')
#             language = request.POST.get('language')
#             domain = request.POST.get('domain')
#             delivery_date = request.POST.get('delivery_date')
#             client_remark = request.POST.get('client_remark')
#             form = TranslationQuoteForm(request.POST)
#             context['form'] = form
#             validate_url = validators.URLValidator()
#             validate_email = validators.EmailValidator()
#             try:
#                 validate_url(url)
#             except ValidationError as e:
#                 context['url_error'] = e.message
#                 return render(request, "Localisation_App/translation_quote/translation_quote.html", context)
#             # try:
#             #     validate_email(company_email)
#             # except ValidationError as e:
#             #     context['email_error'] = e.message
#             #     return render(request, "Localisation_App/translation_quote/translation_quote.html", context)
            
#             emailstatus=isValid(company_email)
#             if emailstatus == 'Invalidemail':
#                 context['email_error'] = "Enter a valid email address."
#                 return render(request, "Localisation_App/translation_quote/translation_quote.html", context)
            
#             if form.is_valid():
#                 logger.info("validation success")
#                 logger.info(form.cleaned_data['url'])
#                 logger.info(form.cleaned_data['company_email'])
#                 logger.info(form.cleaned_data['language'])
#                 logger.info(form.cleaned_data['domain'])
#                 logger.info(form.cleaned_data['delivery_date'])
#                 logger.info(form.cleaned_data['client_remark'])
#                 current_user = request.user
#                 logger.info(current_user)
#                 try:
#                     date1 = form.cleaned_data['delivery_date']
#                     if date1 < date.today():
#                         raise ValidationError(
#                             "Delivery date cannot be in the past!")
#                 except ValidationError as e:
#                     context['date_error'] = e.message
#                     return render(request, "Localisation_App/translation_quote/translation_quote.html", context)
#                 try:
#                     if len(client_remark) > 5000:
#                         raise ValidationError(
#                             # "You have entered " + str(len(client_remark)) + " characters But only 5000 characters allowed"
#                             "Max. Character Limit Exceeded(maximum length 5000 characters)"
#                         )
#                 except ValidationError as e:
#                     context['remark_error'] = e.message
#                     return render(request, "Localisation_App/translation_quote/translation_quote.html", context)
#                 application_number = str('GI-' + str(date.today().year) + '-' +
#                                          current_user.username[0:2].upper() + str(random.randrange(100000000, 1000000000)))
#                 data = TranslationQuote(
#                     url=url, company_email=company_email, language=language, domain=domain, delivery_date=delivery_date, client_remark=client_remark, application_number=application_number, username=current_user)
#                 data.save()
#                 context['status'] = 'success'
#                 context['message'] = "Form submitted successfully"
#                 try:
#                     res = send_mail("Translation Quote", "Your request for translation quote with application No : " +
#                                    application_number + " submitted ssuccessfully.", "tanvip@cdac.in", [company_email])
#                     logger.info("Email sent successfully to "+ company_email)
#                 except:
#                     logger.error("Email not sent to "+ company_email)
#                     pass
                
#                 return render(request, 'Localisation_App/translation_quote/translation_quote.html', context)
#             else:
#                 context['status'] = 'error'
#                 context['message'] = "Invalid URL!"
#                 return render(request, 'Localisation_App/translation_quote/translation_quote.html', context)
#         return render(request, "Localisation_App/translation_quote/translation_quote.html", context)
#     except Exception as e:
#         logger.error('%s' % type(e))
#         logger.error("Error while, displaying translation_quote page")
        


# Translation Quote Page View Ends


# Machine_Translation Page View Starts

''' 
AUTHOR : TANVI PATIL
DATE : 24-07-2022
BELOW FUNCTION CONTENT FOR translation_quote PAGE TOP AND FOOTER MENUS.

'''


def machine_translation(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        logger.info("Machine Translation page is getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data
        }
        return render(request, 'Localisation_App/services_pages/machine_translation.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error("Error while, displaying machine_translation page")
        

# Machine_Translation Page View Ends


# Name_Matcher Page View Starts

''' 
AUTHOR : TANVI PATIL
DATE : 24-07-2022
BELOW FUNCTION CONTENT FOR name_matcher PAGE TOP AND FOOTER MENUS.

'''


def name_matcher(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
        }
        return render(request, 'Localisation_App/services_pages/name_matcher.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error("Error while, displaying name_matcher page")
        

# Name_Matcher Page View Ends


# Empanelled_Agencies Page View Starts
''' 
AUTHOR : SHIVAM SHARMA
DATE : 24-07-2022
BELOW FUNCTION CONTENT FOR empanelled_agencies data with empanelled_agencies email Data PAGE TOP AND FOOTER MENUS.

'''


def empanelled_agencies(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = fetch_top_menu_items()
        footer_menu_items_data = fetch_footer_menu_items()
        empanelled_agecies_data = fetch_All_empanelled_agecies_data()
        empanelled_agecies_data_list = []
        for i in empanelled_agecies_data:
            data = {}
            data['company_name'] = i.company_name
            data['contact_person'] = i.contact_person
            emails = []
            for i in EmpanelledAgenciesEmail.objects.filter(empanelled_agencies=i):
                emails.append(i.email)
            data['email'] = emails
            empanelled_agecies_data_list.append(data)
        logger.info(empanelled_agecies_data_list)
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'empanelled_agencies_data': empanelled_agecies_data_list,
        }
        return render(request, 'Localisation_App/footer_links/empanelled_agencies.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error("Error while, displaying empanelled_agencies page")
        

# Empanelled_Agencies Page View Ends


# Translation_Quote_User_Dashboard Page View Start

''' 
AUTHOR : SHIVAM SHARMA
DATE : 24-07-2022
BELOW FUNCTION CONTENT FOR empanelled_agencies data with empanelled_agencies email Data PAGE TOP AND FOOTER MENUS.

'''



# def translation_quote_user_dashboard(request):
#     try:
#         top_menu_items_data = fetch_top_menu_items()
#         footer_menu_items_data = fetch_footer_menu_items()
#         current_user = request.user
#         logger.info(current_user)
#         translation_quote_data = TranslationQuote.objects.filter(
#             username=current_user)
#         logger.info("Database data for All_translation_quote")
#         logger.info(translation_quote_data)
#         context = {
#             'topmenus': top_menu_items_data,
#             'FooterMenuItemsdata': footer_menu_items_data,
#             'translation_quote_data': translation_quote_data,
#         }
#         return render(request, 'Localisation_App/translation_quote/translation_quote_user_dashboard.html', context)
#     except Exception as e:
#         logger.error('%s' % type(e))
#         logger.error(
#             "Error while, displaying translation_quote_user_dashboard page")
        

# Translation_Quote_User_Dashboard Page View Ends


# Translation_Quote_User_Show Page View Starts
''' 
AUTHOR : SHIVAM SHARMA
DATE : 24-07-2022
BELOW FUNCTION CONTENT FOR Translation_Quote_User_Show DATA WITH PAGE TOP AND FOOTER MENUS.

'''


# def translation_quote_show(request, application_number):
#     try:
#         # logger.info("application number ", application_number)
#         top_menu_items_data = fetch_top_menu_items()
#         footer_menu_items_data = fetch_footer_menu_items()
#         translation_quote_data = TranslationQuote.objects.filter(
#                  application_number=application_number)[0]
#         logger.info(translation_quote_data)
#         username = translation_quote_data.username
#         context = {
#             'topmenus': top_menu_items_data,
#             'FooterMenuItemsdata': footer_menu_items_data,
#             'translation_quote_data': translation_quote_data,
#         }
#         logger.info("Email ", username.username)

#         if username.username == 'admin':
#             print("hii")
#             return render(request, 'Localisation_App/translation_quote/translation_quote_show.html', context)
#         else:
#             user_details = UserRegistration.objects.filter(
#                 userregistration_email_field=username.username)[0]

#             context['user_details'] = user_details
#             return render(request, 'Localisation_App/translation_quote/translation_quote_show.html', context)
#     except Exception as e:
#         logger.error('%s' % type(e))
#         logger.error("Error while, displaying translation_quote_show page")
        

# Translation_Quote_User_Show Page View Ends


def bhashini(request):
    try:
        top_menu_items_data = fetch_top_menu_items()

        footer_menu_items_data = fetch_footer_menu_items()

        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
        }
        return render(request, 'Localisation_App/bhashini.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error("Error while, displaying bhashini page")
        


def anuvaad(request):
    try:
        top_menu_items_data = TopMenuItems.objects.all()
        footer_menu_items_data = FooterMenuItems.objects.all()

        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
        }
        return render(request, 'Localisation_App/services_pages/anuvaad.html', context)
    except Exception as e:
        logger.error('%s' % type(e))
        logger.error("Error while, displaying anuvaad page")
        


def custom_page_not_found_view(request, exception=None):
    return render(request, "Localisation_App/errors/404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "Localisation_App/errors/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "Localisation_App/errors/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "Localisation_App/errors/400.html", {})

# def error_404(request, exception):
#     return render(request,'Localisation_App/errors/404.html')

# def error_500(request, exception=None):
#     return render(request,'Localisation_App/errors/500.html')
