#we need something that converts  Pyhton/DJango object to JSON and vice versa 
# that something  is called as a serializer 
# serializtion  means Convert a complex object into a simpler transferable format.
# here the feild will look same because here we wre defining the same data but for the API  , not for the DB 
# and serializer class does not have a text feild , it only stores as string in char feild 
"""The serializer mainly handles:

converting data ↔ objects
validation
creating objects (create())
updating objects (update())
Deletion is usually not part of the serializer's responsibility.

Deletion normally happens in the view.
"""

from rest_framework import serializers
from snippets.models import Snippet , LANGUAGE_CHOICES , STYLE_CHOICES
from django.contrib.auth.models import User
# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only = True)
#     title = serializers.CharField(required = False , allow_blank = True , max_length = 100)
#     code = serializers.CharField(style = {"base_template" : "textarea.html"}) # this tells when showing this feild in the DRF web interface , use a large multilinie text area instead of one line text input 
#     linenos = serializers.BooleanField(required = True)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES , default = "python") # here the choice feild is  there but in models it was char feild becaause , in db we only store strings and do not require much validation , but when taking taking an input via  api we need to validate is the input is among the choices or not .
#     style = serializers.ChoiceField(choices=STYLE_CHOICES , default = "friendly")

#     def create(self , validated_data):
#         """
#         create and return a new Snippet instance 
        
#         , given the validated data 
#         when data comes from the client in json format 
#         def receives a python dictionary , and we then do serializer = SnippetSerializer(data=data)
#         then serializer.is_valid() ,,this  is by default in the serializer class 
#         def validates everything , if successfull it passes the data to create(validated_data)
#         """
#         return Snippet.objects.create(**validated_data) #  '**' this is used to tell that the data is in dictioonary form and expand it into keyword arguments 
#         """ also the code we wrote above , it it shorter version of
#             def create(self, validated_data):

#     snippet = Snippet(
#         title=validated_data["title"],
#         code=validated_data["code"],
#         language=validated_data["language"]
#     )

#     snippet.save()

#     return snippet

#     this code , and we can  see that .save() is automatically called above  
#         """ 

#     def update(self , instance , validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get("title" , instance.title) # meaning = get this key if exists or use the default value  dictionary.get(key , default_value)
#         instance.code = validated_data.get("code" , instance.code)
#         instance.linenos = validated_data.get("linenos", instance.linenos)
#         instance.language = validated_data.get("language", instance.language)
#         instance.style = validated_data.get("style", instance.style)
#         instance.save()
#         return instance


# the upper method is the django method where we only use Serializer class but rest framework gives a better option to use ModelSerializer class that inherits from serializer class
# ModelSerializer class automatically creates the serializers by looking at the model and also generated the create() and update() methods . 




"""
This field is doing something quite interesting. The source argument controls which attribute is used to populate a field, and can point at any attribute on the serialized instance. It can also take the dotted notation shown above, in which case it will traverse the given attributes, in a similar way as it is used with Django's template language.

The field we've added is the untyped ReadOnlyField class, in contrast to the other typed fields, such as CharField, BooleanField etc... The untyped ReadOnlyField is always read-only, and will be used for serialized representations, but will not be used for updating model instances when they are deserialized. We could have also used CharField(read_only=True) here.
"""
class SnippetSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    class Meta:
        model = Snippet
        fields = ["id" , "title" , "code" , "linenos" , "language" , "style" , "owner"]


# because anippets is not included in the Users model by default so we have to explicitly add it in the feilds 
class UserSerializer (serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(
        many = True , queryset = Snippet.objects.all()
    )
    class Meta:
        model = User
        fields = ["id" , "username" , "snippets"]