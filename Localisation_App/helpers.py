from asyncio import constants
from django.core.mail import send_mail
from django.conf import settings
from threading import currentThread
from wsgiref import validate
from django.db.models import Sum
from django.forms import ValidationError
from Localisation_Project.settings import CACHE_TTL , env
from .forms import TTSservice, TranslationQuoteForm
from django.contrib import messages
from django.core.mail import send_mail, mail_admins
from django.core.paginator import Paginator
from multiprocessing import context
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .models import *
import random
import requests
from .word_count import crawl_data
from django.contrib.auth.models import User
import uuid
from datetime import date, datetime
import json
from bson import json_util
from django.urls import resolve
from django.contrib.auth.decorators import login_required
import logging
from datetime import date
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core import validators
logger = logging.getLogger('django')
global str_num
global url
CACHE_TTL = getattr(settings,'CACHE_TTL',DEFAULT_TIMEOUT)
from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings
from django.views.decorators.cache import cache_control



# def send_forget_password_email(email, token):
#     subject = 'Your forget password link'
#     message = 'Hi, click on this link for reset password '+ env('RESET_PASSWORD_LINK') + '/' + token
#     print("message", message)
#     email_form = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     try:
#         send_mail(subject, message, email_form, recipient_list)
#         print("email sent")
#         return True
#     except:
#         print("email not sent")
#         return False

'''

BELOW FUNCTION IS FETCHING TOP MENUS DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''
def fetch_top_menu_items():
    if cache.get("All_top_menu_items_data_data"):
        top_menu_items_data = cache.get("All_top_menu_items_data_data")
        logger.info("Cache data of top_menu_items_data being rendered")
    else:
        top_menu_items_data = TopMenuItems.objects.all()
        cache.set("All_top_menu_items_data_data", top_menu_items_data)
        logger.info("Database data of top_menu_items_data being rendered")
    return top_menu_items_data

'''

BELOW FUNCTION IS FETCHING FOOTER MENUS DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''
def fetch_footer_menu_items():
    if cache.get("All_footer_menu_items_data_data"):
        footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
        logger.info("Cache data of footer_menu_items_data being rendered")
    else:
        footer_menu_items_data = FooterMenuItems.objects.all()
        cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
        logger.info("Database data of footer_menu_items_data being rendered")
    return footer_menu_items_data

'''

BELOW FUNCTION IS FETCHING ABOUT_US_ARTICLE DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''
def fetch_aboutus_data():
    if cache.get("All_About_data"):
        articleData = cache.get("All_About_data")
        logger.info("Cache data of articleData being rendered")
    else:
        articleData = Article.objects.all().filter(Article_HeadingName="About Us")
        cache.set("All_About_data", articleData)
        logger.info("Database data of articleData being rendered")
    return articleData

'''

BELOW FUNCTION IS FETCHING SERVICES_HEADINGS_NAME DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE
THIS ORM QUERY Services.objects.values("Services_Name") - RENDERING DATA IN THE FORM OF QUERYSET OF LIST OF DICTIONARY
USING FOR LOOP, WE ARE CONVERTING DATA IN DICTIONARY AND APPENDED TO LIST 

'''
def fetch_services_heading_data():
    services_name_data_list=[]
    if cache.get("All_Services_data"):
        services_name_data_list = cache.get("All_Services_data")
        logger.info("Cache data of services_name_data_list being rendered")
    else:
        services_name_data = Services.objects.values("Services_Name") 
        for name in services_name_data:
            print(name["Services_Name"])
            services_name_data_list.append(name["Services_Name"])
        cache.set("All_Services_data", services_name_data_list)
        logger.info("Database data of services_name_data_list being rendered")
    return services_name_data_list

'''

BELOW FUNCTION IS FETCHING ALL ARTICLE DATA REQUIRED FOR HOME PAGE FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''
def fetch_all_article_data():
    if cache.get("All_Article_data"):
        articleData = cache.get("All_Article_data")
        logger.info("Cache data of all article data being rendered")
        print("cache")
    else:
        articleData = Article.objects.all()
        cache.set("All_Article_data", articleData)
        print("database")
        logger.info("Database data of all article data being rendered")
    return articleData

'''

BELOW FUNCTION IS FETCHING ALL NewsAndEvents DATA REQUIRED FOR HOME PAGE FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''
def fetch_all_newsAndEvents_data():
    if cache.get("All_NewsAndEvents_data"):
        newsAndEventsData = cache.get("All_NewsAndEvents_data")
        logger.info("Cache data of all news and events data being rendered")
    else:
        newsAndEventsData = NewsAndEvents.objects.all()
        cache.set("All_NewsAndEvents_data", newsAndEventsData)
        logger.info("Database data of all news and events data being rendered")
    return newsAndEventsData

'''

BELOW FUNCTION IS FETCHING ALL Faqs DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''
def fetch_faqs_data():
    if cache.get("All_Faqs_data"):
        faqs_data = cache.get("All_Faqs_data")
        logger.info("Cache data of all faqs data being rendered")
    else:
        faqs_data = FAQs.objects.all()
        cache.set("All_Faqs_data", faqs_data)
        logger.info("Database data of all faqs data being rendered")
    return faqs_data

