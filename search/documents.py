import django
from django_elasticsearch_dsl import Document,Index, fields
from django_elasticsearch_dsl.registries import registry
from Localisation_App.models import FAQs, SuccessStories, ToolsData, ResourceData
from elasticsearch_dsl import analyzer


@registry.register_document
class FaqsDocument(Document):
    class Index:
        name='faqs'
        settings={
            'number_of_shards':1,
            'number_of_replicas':0
        }
   

    FAQs_Answer = fields.TextField(
        attr=None
    )
    class Django:
        model = FAQs
        fields = [
            'id',
            'FAQs_Question',
            # 'FAQs_Answer'
        ]

@registry.register_document
class SuccessStoriesDocument(Document):
    class Index:
        name='successstories'
        settings={
            'number_of_shards':1,
            'number_of_replicas':0
        }
    SuccessStories_Description = fields.TextField(
        attr=None
    )
    
    class Django:
        model = SuccessStories
        fields = [
            'id',
            'SuccessStories_TitleName'
        ]

@registry.register_document
class ToolsDataDocument(Document):
    class Index:
        name='tools'
        settings={
            'number_of_shards':1,
            'number_of_replicas':0
        }
    ToolsData_Description = fields.TextField(
        attr=None
    )
    
    class Django:
        model = ToolsData
        fields = [
            'id',
            'ToolsData_HeadingName'
        ]

@registry.register_document
class ResourceDataDocument(Document):
    class Index:
        name='resources'
        settings={
            'number_of_shards':1,
            'number_of_replicas':0
        }
    ResourceData_Description = fields.TextField(
        attr=None
    )
    
    class Django:
        model = ResourceData
        fields = [
            'id',
            'ResourceData_HeadingName'
        ]

