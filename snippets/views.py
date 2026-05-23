"""
View is a class or a function that receives a http response , performs some logic and returns the http response 



What is CSRF?

CSRF = Cross Site Request Forgery

Imagine you're logged into a banking website.

A malicious website secretly sends:

POST /transfer-money

using your session.

CSRF protection prevents such fake requests.

Normally Django expects a CSRF token:

<input hidden value="token123">

But APIs often don't use forms, so in the tutorial they temporarily disable it:
"""


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

@csrf_exempt
def snippet_list(request):   # this method is made to get and 
    """
    listt all  code snippets , or create a new snippet. 
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets , many = True)
        return JsonResponse(serializer.data , safe = False)  #json  response expects a dictionary but here it is a list so safe is turned to false 
    elif request.method == 'POST':   
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)   # here we can see we have not given an existing instance in get argument , so it will tell the drf to create a new instance and if data validates , it will automatically call the create()  method and insert a new row in table
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data , status = 201)
        return JsonResponse(serializer._errors , status = 400)
    

""" now we need a function to retreive , update or delete a particular snippet 
"""
@csrf_exempt
def snippet_detail(request , pk): #pk means the primary key
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:  # here  the  exception is used because without it , it will throw a large error and crashes , here excemption catcches the error and instead of crashing , it sends user the 404 error
        return HttpResponse(status = 404)
    
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)
    
    elif request.method == 'POST':
        data = JSONParser().parse(snippet)
        serializer = SnippetSerializer(snippet , data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(status = 400)
    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
    