'''

BELOW FUNCTION IS FETCHING SEARCHED Faqs DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_faqs_searched_data(request,url): 
    try:
        faq_searched_title = request.POST.get("faq_title")
        fAQs_Data = FAQs.objects.all()
        count = fAQs_Data.count()
        if faq_searched_title != '':
            print("inside")
            faq_searched_title_name = faq_searched_title.replace(" ", "-")
            faq_searched_title_name = faq_searched_title_name.replace("<", "-")
            faq_searched_title_name = faq_searched_title_name.replace("-", "-")
            faq_searched_title_name = faq_searched_title_name.replace(">", "-")
            faq_searched_title_name = faq_searched_title_name.replace("(", "-")
            faq_searched_title_name = faq_searched_title_name.replace(")", "-")
            faq_searched_title_name = faq_searched_title_name.replace("`", "-")
            faq_searched_title_name = faq_searched_title_name.replace("'", "-")
            faq_searched_title_name = faq_searched_title_name.replace("=", "-")
            faq_searched_title_name = faq_searched_title_name.replace("+", "-")
            faq_searched_title_name = faq_searched_title_name.replace("@", "-")
            faq_searched_title_name = faq_searched_title_name.replace("#", "-")
            faq_searched_title_name = faq_searched_title_name.replace("$", "-")
            faq_searched_title_name_url=url+faq_searched_title_name
            if cache.get(faq_searched_title_name_url):
                fAQs_Data = cache.get(faq_searched_title_name_url)
                logger.info("Cache data of searched faqs data being rendered")
            else:
                fAQs_Data = FAQs.objects.filter(FAQs_Question__icontains=faq_searched_title_name)
                cache.set(faq_searched_title_name_url, fAQs_Data)
                logger.info("Database data of searched faqs data being rendered")
            print("data",fAQs_Data)
            logger.info("Finally, Faqs page getting displayed with serached title")
            context = {
                'data': fAQs_Data,
                'faq_title': faq_searched_title_name,
                'count': count
            }
        else:
            print("outside")
            logger.info("Faqs page getting displayed with all faqs data")
            logger.info("Finally, Faqs page getting displayed without serached title")
            context = {
                'data': fAQs_Data,
                'faq_title': 'none',
                'count': count
                }
    except:
        print("exceg")
        logger.error("faqssearch function, getting wrong input search data")
        fAQs_Data = FAQs.objects.all()
        count = fAQs_Data.count()
        context = {
            'data': fAQs_Data,
            'faq_title': 'none',
            'count': count
        }
    return context

'''

BELOW FUNCTION IS FETCHING Terms & Conditions DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_terms_and_conditions_data():
    if cache.get("All_TermsConditions_data_data"):
        footer_data = cache.get("All_TermsConditions_data_data")
        logger.info("Cache data of Terms & Conditions data being rendered")
    else:
        footer_data = Footer_Links.objects.get(Footer_Links_Title__contains='Terms & Conditions')
        cache.set("All_TermsConditions_data_data", footer_data)
        logger.info("Database data of Terms & Conditions data being rendered")
    return footer_data

'''

BELOW FUNCTION IS FETCHING  Accessibility Statement DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_accessibilityStatement_data():
    if cache.get("All_AccessibilityStatement_data_data"):
        footer_data = cache.get("All_AccessibilityStatement_data_data")
        logger.info("Cache data of Accessibility Statement data being rendered")
    else:
        footer_data = Footer_Links.objects.get(
        Footer_Links_Title__contains='Accessibility Statement')
        cache.set("All_AccessibilityStatement_data_data", footer_data)
        logger.info("Database data of Accessibility Statement data being rendered")
    return footer_data


'''

BELOW FUNCTION IS FETCHING  Website Policies Sub DATA and Content FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_websitepolicy_sub_data():
    if cache.get("All_WebsitePolicies_data_data"):
        footer_sub_data = cache.get("All_WebsitePolicies_data_data")
        logger.info("Cache data of Website Policies Sub data being rendered")
    else:
        footer_sub_data = Footer_Links_Info.objects.all().filter(
        Footer_Links_Info_MainTitle__Footer_Links_Title__contains="Website Policies")
        cache.set("All_WebsitePolicies_data_data", footer_sub_data)
        logger.info("Database data of Website Policies Sub data being rendered")
    return footer_sub_data

def fetch_websitepolicy_content_data():
    if cache.get("All_Copyright_data"):
        content = cache.get("All_Copyright_data")
        logger.info("Cache data of Website Policies Content data being rendered")
    else:
        content = Footer_Links_Info.objects.all().filter(
        Footer_Links_Info_SubTitle="Copyright Policy")[0]
        cache.set("All_Copyright_data", content)
        logger.info("Database data of Website Policies Content data being rendered")
    return content


'''

BELOW FUNCTION IS FETCHING  Sitemap FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def  fetch_sitemap_data():
    if cache.get("All_Sitemap_data"):
        footer_data = cache.get("All_Sitemap_data")
        logger.info("Cache data of Sitemap data being rendered")
    else:
        footer_data = Footer_Links.objects.get(
        Footer_Links_Title__contains='Sitemap')
        cache.set("All_Sitemap_data", footer_data)
        logger.info("Database data of Sitemap data being rendered")
    return footer_data


'''

BELOW FUNCTION IS FETCHING  Help Sub DATA and Content FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_help_sub_data():
    if cache.get("All_help_data"):
        footer_sub_data = cache.get("All_help_data")
        logger.info("Cache data of Help Sub data being rendered")
    else:
        footer_sub_data = Footer_Links_Info.objects.all().filter(
        Footer_Links_Info_MainTitle__Footer_Links_Title__contains="help")
        cache.set("All_help_data", footer_sub_data)
        logger.info("Database data of Help Sub data being rendered")
    return footer_sub_data

def fetch_help_content_data():
    if cache.get("All_Reader_data"):
        content = cache.get("All_Reader_data")
        logger.info("Cache data of Help Content data being rendered")
    else:
        content = Footer_Links_Info.objects.all().filter(
        Footer_Links_Info_SubTitle="Screen Reader Access")[0]
        cache.set("All_Reader_data", content)
        logger.info("Database data of Help Content data being rendered")
    return content


# Dashborad Page Helper Functions Starts

'''

BELOW FUNCTION IS FETCHING calculate_totaldownloadcount_tools DATA and calculate_totaldownloadcount_resources DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''
def calculate_totaldownloadcount_tools():
    if cache.get("Total_Tools_DownloadCount"):
        Total_Tools_DownloadCount = cache.get("Total_Tools_DownloadCount")
        logger.info("Cache data of Total_Tools_DownloadCount being rendered")
    else:
        Total_Tools_DownloadCount = ToolsData.objects.aggregate(
        Sum('ToolsData_DownloadCounter'))
        cache.set("Total_Tools_DownloadCount", Total_Tools_DownloadCount)
        logger.info("Database data of Total_Tools_DownloadCount being rendered")
    return Total_Tools_DownloadCount


def calculate_totaldownloadcount_resources():
    if cache.get("Total_ResourceData_DownloadCount"):
        Total_ResourceData_DownloadCount = cache.get("Total_ResourceData_DownloadCount")
        logger.info("Cache data of Total_ResourceData_DownloadCount being rendered")
    else:
        Total_ResourceData_DownloadCount = ResourceData.objects.aggregate(
        Sum('ResourceData_DownloadCounter'))
        cache.set("Total_ResourceData_DownloadCount", Total_ResourceData_DownloadCount)
        logger.info("Database data of Total_ResourceData_DownloadCount being rendered")
    return Total_ResourceData_DownloadCount


'''

