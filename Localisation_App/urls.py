from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views


'''
BELOW URL PATTERNS CONTAINS THE VARIOUS URLS AND THEIR RESPECTIVE CALLING VIEWS .
THE REQUEST KEYWORDS IN URL ARE MAPPED IN THIS URLPATTERN BLOCK TO DIFFERENT VIEWS WITH NAME
SITEMAP OF WEBSITE CAN BE MADE USING ALL THE URLS MENTIONED HERE IN URLPATTERN BLOCK .
'''


app_name = 'Localisation_App'

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('toolsPage/', views.toolsPage, name='toolsPage'),
    path('toolsPage/<id>', views.toolsPage, name='toolsPage'),
    path('tools/', views.tools, name='tools'),
    path('toolsDownloadCounter/<int:id>',
         views.toolsDownloadCounter, name='toolsDownloadCounter'),
    path('toolsReset/', views.toolsReset, name='toolsReset'),
    path('toolsSearch/', views.toolsSearch, name='toolsSearch'),
    path('resourcesPage/', views.resourcesPage, name='resourcesPage'),
    path('resourcesPage/<id>', views.resourcesPage, name='resourcesPage'),
    path('resources/', views.resources, name='resources'),
    path('resourceDownloadCounter/<int:id>',
         views.resourceDownloadCounter, name='resourceDownloadCounter'),
    path('resourcesReset/', views.resourcesReset, name='resourcesReset'),
    path('resourceSearch/',
         views.resourceSearch, name='resourceSearch'),
    path('services/', views.services, name='services'),
    path('successstoryPage/', views.successstoryPage, name='successstoryPage'),
    path('successstory/', views.successstory, name='successstory'),
    path('successstorySearch/',
         views.successstorySearch, name='successstorySearch'),
    path('successstoryPage/<id>',views.successstoryPage, name='successstoryPage'),
    #     path('successstoryReset/', views.successstoryReset, name='successstoryReset'),
    path('submit/', views.submit, name='submit'),
    path('faqs/', views.faqs, name='faqs'),
    path('faqs/<data>',views.faqs,name='faqs'),
    path('faqsSearch/', views.faqsSearch, name='faqsSearch'),
    path('contactus/', views.contactus, name='contactus'),
    path('websitepolicy/', views.websitepolicy, name='websitepolicies'),
    path('websitepolicy/<int:id>', views.websitepolicydata,
         name='websitepolicydata'),
    path('termsandcondition/', views.termsandcondition, name='termsandcondition'),
    path('accessibilityStatement/', views.accessibilityStatement,
         name='accessibilityStatement'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('help/', views.help, name='help'),
    path('submit/<img>', views.submit, name='submit'),
    path('help/<int:id>', views.helpData, name='helpData'),
    path('srvEnableTyping/', views.srvEnableTyping, name='srvEnableTyping'),
    path('srvGoTranslateWebLocalizer/', views.srvGoTranslateWebLocalizer,
         name='srvGoTranslateWebLocalizer'),
    path('srvOnscreenKeyboard/', views.srvOnscreenKeyboard,
         name='srvOnscreenKeyboard'),
    path('srvTTS/', views.srvTTS, name='srvTTS'),
    path('srvTransliteration/', views.srvTransliteration,
         name='srvTransliteration'),


    path('goTranslate/', views.goTranslate,
         name='goTranslate'),
#     path('translation-quote/', views.translation_quote,
#          name='translation_quote'),
#     path('translation-quote-user-dashboard', views.translation_quote_user_dashboard,
#          name='translation_quote_user_dashboard'),
#     path('translation-quote-show/<str:application_number>/',
#          views.translation_quote_show, name='translation_quote_show'),
    #     path('dashboard2', views.dashboard2, name="dashboard2"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('machine-translation/', views.machine_translation,
         name="machine_translation"),
    path('name-matcher/', views.name_matcher, name="name_matcher"),
    path('empanelled_agencies/', views.empanelled_agencies,
         name="empanelled_agencies"),
    path('bhashini/', views.bhashini, name="bhashini"),
    path('anuvaad/', views.anuvaad, name="anuvaad")

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL,
#                           document_root=settings.STATIC_ROOT)
