from dataclasses import fields
from math import fabs
from typing import Dict
from django.shortcuts import render

from django.core.paginator import Paginator

from Localisation_App.models import SuccessStories
from .documents import FaqsDocument, SuccessStoriesDocument, ToolsDataDocument, ResourceDataDocument
from Localisation_App.models import TopMenuItems, FooterMenuItems
import re
# Create your views here.

def search(request):
    q = request.GET.get("q")
    print("search term ",q)
    regex = re.search('[@!#$%^&*()<>/\|}{~:]',str(q))
    print("regex check ",regex)
    # totalfaqs1 = FaqsDocument.search()
    # total = totalfaqs1.count()

    # totalfaqs = totalfaqs1[:total]
    # for i in totalfaqs:
    #     print("iii  ", i)
    # print('total faqs1 ',totalfaqs)
    
    top_menu_items_data = TopMenuItems.objects.all()
    footer_menu_items_data = FooterMenuItems.objects.all()
        
    if(regex==None):
        faqs = FaqsDocument.search()
        totalfaqs = faqs[:faqs.count()]
        successstory = SuccessStoriesDocument.search()
        totalsuccessstory = successstory[:successstory.count()]
        tools = ToolsDataDocument.search()
        totaltools = tools[:tools.count()]
        resources = ResourceDataDocument.search()
        totalresources = resources[:resources.count()]
        totaldata = []
        counter = 0
        for faq in totalfaqs:
            counter = counter+1
            faqs = {'title': faq.FAQs_Question}
            totaldata.append(faqs)
        print("counter faq ",counter)
        counter1  = 0
        
        for story in totalsuccessstory:
            counter1 = counter1+1
            stories = {'title': story.SuccessStories_TitleName}
            totaldata.append(stories)
        
        for tool in totaltools:
            tools = {'title': tool.ToolsData_HeadingName}
            totaldata.append(tools)

        for resource in totalresources:
            resources = {'title': resource.ResourceData_HeadingName}
            totaldata.append(resources)
        print("counter ss",counter1)
        # print("total data ",totaldata)
        print("total data length",len(totaldata))
        # totaldata = []
        if q:
            faqs = FaqsDocument.search().query('multi_match',query=q,fields=['FAQs_Question', 'FAQs_Answer'])
            successstories = SuccessStoriesDocument.search().query('multi_match',query=q, fields=['SuccessStories_TitleName', 'SuccessStories_Description'])
            tools = ToolsDataDocument.search().query('multi_match',query=q, fields=['ToolsData_HeadingName', 'ToolsData_Description'])
            resources = ResourceDataDocument.search().query('multi_match',query=q, fields=['ResourceData_HeadingName', 'ResourceData_Description'])
            data = []
            for i in faqs:
                faq = {"type":'faqs', 'data':{"id":i.id, "title": i.FAQs_Question, 'desc':i.FAQs_Answer}}
                data.append(faq)
            for i in successstories:
                successstory = {"type":'successstoryPage', 'data':{"id":i.id, "title": i.SuccessStories_TitleName, 'desc':i.SuccessStories_Description}}
                data.append(successstory)
            for i in tools:
                tool = {"type":'toolsPage', 'data':{"id":i.id, "title": i.ToolsData_HeadingName, 'desc':i.ToolsData_Description}}
                data.append(tool)
            for i in resources:
                resource = {"type":'resourcesPage', 'data':{"id":i.id, "title": i.ResourceData_HeadingName, 'desc':i.ResourceData_Description}}
                data.append(resource)
            
            paginator = Paginator(data, 10)
            total_searched_data_count = paginator.count
            page_number = request.GET.get('page')
            datafinal = paginator.get_page(page_number)
            print('data ',datafinal)
            # print(type(datafinal))
            print("total data ",totaldata)
            # return render(request, 'search/search.html', { 'searched_data': datafinal, "searched_term":q, "total_searched_data_count":total_searched_data_count, 'totaldata':totaldata})
        else:
            datafinal= ''
            print("I am in else")
            total_searched_data_count = ''
        return render(request, 'search/search.html', { 'searched_data': datafinal, "searched_term":q, "total_searched_data_count":total_searched_data_count, 'totaldata':totaldata, "topmenus":top_menu_items_data, "FooterMenuItemsdata": footer_menu_items_data})
    else:
        return render(request, 'search/search.html', { 'error_message':'enter valid search term', "topmenus":top_menu_items_data, "FooterMenuItemsdata": footer_menu_items_data})