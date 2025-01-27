# Import necessary modules from Django
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from simple_history.models import HistoricalRecords

# Define a new model class named ActivityLogs

#the class is a table in the database,and the rest are columns 
class ActivityLogs(models.Model):
    
    # Define a foreign key to the User model. If the user is deleted, set this field to NULL.
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Define a character field to store the action performed by the user.
    #this is stuff like log in ,log out ,delete or update
    action = models.CharField(max_length=100)
    
    # Define a text field to store a detailed description of the action.
    description = models.TextField()
    
    # Define a character field to store the origin of the action.
    #this is either admin or user ,just gives more informatio on who did what
    origin = models.CharField(max_length=255, null=True, blank=True)
    
    # Define a datetime field to store the timestamp of when the log entry was created.
    # This field is automatically set to the current date and time when the entry is created.
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Define a field to store the IP address from which the action was performed.
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # Define a character field to store the user agent string of the browser or client used.
    # This is like whatsapp log file that says you used windows 
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    
    # Define a character field to store the X-Forwarded-For header value.
    #if the client uses a proxy this will help us know the original ip address
    x_forwarded_for = models.CharField(max_length=255, null=True, blank=True)
    
    # Define a foreign key to the ContentType model. If the content type is deleted, set this field to Null
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Define a positive integer field to store the object ID.
    object_id = models.PositiveIntegerField(null=True, blank=True)
    
    # Define a generic foreign key that combines content_type and object_id to create a generic relation.
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Add historical records to the model using the django-simple-history package.
    # This allows tracking changes to instances of this model over time.
    history = HistoricalRecords()
    
    # Define the string representation of the ActivityLogs model.
    # This method returns a string that includes the timestamp, action, and user.
    def __str__(self):
        return f"{self.timestamp} - {self.action} - {self.user}"