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




# @csrf_exempt
# def snippet_list(request):   # this method is made to get and 
#     """
#     listt all  code snippets , or create a new snippet. 
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets , many = True)
#         return JsonResponse(serializer.data , safe = False)  #json  response expects a dictionary but here it is a list so safe is turned to false 
#     elif request.method == 'POST':   
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)   # here we can see we have not given an existing instance in get argument , so it will tell the drf to create a new instance and if data validates , it will automatically call the create()  method and insert a new row in table
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data , status = 201)
#         return JsonResponse(serializer._errors , status = 400)
    

# """ now we need a function to retreive , update or delete a particular snippet 
# """
# @csrf_exempt
# def snippet_detail(request , pk): #pk means the primary key
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:  # here  the  exception is used because without it , it will throw a large error and crashes , here excemption catcches the error and instead of crashing , it sends user the 404 error
#         return HttpResponse(status = 404)
    
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return JsonResponse(serializer.data)
    
#     elif request.method == 'POST':
#         data = JSONParser().parse(snippet)
#         serializer = SnippetSerializer(snippet , data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status = 201)
#         return JsonResponse(status = 400)
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)

"""
upper code was what django gave us , now we move on to the Rest framework , 
Request object - REST framework introduces a Request object that extends the regular HttpRequest, and provides more flexible request parsing. The core functionality of the Request object is the request.data attribute, which is similar to request.POST, but more useful for working with Web APIs.
Response object - automatically renders the data into the format asked by the client , earlier we had to type Jsonresponse etc.
Status codes -- Using numeric HTTP status codes in your views doesn't always make for obvious reading, and it's easy to not notice if you get an error code wrong. REST framework provides more explicit identifiers for each status code, such as HTTP_400_BAD_REQUEST in the status module. It's a good idea to use these throughout rather than using numeric identifiers.
Wrapping API views -- REST framework provides two wrappers you can use to write API views.

1. The @api_view decorator for working with function based views.
2. The APIView class for working with class-based views.
These wrappers provide a few bits of functionality such as making sure you receive Request instances in your view, and adding context to Response objects so that content negotiation can be performed.
The wrappers also provide behavior such as returning 405 Method Not Allowed responses when appropriate, and handling any ParseError exceptions that occur when accessing request.data with malformed input.
"""


"""
Adding optional format suffixes to our URLs
To take advantage of the fact that our responses are no longer hardwired to a single content type let's add support for format suffixes to our API endpoints. Using format suffixes gives us URLs that explicitly refer to a given format, and means our API will be able to handle URLs such as http://example.com/api/items/4.json.
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

@api_view(["GET" , "POST"])
def snippet_list(request , format = None):
    """list all the code snippets ,  or create new snippet """
    if request.method == "GET":
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets , many= True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = SnippetSerializer(data = request.data) # earlier we used data = JsonParser , but now request.data automatically parses it into python data structure
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data ,status=status.HTTP_201_CREATED)
        
@api_view(["GET" , "DELETE" , "PUT"])
def snippet_details(request,pk, format = None):
    """
    Retrieve , update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = SnippetSerializer(snippet , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)