BELOW FUNCTION IS FETCHING All_SuccessStories_Category_dashboard DATA, All_Resources_Category_dashboard and All_tools_Category_dashboard DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_SuccessStories_Category():
    if cache.get("All_SuccessStories_Category_dashboard"):
        successStories_CategoryData = cache.get("All_SuccessStories_Category_dashboard")
        logger.info("Cache data of All_SuccessStories_Category_dashboard being rendered")
    else:
        successStories_CategoryData = SuccessStories_Category.objects.all()
        cache.set("All_SuccessStories_Category_dashboard", successStories_CategoryData)
        logger.info("Database data of All_SuccessStories_Category_dashboard being rendered")
    return successStories_CategoryData


def fetch_Tools_Category():
    if cache.get("All_tools_Category"):
        toolsCategory_data = cache.get("All_tools_Category")
        logger.info("Cache data of All_tools_Category being rendered")
    else:
        toolsCategory_data = Tools_Category.objects.all()
        cache.set("All_tools_Category", toolsCategory_data)
        logger.info("Database data of All_tools_Category being rendered")
    return toolsCategory_data


def fetch_Resources_Category():
    if cache.get("All_Resources_Category"):
        resourcesCategory_data = cache.get("All_Resources_Category")
        logger.info("Cache data of All_Resources_Category_dashboard being rendered")
    else:
        resourcesCategory_data = Resources_Category.objects.all()
        cache.set("All_Resources_Category", resourcesCategory_data)
        logger.info("Database data of All_Resources_Category_dashboard being rendered")
    return resourcesCategory_data


'''

BELOW FUNCTION IS FETCHING All_SuccessStories_Category_Name DATA and COUNT OF TOTAL STORIES PER CATEGORY DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''


def fetch_SuccessStoriescategory_name_dashboard(successStories_CategoryData):
    SuccessStoriescategory_name = []
    if cache.get("All_SuccessStoriesCat_name_dashboard_toDisplay"):
        SuccessStoriescategory_name = cache.get("All_SuccessStoriesCat_name_dashboard_toDisplay")
        logger.info("Cache data of All_Resources_Category_Name being rendered")
    else:
        for n in successStories_CategoryData:
            SuccessStoriescategory_name.append(n.SuccessStories_CategoryType)
        cache.set("All_SuccessStoriesCat_name_dashboard_toDisplay", SuccessStoriescategory_name)
        logger.info("Database data of All_Resources_Category_Name being rendered")
    return SuccessStoriescategory_name


def fetch_countOfStoriesWithCategory_dashboard(successStories_CategoryData):
    countOfStoriesWithCategory = []
    if cache.get("All_SuccessStoriescount_dashboard_toDisplay"):
        countOfStoriesWithCategory = cache.get("All_SuccessStoriescount_dashboard_toDisplay")
        logger.info("Cache data of Count of total stories per category data being rendered")
    else:
        for n in successStories_CategoryData:
            count = SuccessStories.objects.filter(
                    SuccessStories_category__SuccessStories_CategoryType=n.SuccessStories_CategoryType).count()
            countOfStoriesWithCategory.append(count)
        cache.set("All_SuccessStoriescount_dashboard_toDisplay", countOfStoriesWithCategory)
        logger.info("Database data of Count of total stories per category data being rendered")
    return countOfStoriesWithCategory


'''

BELOW FUNCTION IS FETCHING All_tools_category_name DATA and COUNT OF TOTAL TOOLS PER CATEGORY DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_toolscategory_name_dashboard(toolsCategory_data):
    toolscategory_name = []
    if cache.get("All_toolsCat_name_dashboard_toDisplay"):
        toolscategory_name = cache.get("All_toolsCat_name_dashboard_toDisplay")
        logger.info("Cache data of All_toolscategory_Name being rendered")
    else:
        for n in toolsCategory_data:
            toolscategory_name.append(n.Tools_CategoryType)
        cache.set("All_toolsCat_name_dashboard_toDisplay", toolscategory_name)
        logger.info("Database data of All_toolscategory_Name being rendered")
    return toolscategory_name


def fetch_countOfToolsWithCategory_dashboard(toolsCategory_data):
    countOfToolsWithCategory = []
    if cache.get("All_Toolscount_dashboard_toDisplay"):
        countOfToolsWithCategory = cache.get("All_Toolscount_dashboard_toDisplay")
        logger.info("Cache data of Count of total tools per category data being rendered")
    else:
        for n in toolsCategory_data:
            count = ToolsData.objects.filter(
                    ToolsData_CategoryType__Tools_CategoryType=n.Tools_CategoryType).count()
            countOfToolsWithCategory.append(count)
        cache.set("All_Toolscount_dashboard_toDisplay", countOfToolsWithCategory)
        logger.info("Database data of Count of total tools per category data being rendered")
    return countOfToolsWithCategory



'''

BELOW FUNCTION IS FETCHING All_resources_category_name DATA and COUNT OF RESOURCES PER CATEGORY DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_resourcescategory_name_dashboard(resourcesCategory_data):
    resourcescategory_name = []
    if cache.get("All_resourcesCat_name_dashboard_toDisplay"):
        resourcescategory_name = cache.get("All_resourcesCat_name_dashboard_toDisplay")
        logger.info("Cache data of All_resourcescategory_Name being rendered")
    else:
        for n in resourcesCategory_data:
                resourcescategory_name.append(n.Resources_CategoryType)
        cache.set("All_resourcesCat_name_dashboard_toDisplay", resourcescategory_name)
        logger.info("Database data of All_resourcescategory_Name being rendered")
    return resourcescategory_name


def fetch_countOfResourcesWithCategory_dashboard(resourcesCategory_data):
    countOfResourcesWithCategory = []
    if cache.get("All_resourcescount_dashboard_toDisplay"):
        countOfResourcesWithCategory = cache.get("All_resourcescount_dashboard_toDisplay")
        logger.info("Cache data of Count of total resources per category data being rendered")
    else:
        for n in resourcesCategory_data:
            count = ResourceData.objects.filter(
                    ResourceData_CategoryType__Resources_CategoryType=n.Resources_CategoryType).count()
            countOfResourcesWithCategory.append(count)
            
        cache.set("All_resourcescount_dashboard_toDisplay", countOfResourcesWithCategory)
        logger.info("Database data of Count of total resources per category data being rendered")
    return countOfResourcesWithCategory



'''

