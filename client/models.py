from django.db import models
from datetime import datetime


# Create your models here.

############## Client ################
class Client(models.Model):
    client_username = models.CharField(max_length=50)
    client_password = models.CharField(max_length=50)
    client_avatar = models.ImageField(upload_to ="images/", blank = True,null=True)
    client_email = models.CharField(max_length=50)
    client_tel = models.CharField(max_length=50)
    def __str__(self):
        return self.client_username


############## Contact ################
'''
Here we will relate this Contact table(model) with 
the client table(model) with the foreign key
'''
class Contact(models.Model):
    #id of the logged in client
    client = models.ForeignKey(Client, on_delete= models.CASCADE)
    #To contact with available users in database and hide myself
    contact_with = models.ForeignKey(Client, related_name="contact_with", on_delete= models.CASCADE)
    #other rows in the table
    contact_username = models.CharField(max_length=50)
    contact_avatar = models.ImageField(upload_to ="images/", blank = True,null=True)
    contact_email = models.CharField(max_length=50)
    contact_tel = models.CharField(max_length=50)
    
    
################## Message ################## 

class Message(models.Model):
    message_from = models.ForeignKey(Client, related_name="message_from", on_delete=models.CASCADE)
    message_to =  models.ForeignKey(Client, related_name="message_to", on_delete=models.CASCADE)
    message_body = models.TextField()
    message_date = models.DateTimeField(default=datetime.now, blank=True)












