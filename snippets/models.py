from django.db import models

# all this is for style and highlighting 
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

# Create your models here.

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # created is the column name(feild) in db , DateTimeFeild is used to store date and time in django 
    # and auto_now_add tells to fill this with current date and time when object is cretaed , but value remains same even after updation 
    # but auto_now  updats the value then object is updated 
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100 , blank=True , default="") # blank true means that this feild can be left empty  , beacuse it is a char feild max length arg is req , database type = VARCHAR(n)
    code = models.TextField() # text feild is used to store large text and does not have max length , and db type is TEXT
    linenos = models.BooleanField(default=False)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default='python' ,  max_length=100
    ) # yeh hamne vo pygments me se uthai this , uspr loop se conditions lga ke 
    style = models.CharField(choices=STYLE_CHOICES , max_length=100 , default="friendly")

    class Meta:
        ordering = ["created"]   
    # this is a special class in django that acts like settings for the model class , here it says ordering  , means to order the model according to the created feild 
    # we can also specify other feild like ['created' , "title"]  is 2 objects are created at same time they will be sorted via title
    #Django needs instructions to convert model code into SQL operations. That is what migrations do.
    # makemigrations - looks at current model , detect the chnages , generate migration instructions
    # migrate - django converts the migrations into SQL 