BELOW FUNCTION IS FETCHING All_tools_name DATA and TOOLS DOWNLOADED COUNT PER TOOL DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_toolsName_hitCount_Per_Name(tools_id):
    toolsName_hitCount_Per_Name = []
    if cache.get("All_toolsName_hitCount_Per_Name_data"):
        toolsName_hitCount_Per_Name = cache.get("All_toolsName_hitCount_Per_Name_data")
        logger.info("Cache data of tools downloaded count per tool data being rendered")
    else:
        for tool_id in tools_id:
            data = ToolsData.objects.values('ToolsData_DownloadCounter').get(id=tool_id)  
            toolsName_hitCount_Per_Name.append(data["ToolsData_DownloadCounter"])
        cache.set("All_toolsName_hitCount_Per_Name_data", toolsName_hitCount_Per_Name)
        logger.info("Database data of tools downloaded count per tool data being rendered")
    return toolsName_hitCount_Per_Name


def fetch_toolsName_dashboard(tools_id):
    toolsName = []
    if cache.get("All_toolsName_data_dashboard"):
        toolsName = cache.get("All_toolsName_data_dashboard")
        logger.info("Cache data of tool name data being rendered")
    else:
        for tool_id in tools_id:
            datname = ToolsData.objects.values('ToolsData_HeadingName').get(id=tool_id)
            toolsName.append(datname["ToolsData_HeadingName"])
        cache.set("All_toolsName_data_dashboard", toolsName)
        logger.info("Database data of tool name data being rendered")
    return toolsName



'''

BELOW FUNCTION IS FETCHING All_resources_name DATA and TOOLS DOWNLOADED COUNT PER RESOURCE DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_resourcesName_hitCount_Per_Name(id_resources):
    resourcesName_hitCount_Per_Name = []
    if cache.get("All_resourcesName_hitCount_Per_Name"):
        resourcesName_hitCount_Per_Name = cache.get("All_resourcesName_hitCount_Per_Name")
        logger.info("Cache data of resources downloaded count per tool data being rendered")
    else:
        for resource_id in id_resources:
            data = ResourceData.objects.values('ResourceData_DownloadCounter').get(id=resource_id)
            resourcesName_hitCount_Per_Name.append(data["ResourceData_DownloadCounter"])
        cache.set("All_resourcesName_hitCount_Per_Name", resourcesName_hitCount_Per_Name)
        logger.info("Database data of resources downloaded count per tool data being rendered")
    return resourcesName_hitCount_Per_Name

def fetch_resourcesName_dashboard(id_resources):
    resourcesName = []
    if cache.get("All_resourcesName_data_dashboard"):
        resourcesName = cache.get("All_resourcesName_data_dashboard")
        logger.info("Cache data of resources name data being rendered")
    else:
        for resource_id in id_resources:
            datname = ResourceData.objects.values(
                    'ResourceData_HeadingName').get(id=resource_id)
            resourcesName.append(datname["ResourceData_HeadingName"])
        cache.set("All_resourcesName_data_dashboard", resourcesName)
        logger.info("Database data of resources name data being rendered")
    return resourcesName



'''

BELOW FUNCTION IS FETCHING All TOOLS DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''


def fetch_all_tools_data():
    if cache.get("All_tools_data"):
        tools_data = cache.get("All_tools_data")
        logger.info("cache data of all tools")
    else:
        tools_data = ToolsData.objects.all()
        cache.set("All_tools_data", tools_data)
        logger.info("Database data of all tools")
    return tools_data


'''

BELOW FUNCTION IS FETCHING All RESOURCES DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_all_resources_data():
    if cache.get("All_resources_data"):
        resources_data = cache.get("All_resources_data")
        logger.info("database data of all tools")
        logger.info("Cache data of all resources")
    else:
        resources_data = ResourceData.objects.all()
        cache.set("All_resources_data", resources_data)
        logger.info("Database data of all resources")
    return resources_data

# Dashborad Page Helper Functions Ends


# Tools Page with search Helper Functions Starts
'''

