from django.shortcuts import render,redirect, HttpResponse, HttpResponseRedirect
from client.forms import *
from .models import *
import json
import csv
from django.core.paginator import Paginator



################# Create your views here ####################
def index (request):
    client = Client.objects.all()

    return render(request, "index.html",context={'client':client})


################ Register clients ##################
def register(request):
    if request.method == "GET":
        form = ClientRegisterForm()
        return render(request, 'register.html', context={'form':form})
    else:
        #send form to database and save 
        form = ClientRegisterForm(request.POST,request.FILES)
        #save if its valid
        if form.is_valid():
            form.save()
            #redirect to register page
        return redirect("/")   
    

################### Login clients ##################
def login(request):
    if request.method == "GET":
        form = ClientLoginForm()
        return render(request, 'login.html', context={'form':form})
    else:
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            #cleaning up the form password and username from the dictionary of form objects
            username = form.cleaned_data['client_username']
            password = form.cleaned_data['client_password']

            #checking if user exist in our Client object
            num = Client.objects.filter(client_username = username, client_password= password).count()
            if num > 0:
                #setting a session for client username
                request.session['username'] = username
                 
                #grabbing the id of the specific user
                client_id = Client.objects.filter(client_username=username,client_password=password)[0].id
                
                #setting a session for the client  id
                request.session['id'] = client_id
                #redirect to the main directory
                return redirect("/") 
            else:
                message = "The username or password doesn't exist"
                #sending message to the url.  
                return render(request, 'login.html', context={'form':form, 'message': message})


################# check if user is logged in ##################
def checkIfClientLoggedIn(request):
    if 'id' in request.session:
        return True
    else:
        return False

################# Logout out section ##############
def logout(request):
    #deleting the sessions
    del request.session["username"]
    del request.session["id"]
    #redirecting to login page
    return redirect("login")

################# client profiles ################
def profile(request):
    if checkIfClientLoggedIn(request):
        #getting the id of logged in user
        client = Client.objects.get(pk = request.session['id'])
        #sending the client to our profile page
        return render(request,"profile.html", context={"client":client})
    else:
        return redirect("login")


################ client edit form ###################

def editProfile(request):
    #first we grab the specific user id from session
    client = Client.objects.get(pk=request.session["id"])
    
    if request.method == 'GET':
        #then we pass the instance to the form
        form = ClientEditForm(instance=client)
        return render(request, 'editProfile.html', context={"form":form})
    else:
        #then we grab the post request and the client instance
        form = ClientEditForm(request.POST, request.FILES, instance=client)
        #validating the form
        if form.is_valid():
            #save to database
            form.save()
            #return redirect to profile page
        return redirect("profile")


###################### CONTACT SECTION #################

#add contact
def addContact(request):
    
    if request.method =="GET":
        form = CreateContactForm(initial = {"client":request.session["id"]})
        return render(request,"addContact.html", context={'form':form})
    else:
        #send form to database and save 
        form = CreateContactForm(request.POST, request.FILES)
        #save if its valid
        if form.is_valid():
           form.save()
           #redirect to register page
           return redirect("profile")

        
#Display the contact list.
def showContacts(request):
    #here we're specific with contact of the logged in client
    contacts = Contact.objects.filter(client=request.session["id"])
    #To restricts the number of items page to 1. 
    paginator = Paginator(contacts, 1)
    #To know the current page, via url
    page = request.GET.get("page")
    contacts = paginator.get_page(page)
    #sending it to the user.
    return render(request, "contacts.html", context={"contacts":contacts})

# show specific contact details
def showContact(request,id):
    contacts = Contact.objects.get(pk=id)
    return render(request, 'showContact.html', context={"contacts":contacts})

#edit contact
def editContact(request, id):
    #grabbing the specific contact id
    contact = Contact.objects.get(pk=id)

    if request.method =="GET":
        form = CreateContactForm(instance=contact)
        return render(request,"editContact.html", context={'form':form})
    else:
        #send form to database and save 
        form = CreateContactForm( request.POST, request.FILES, instance = contact)
        #save if its valid
        if form.is_valid():
           form.save()
           #redirect to register page
           return redirect("contacts")

#delete contact
def deleteContact(request, id):
    contact = Contact.objects.get(pk=id)
    contact.delete()
    return redirect("contacts")


#Search contact
def search(request):
    #grabbing our contacts
    contacts =  contacts = Contact.objects.filter(client=request.session["id"])
    
    #grabbing data from our form
    username= request.GET.get("username")
    email= request.GET.get("email")
    tel= request.GET.get("tel")

    if username != "":
        #don't forget the '__contains' syntax
        contacts = contacts.filter(contact_username__contains = username)
        
    if email != "":
        #don't forget the '__contains' syntax
        contacts = contacts.filter(contact_email__contains = email)
    
    if tel != "":
        #don't forget the '__contains' syntax
        contacts = contacts.filter(contact_tel__contains = tel)

    #search helper
    filter_values = {"username":username,"email":email,"tel":tel}

    return render(request, "contacts.html", context = {"contacts":contacts,"filter":filter_values})

#How to export contacts
def export(request):
    #grabbing our contacts
    contacts =  contacts = Contact.objects.filter(client=request.session["id"])
    if request.GET.get("type") =="json":        
        response_data = []
        for contact in contacts.values_list("contact_username","contact_email", "contact_tel") :
            response_data.append(contact)
        response = HttpResponse(json.dumps(response_data), content_type = "application/json")
        response["Content-Disposition"] = 'attachment;filename="contacts.json"'
        return response
    else:
        response = HttpResponse(content_type = "application/csv")
        writer = csv.writer(response)
        #specifying how we want our header row to look like
        writer.writerow(["username","email", "tell"])
        for contact in contacts.values_list("contact_username","contact_email", "contact_tel") :
            writer.writerow(contact)
        response["Content-Disposition"] = 'attachment;filename="contacts.csv"'
        return response

################# Messaging system #########################

def send_message(request, id):

    contact = Contact.objects.get(pk=id)

    if request.method == "GET":
        form = MessageForm(initial = {"message_from":contact.client,"message_to":contact.contact_with})
        messages = Message.objects.all()
        messages_related = []
        for message in messages :
            if message.message_from == contact.client and message.message_to == contact.contact_with:
                messages_related.append(message)
            elif message.message_from == contact.contact_with and message.message_to ==contact.client:
                messages_related.append(message)

        return render(request,"chat.html", context={"form":form, "messages":messages_related})
    else:
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(request.path_info)

    




