BELOW FUNCTION IS FETCHING TOOLS DATA AFTER SERACHED FUNCTION WITH PAGINATION FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_tools_searched_data(request,url):
    try:
        tools_searched_slug = request.POST.get("toolname")
        if tools_searched_slug != '':
            tools_searched_name = tools_searched_slug.replace(" ", "-")
            tools_searched_name = tools_searched_name.replace("<", "-")
            tools_searched_name = tools_searched_name.replace("-", "-")
            tools_searched_name = tools_searched_name.replace(">", "-")
            tools_searched_name = tools_searched_name.replace("(", "-")
            tools_searched_name = tools_searched_name.replace(")", "-")
            tools_searched_name = tools_searched_name.replace("`", "-")
            tools_searched_name = tools_searched_name.replace("'", "-")
            tools_searched_name = tools_searched_name.replace("=", "-")
            tools_searched_name = tools_searched_name.replace("+", "-")
            tools_searched_name = tools_searched_name.replace("@", "-")
            tools_searched_name = tools_searched_name.replace("#", "-")
            tools_searched_name = tools_searched_name.replace("$", "-")
            print("datasearched",tools_searched_name)
            Tools_search=url+tools_searched_name
            if cache.get(Tools_search):
                tools_Data=cache.get(Tools_search)
                logger.info("Inside toolsSearch function,fetching Tools_Data data by search data through cache")
            else:
                tools_Data = ToolsData.objects.filter(ToolsData_slug__icontains=tools_searched_name)
                cache.set(Tools_search,tools_Data)
                logger.info("Inside toolsSearch function,fetching Tools_Data data by search data through database")
            logger.info("Finally, Tools page getting displayed with serached title")
        else:
            logger.info("Tools page getting displayed with all tools data")
            tools_Data=fetch_all_tools_data()
            logger.info("Finally, Tools page getting displayed without serached title")
        page = Paginator(tools_Data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = tools_Data.count()
        context = {
            'toolsdata': tools_Data,
            'tools_title': tools_searched_name,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
            }
    except:
        logger.error("toolsSearch function, getting wrong input search data")
        tools_Data=fetch_all_tools_data()
        page = Paginator(tools_Data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = tools_Data.count()
        context = {
            'toolsdata': tools_Data,
            'tools_title': 'none',
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    return context


    
def fetch_tools_searched_data_pagination(request,tools_title,url):
    if tools_title != 'none':
        tools_searched_name = tools_title.replace(" ", "-")
        tools_searched_name = tools_searched_name.replace(" ", "-")
        tools_searched_name = tools_searched_name.replace("<", "-")
        tools_searched_name = tools_searched_name.replace("-", "-")
        tools_searched_name = tools_searched_name.replace(">", "-")
        tools_searched_name = tools_searched_name.replace("(", "-")
        tools_searched_name = tools_searched_name.replace(")", "-")
        tools_searched_name = tools_searched_name.replace("`", "-")
        tools_searched_name = tools_searched_name.replace("'", "-")
        tools_searched_name = tools_searched_name.replace("=", "-")
        tools_searched_name = tools_searched_name.replace("+", "-")
        tools_searched_name = tools_searched_name.replace("@", "-")
        tools_searched_name = tools_searched_name.replace("#", "-")
        tools_searched_name = tools_searched_name.replace("$", "-")
        logger.info("Tools page getting displayed with searched tools data by slugs")
        Tools_search_name=url+tools_searched_name
        if cache.get(Tools_search_name):
            tools_Data=cache.get(Tools_search_name)
            logger.info("Inside toolsSearch function,fetching Tools_Data data by search data through cache for pagination")
        else:
            tools_Data = ToolsData.objects.filter(ToolsData_slug__icontains=tools_searched_name)
            cache.set(Tools_search_name,tools_Data)
            logger.info("Inside toolsSearch function,fetching Tools_Data data by search data through database for pagination")   
    else:
        logger.info("Tools page getting displayed with all tools data")
        tools_Data=fetch_all_tools_data()
    page = Paginator(tools_Data, 8)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    count = tools_Data.count()
    logger.info("hereee", tools_Data)
    context = {
            'toolsdata': tools_Data,
            'tools_title': tools_title,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    return context


# Tools Page with search Helper Functions Ends



# Tools Page with category filteration Helper Functions Starts

'''

BELOW FUNCTIONS ARE FETCHING TOOLS DATA AFTER CATEGORY FILTERATION FUNCTION WITH PAGINATION FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_tools_data_with_selected_category(request,url):  
    if request.POST.get('all_checkbox') != 'all_Checked':
        category_name = []
        filtered_Tools_Data = ToolsData.objects.none()
        checklist = request.POST.getlist('checkbox')
        Tools_Category.objects.all().update(Tools_Cat_Status=False)
        try:
            for cat_check in checklist:
                Tools_Category.objects.filter(
                    pk=int(cat_check)).update(Tools_Cat_Status=True)
            checklist.append(10101010110101010101)
            if cache.get(checklist):
                toolsData_Checked=cache.get(checklist)
                logger.info("Inside tools function, fetching Tools_Category data by selected category ids through cache")
            else:
                toolsData_Checked = Tools_Category.objects.filter(id__in=checklist)
                cache.set(checklist,toolsData_Checked)
                logger.info("Inside tools function, fetching Tools_Category data by selected category ids through database")
        except:
            tools_Data=fetch_all_tools_data()
            toolsCategory_data = Tools_Category.objects.all()
            page = Paginator(tools_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = ToolsData.objects.all().count()
            logger.error("Inside tools function, error in fetching Tools_Category data by selected category ids")
            context = {
                    'toolsdata': tools_Data,
                    'tools_title': 'none',
                    'toolscategory': toolsCategory_data,
                    "page": page,
                    'status_All_Checked': 'True',
                    'Pagination_Type': 'All_Data',
                    'count': count
                }
        try:
            for cat_check_name in toolsData_Checked:
                category_name.append(cat_check_name.Tools_CategoryType)
            category_name.append("ToFetch_FilteredTools_With_Cache")
            to_fetch = tuple(category_name)
            if cache.get(to_fetch):
                filtered_Tools_Data=cache.get(to_fetch)
                logger.info("Inside tools function,fetching Tools_Data data by selected category name through cache")
            else:
                for cat_name in to_fetch:
                    filtered_Tools_Data = filtered_Tools_Data | ToolsData.objects.filter(
                        ToolsData_CategoryType__Tools_CategoryType__contains=cat_name)
                cache.set(to_fetch,filtered_Tools_Data)
                logger.info("Inside tools function,fetching Tools_Data data by selected category name through database") 
        except:
            toolsCategory_data = Tools_Category.objects.all()
            page = Paginator(tools_Data, 8)
            Tools_Category.objects.all().update(Tools_Cat_Status=False)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = ToolsData.objects.all().count()
            logger.error("Inside tools function, error in fetching Tools_Data data by selected category name")
            context = {
                    'toolsdata': tools_Data,
                    'tools_title': 'none',
                    'toolscategory': toolsCategory_data,
                    "page": page,
                    'status_All_Checked': 'True',
                    'Pagination_Type': 'All_Data',
                    'count': count
                }
        toolsCategory_data = Tools_Category.objects.all()
        count = filtered_Tools_Data.count()
        page = Paginator(filtered_Tools_Data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        logger.info("Tools page getting displayed with selected category filteration")
        context = {
            'toolsdata': filtered_Tools_Data,
            'tools_title': 'none',
            'toolscategory': toolsCategory_data,
            "page": page,
            'status_All_Checked': None,
            'Pagination_Type': 'Category_Post',
            'count': count
        }
    else:
        tools_Data=fetch_all_tools_data()
        logger.info("Tools page getting displayed with all category filteration")
        page = Paginator(tools_Data, 8)
        Tools_Category.objects.all().update(Tools_Cat_Status=False)
        toolsCategory_data = Tools_Category.objects.all()
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = ToolsData.objects.all().count()
        context = {
            'toolsdata': tools_Data,
            'tools_title': 'none',
            'toolscategory': toolsCategory_data,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count
        }
    return context


def fetch_filteredToolsdata_for_pagination(to_fetch):
    if cache.get(to_fetch):
        filtered_Tools_Data=cache.get(to_fetch)
        logger.info("Inside tools function,fetching Tools_Data data by selected category name through cache for pagination")
    else:
        for cat_name in to_fetch:
            filtered_Tools_Data = filtered_Tools_Data | ToolsData.objects.filter(
                        ToolsData_CategoryType__Tools_CategoryType__contains=cat_name)
        cache.set(to_fetch,filtered_Tools_Data)
        logger.info("Inside tools function,fetching Tools_Data data by selected category name through database for pagination")  
    return filtered_Tools_Data

# Tools Page with category filteration Helper Functions Ends


# Resources Page with search Helper Functions Starts
'''

BELOW FUNCTION IS FETCHING RESOURCES DATA AFTER SERACHED FUNCTION WITH PAGINATION FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''
def fetch_resources_searched_data(request,url):
    try:
        resource_searched_slug= request.POST.get("resourcename")
        if resource_searched_slug != '':
            resource_search_name = resource_searched_slug.replace(" ", "-")
            resource_search_name = resource_search_name.replace("<", "-")
            resource_search_name = resource_search_name.replace("-", "-")
            resource_search_name = resource_search_name.replace(">", "-")
            resource_search_name = resource_search_name.replace("(", "-")
            resource_search_name = resource_search_name.replace(")", "-")
            resource_search_name = resource_search_name.replace("`", "-")
            resource_search_name = resource_search_name.replace("'", "-")
            resource_search_name = resource_search_name.replace("=", "-")
            resource_search_name = resource_search_name.replace("+", "-")
            resource_search_name = resource_search_name.replace("@", "-")
            resource_search_name = resource_search_name.replace("#", "-")
            resource_search_name = resource_search_name.replace("$", "-")
            resources_search=url+resource_search_name
            if cache.get(resources_search):
                resource_Data=cache.get(resources_search)
                logger.info("Inside resourceSearch function, fetching ResourceData data by searched name through cache")
            else:
                resource_Data = ResourceData.objects.filter(ResourceData_slug__icontains=resource_search_name)
                cache.set(resources_search,resource_Data)
                logger.info("Inside resourceSearch function, fetching ResourceData data by searched name through database")
        else:
            logger.info("Resources page getting displayed with all data")
            resource_Data=fetch_all_resources_data()
        page = Paginator(resource_Data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = resource_Data.count()
        context = {
            'resoucesdata': resource_Data,
            'resource_title': resource_search_name,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    except:
        logger.info("resourceSearch function, getting wrong input search data")
        resource_Data=fetch_all_resources_data()
        page = Paginator(resource_Data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = resource_Data.count()
        context = {
            'resoucesdata': resource_Data,
            'resource_title': 'none',
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    return context



def fetch_resources_serached_data_pagination(request,url,resource_title):
    if resource_title != 'none':
        resource_search_name = resource_title.replace(" ", "-")
        resource_search_name = resource_search_name.replace("<", "-")
        resource_search_name = resource_search_name.replace("-", "-")
        resource_search_name = resource_search_name.replace(">", "-")
        resource_search_name = resource_search_name.replace("(", "-")
        resource_search_name = resource_search_name.replace(")", "-")
        resource_search_name = resource_search_name.replace("`", "-")
        resource_search_name = resource_search_name.replace("'", "-")
        resource_search_name = resource_search_name.replace("=", "-")
        resource_search_name = resource_search_name.replace("+", "-")
        resource_search_name = resource_search_name.replace("@", "-")
        resource_search_name = resource_search_name.replace("#", "-")
        resource_search_name = resource_search_name.replace("$", "-")
        logger.info( "Resources page getting displayed with searched data by slugs with pagination")
        resources_search_name=url+resource_search_name
        if cache.get(resources_search_name):
            resource_Data=cache.get(resources_search_name)
            logger.info("Inside resourceSearch function, fetching ResourceData data by searched name through cache")
        else:
            resource_Data = ResourceData.objects.filter(ResourceData_slug__icontains=resource_search_name)
            cache.set(resources_search_name,resource_Data)
            logger.info("Inside resourceSearch function, fetching ResourceData data by searched name through database")
    else:
        logger.info("Resources page getting displayed with all data")
        resource_Data=fetch_all_resources_data()
    page = Paginator(resource_Data, 8)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    count = resource_Data.count()
    context = {
            'resoucesdata': resource_Data,
            'resource_title': resource_title,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    return context

# Resources Page with search Helper Functions Ends


# Resources Page with category filteration Helper Functions Starts

'''

BELOW FUNCTIONS ARE FETCHING RESOURCES DATA AFTER CATEGORY FILTERATION FUNCTION WITH PAGINATION FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_resources_data_with_selected_category(request,url):
    if request.POST.get('all_checkbox') != 'all_Checked':
        category_name = []
        filtered_resources_data = ResourceData.objects.none()
        checklist = request.POST.getlist('checkbox')
        Resources_Category.objects.all().update(Resources_Cat_Status=False)
        try:
            for n in checklist:
                Resources_Category.objects.filter(
                    pk=int(n)).update(Resources_Cat_Status=True)
            checklist.append(20202020220202020202)
            if cache.get(checklist):
                resources_data_Checked=cache.get(checklist)
                logger.info("Inside resources function, fetching Resources_Category data by selected category ids through cache")
            else:
                resources_data_Checked = Resources_Category.objects.filter(
                id__in=checklist)
                cache.set(checklist,resources_data_Checked)
                logger.info("Inside resources function, fetching Resources_Category data by selected category ids through database") 
        except:
            resources_data=fetch_all_resources_data()
            logger.info( "Resources page getting displayed with all category filteration")
            page = Paginator(resources_data, 8)
            Resources_Category.objects.all().update(Resources_Cat_Status=False)
            resouces_category_data=Resources_Category.objects.all()
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = resources_data.count()
            context = {
                'resoucesdata': resources_data,
                'resource_title': 'none',
                'resourcescategory': resouces_category_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }
        try:
            for cat_Type in resources_data_Checked:
                category_name.append(cat_Type.Resources_CategoryType)
            category_name.append("ToFetch_FilteredResources_With_Cache")
            to_fetch = tuple(category_name)
            if cache.get(to_fetch):
                filtered_resources_data=cache.get(to_fetch)
                logger.info("Inside resources function, fetching ResourceData data by selected category names through cache")
            else:
                for cat_name in to_fetch:
                    filtered_resources_data = filtered_resources_data | ResourceData.objects.filter(
                    ResourceData_CategoryType__Resources_CategoryType__contains=cat_name)
                cache.set(to_fetch,filtered_resources_data)
                logger.info("Inside resources function, fetching ResourceData data by selected category names through database")
        except:
            resources_Data=fetch_all_resources_data()
            logger.info( "Resources page getting displayed with all category filteration")
            page = Paginator(resources_Data, 8)
            Resources_Category.objects.all().update(Resources_Cat_Status=False)
            resouces_category_data=Resources_Category.objects.all()
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = resources_Data.count()
            context = {
                'resoucesdata': resources_Data,
                'resource_title': 'none',
                'resourcescategory': resouces_category_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }
        resouces_category_data=Resources_Category.objects.all()
        count = filtered_resources_data.count()
        page = Paginator(filtered_resources_data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        logger.info("Resources page getting displayed with selected category filteration")
        context = {
            'resoucesdata': filtered_resources_data,
            'resource_title': 'none',
            'resourcescategory': resouces_category_data,
            "page": page,
            'status_All_Checked': None,
            'Pagination_Type': 'Category_Post',
            'count': count
        }
        
    else:
        resources_Data=fetch_all_resources_data()
        logger.info("Resources page getting displayed with all category filteration")
        page = Paginator(resources_Data, 8)
        Resources_Category.objects.all().update(Resources_Cat_Status=False)
        resouces_category_data=Resources_Category.objects.all()
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = resources_Data.count()
        context = {
            'resoucesdata': resources_Data,
            'resource_title': 'none',
            'resourcescategory': resouces_category_data,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count
        }
    return context
        

def fetch_resources_fultereddata_for_pagination(to_fetch):
    if cache.get(to_fetch):
        filtered_resources_data=cache.get(to_fetch)
        logger.info("Inside resources function, fetching ResourceData data by selected category names through cache for pagination")
    else:
        for cat_name in to_fetch:
            filtered_resources_data = filtered_resources_data | ResourceData.objects.filter(
                ResourceData_CategoryType__Resources_CategoryType__contains=cat_name)
        cache.set(to_fetch,filtered_resources_data)
        logger.info("Inside resources function, fetching ResourceData data by selected category names through database for pagination")
    return filtered_resources_data

# Resources Page with category filteration Helper Functions Ends


# Services Page Helper Functions Starts

'''

BELOW FUNCTIONS ARE FETCHING SERVICES DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''
def fetch_all_services_data():
    if cache.get("All_servicesdata_data"):
        servicesdata = cache.get("All_servicesdata_data")
        logger.info("Cache data for all services data")
    else:
        servicesdata = Services.objects.all()
        cache.set("All_servicesdata_data", servicesdata)
        logger.info("Database data for all services data")
    return servicesdata

# Services Page Helper Functions Ends


'''

BELOW FUNCTIONS ARE FETCHING Websitepolicies DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_all_Websitepolicies_sub_data():
    if cache.get("All_WebsitePolicies_sub_data_data"):
        footer_sub_data = cache.get("All_WebsitePolicies_sub_data_data")
        logger.info("Cache data WebsitePolicies_sub_data")
    else:
        footer_sub_data = Footer_Links_Info.objects.all().filter(
            Footer_Links_Info_MainTitle__Footer_Links_Title__contains="Website Policies")
        cache.set("All_WebsitePolicies_sub_data_data", footer_sub_data)
        logger.info("Database data WebsitePolicies_sub_data")
    return footer_sub_data



'''

BELOW FUNCTIONS ARE FETCHING Help DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''
def fetch_help_sub_data_with_id():
    if cache.get("All_help_sub_data_data"):
        footer_sub_data = cache.get("All_help_sub_data_data")
        logger.info("Cache data for help_sub_data")
    else:
        footer_sub_data = Footer_Links_Info.objects.all().filter(
                Footer_Links_Info_MainTitle__Footer_Links_Title__contains="help")
        cache.set("All_help_sub_data_data", footer_sub_data)
        logger.info("Database data for help_sub_data")
    return footer_sub_data


'''

BELOW FUNCTIONS ARE FETCHING All_empanelled_agecies_data DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''
def fetch_All_empanelled_agecies_data():
    if cache.get("All_empanelled_agecies_data"):
        footer_sub_data = cache.get("All_empanelled_agecies_data")
        logger.info("Cache data for All_empanelled_agecies_data")
    else:
        empanelled_agecies_data = EmpanelledAgencies.objects.all()
        cache.set("All_empanelled_agecies_data", empanelled_agecies_data)
        logger.info("Database data for All_empanelled_agecies_data")
    return empanelled_agecies_data


'''

BELOW FUNCTIONS ARE FETCHING translation_quote_data WITH CURRENT USER DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''
# def fetch_translation_quote_data_dashborad(current_user):
#     if cache.get("All_translation_quote_data"):
#         footer_sub_data = cache.get("All_translation_quote_data")
#         logger.info("Cache data for All_translation_quote ")
#     else:
#         translation_quote_data = TranslationQuote.objects.filter(
#             username=current_user)
#         cache.set("All_translation_quote_data", translation_quote_data)
#         logger.info("Database data for All_translation_quote")
#     return footer_sub_data


'''

BELOW FUNCTIONS ARE FETCHING translation_quote_data_with_applicationNo WITH APPLICATION NUMBER DATA FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

# def fetch_translation_quote_data_with_applicationNo(application_number):
#     if cache.get(application_number):
#         translation_quote_data = cache.get(application_number)
#         logger.info("Cache data for translation_quote_data_with_applicationNo")
#     else:
#         translation_quote_data = TranslationQuote.objects.filter(
#                 application_number=application_number)[0]
#         cache.set(application_number, translation_quote_data)
#         logger.info("Database data for translation_quote_data_with_applicationNo")
#     return translation_quote_data




# Success Stories Page  Helper Functions Starts


'''

BELOW FUNCTIONS ARE FETCHING fetch_All_SuccessStories_Category_data FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''


def fetch_All_SuccessStories_Category_data():
    if cache.get("All_SuccessStories_Category_data"):
        successStories_CategoryData = cache.get(
                "All_SuccessStories_Category_data")
        logger.info("Cache data for All_SuccessStories_Category_data")
    else:
        successStories_CategoryData = SuccessStories_Category.objects.order_by(
                'SuccessStories_Cat_Priority')
        cache.set("All_SuccessStories_Category_data",
                      successStories_CategoryData)
        logger.info("Database data for All_SuccessStories_Category_data")
    return successStories_CategoryData



'''

BELOW FUNCTIONS ARE FETCHING fetch_All_SuccessStories_Category_data FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_All_SuccessStories_data():
    if cache.get("All_SuccessStories_data"):
        successStoriesData = cache.get("All_SuccessStories_data")
        logger.info("cache data")
    else:
        successStoriesData = SuccessStories.objects.order_by(
            'SuccessStories_Priority')
        cache.set("All_SuccessStories_data", successStoriesData)
        logger.info("database data")
    return successStoriesData
        
'''

BELOW FUNCTIONS ARE FETCHING fetch_SuccessStories_data as per serached title FROM EITHER DATABASE OR CACHE IF AVAILABLE

'''

def fetch_successstories_searched_data(request,url):
    try:
        story_searchData12 = request.POST.get("storyname")
        if story_searchData12 != '':
            story_searchData1 = story_searchData12.replace(" ", "-")
            story_searchData1 = story_searchData1.replace("-", "-")
            story_searchData1 = story_searchData1.replace(">", "-")
            story_searchData1 = story_searchData1.replace("(", "-")
            story_searchData1 = story_searchData1.replace(")", "-")
            story_searchData1 = story_searchData1.replace("`", "-")
            story_searchData1 = story_searchData1.replace("'", "-")
            story_searchData1 = story_searchData1.replace("=", "-")
            story_searchData1 = story_searchData1.replace("+", "-")
            story_searchData1 = story_searchData1.replace("@", "-")
            story_searchData1 = story_searchData1.replace("#", "-")
            story_searchData1 = story_searchData1.replace("$", "-")
            stories_search = url+story_searchData1
            if cache.get(stories_search):
                successStoriesData = cache.get(stories_search)
                logger.info("Inside successStoriesSearch function,fetching Stories_Data data by search data through cache")
            else:
                successStoriesData = SuccessStories.objects.filter(
                    SuccessStories_slug__icontains=story_searchData1).order_by('SuccessStories_Priority')
                cache.set(stories_search, successStoriesData)
                logger.info("Inside successStoriesSearch function,fetching Stories_Data data by search data through database")
            logger.info("Finally, Success stories page getting displayed with serached title")
        else:
            logger.info("Success stories page getting displayed with all stories data")
            successStoriesData = SuccessStories.objects.all().order_by('SuccessStories_Priority')
            logger.info("Finally, Success stories page getting displayed without serached title")  
        page = Paginator(successStoriesData, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = successStoriesData.count()
        context = {
            'SuccessStoriesData': successStoriesData,
            'story_title': story_searchData1, 
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    except:
        logger.error("tsuccess stories Search function, getting wrong input search data")
        successStoriesData = SuccessStories.objects.all().order_by('SuccessStories_Priority')
        page = Paginator(successStoriesData, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = successStoriesData.count()
        context = {
            'SuccessStoriesData': successStoriesData,
            'story_title': 'none', 
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    return context

'''

BELOW FUNCTIONS ARE FETCHING fetch_SuccessStories_data as per serached title  with paginationFROM EITHER DATABASE OR CACHE IF AVAILABLE

'''
def fetch_success_stories_data_with_pagination(request,url,story_title):
    if story_title != 'none':
        story_searchData = story_title.replace(" ", "-")
        story_searchData1 = story_searchData.replace("-", "-")
        story_searchData1 = story_searchData1.replace(">", "-")
        story_searchData1 = story_searchData1.replace("(", "-")
        story_searchData1 = story_searchData1.replace(")", "-")
        story_searchData1 = story_searchData1.replace("`", "-")
        story_searchData1 = story_searchData1.replace("'", "-")
        story_searchData1 = story_searchData1.replace("=", "-")
        story_searchData1 = story_searchData1.replace("+", "-")
        story_searchData1 = story_searchData1.replace("@", "-")
        story_searchData1 = story_searchData1.replace("#", "-")
        story_searchData1 = story_searchData1.replace("$", "-")
        stories_search1 = url+story_searchData1
        if cache.get(stories_search1):
            successStoriesData = cache.get(stories_search1)
            logger.info("cache data")
        else:
            successStoriesData = SuccessStories.objects.filter(
                SuccessStories_slug__icontains=story_searchData1).order_by('SuccessStories_Priority')
            cache.set(stories_search1, successStoriesData)
            logger.info("database data")
        logger.info(
            "Success stories  page getting displayed with searched data by heading with pagination")
    else:
        logger.info("Success stories page getting displayed with all stories data with pagination")
        successStoriesData = SuccessStories.objects.all().order_by('SuccessStories_Priority')
    page = Paginator(successStoriesData, 8)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    count = successStoriesData.count()
    context = {
        'SuccessStoriesData': successStoriesData,
        'story_title': story_title,
        "page": page,
        'status_All_Checked': 'True',
        'Pagination_Type': 'Searched_Post',
        'count': count
    }
    return context


# Success Stories Page  Helper Functions Ends




'''
    BELOW FUNCTION ARE UASED TO ENCRYPT AND DECRYPT PASSWORDS WITH REGISTRATION , LOGIN , CHANGE PASSWORD VIEW FUNCTIONS

'''


def encrypt(pas):
    try:        
        pas = str(pas)
        cipher_pass = Fernet(settings.ENCRYPT_KEY)
        encrypt_pass = cipher_pass.encrypt(pas.encode('ascii'))
        encrypt_pass = base64.urlsafe_b64encode(encrypt_pass).decode("ascii") 
        print("inside1",cipher_pass)
        print("inside2",encrypt_pass)
        return encrypt_pass
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(pas):
    try:
        pas = base64.urlsafe_b64decode(pas)
        cipher_pass = Fernet(settings.ENCRYPT_KEY)
        decod_pass = cipher_pass.decrypt(pas).decode("ascii")     
        return decod_pass
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None
