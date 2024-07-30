from django.shortcuts import render , redirect, HttpResponse
from .models import WebbForm, Responses
from json import loads , dumps
from .confirmationMail import sendConfirmation
from django.views.decorators.clickjacking import xframe_options_exempt 
import pytz
def addForm(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=='POST':
        newForm = WebbForm()
        newForm.form_name = request.POST['formName']
        newForm.user = request.user
        newForm.save()
        print('New form created')
        return redirect(f'/forms/editform/{newForm.id}')
    return render(request, 'addForm.html', {})

def editForm(request, formId):
    if not request.user.is_authenticated:
        return redirect('login')
    formObject= WebbForm.objects.get(id=int(formId))
    if formObject.user!=request.user:
        return render(request, 'unautorisedError.html' , {})
    if request.method=='POST':
        formObject.formSchema = request.POST['schema']
        formObject.customCSS = request.POST['customCSS']
        formObject.form_name = request.POST['formTitle']
        formObject.success_message = request.POST['successMessage']
        formObject.emailRecieptsEnabled = True if 'emailRecieptEnabled' in request.POST else False
        formObject.headerEnabled = True if 'enableHeader' in request.POST else False
        formObject.save() 
    return render(request,  'editForm.html', { 'formSchema': formObject.formSchema , 'customCSS':formObject.customCSS , 'formName': formObject.form_name , 'successMessage' : formObject.success_message , 'emailReciepts': formObject.emailRecieptsEnabled , 'enableHeader': formObject.headerEnabled , "formID": formId} )

@xframe_options_exempt
def webbForm(request, formId):
    formObject = WebbForm.objects.get(id=int(formId))
    if not formObject.formSchema:
        return HttpResponse('Invalid/Empty form')
    if request.method=='POST':
        formResponse = Responses()
        formResponse.form = WebbForm.objects.get(id = int(formId))
        submittedResponse = dict(request.POST)
        del(submittedResponse['csrfmiddlewaretoken'])
        formResponse.response = dumps(submittedResponse)
        formResponse.save()
        if formObject.emailRecieptsEnabled and formObject.user.email:
            sendConfirmation(formObject.form_name, formObject.user.email , submittedResponse, formResponse.timesTamp.astimezone(pytz.timezone('Asia/Kolkata')))
    formHTML = ''
    schema = loads(formObject.formSchema)
    for i,element in enumerate(schema):
        formHTML+='<div class="formInputElement">'
        id = ''
        classList = ''
        if element['classList']:
            classList= 'class="' +element['fieldClassList']+'"'
        if element['ID']:
            id=element['ID']
        else:
            id='element'+str(i)
        if element['label']:
            formHTML+= f'<label for="{id}">{element['label']}</label>'
        if element['type'] in ['text', 'email','url','number']:
            if element['placeholder']:
                placeholder='placeholder="'+element['placeholder']+'"'
            else:
                placeholder=''
            formHTML+=f'<input type="{element['type']}" {placeholder} id="{id}" name="{element['name']}" {classList} { 'required' if 'required' in element.keys() and element['required']==True else ''} >'
        if element['type']=='textarea':
            if element['placeholder']:
                placeholder='placeholder="'+element['placeholder']+'"'
            else:
                placeholder=''
            if element['placeholder']:
                placeholder='placeholder="'+element['placeholder']+'"'
            else:
                placeholder=''
            formHTML+=f'<textarea rows="5" type="{element['type']}" {placeholder} id="{id}" name="{element['name']}" {classList} { 'required' if 'required' in element.keys() and element['required']==True else ''}></textarea>'

        if element['type']=='radio':
            formHTML+=f'<div id="{id}" {classList}>'
            for j,option in enumerate(element['options']):
                formHTML+=f'<label for="{id}+_option{j}"><input type="radio" id="{id}+_option{j}"  {'required' if 'required' in element.keys() and element['required']==True else ''} name="{element['name']}" value="{option}"> {option} </label>'
            formHTML+='</div>'
        if element['type']=='checkbox':
            formHTML+=f'<div id="{id}" {classList} {'requiredcheckbox' if 'required' in element.keys() and element['required']==True else ''}>'
            for j,option in enumerate(element['options']):
                formHTML+=f'<label for="{id}+_option{j}"> <input type="checkbox" id="{id}+_option{j}"  name="{element['name']}" value="{option}">  {option}</label> ' 
            formHTML+='</div>'
        if element['type']=='dropdown':
            formHTML+=f'<select id="{id}" name="{element['name']}" {classList}>'
            for j,option in enumerate(element['options']):
                formHTML+=f'<option id="{id}+_option{j}" " value="{option}"> {option} </option>'
            formHTML+='</select> <br>'
        formHTML+='</div>'
    return render(request , 'webbForm.html' , {'schema': formHTML , 'customCSS' : '<style>\n'+formObject.customCSS+ '</style>' if formObject.customCSS else '' , 'successMessage': formObject.success_message if request.method=='POST' else '' , 'formName': formObject.form_name, 'headerenabled': formObject.headerEnabled , 'formTitle': formObject.form_name })

def responses(request, formId):
    webForm = WebbForm.objects.get(id=int(formId))
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user== webForm.user:
        formResponses = Responses.objects.filter(form = WebbForm.objects.get(id=int(formId)))
        responseList = [(response.timesTamp, loads(response.response).items() , response.id )for response in formResponses]
        formName = webForm.form_name
        return render(request, 'responses.html', {'responses': responseList, 'formName': formName})
    else:
        return render(request, 'unautorisedError.html', {})
    
def deleteForm(request, formId):
    formObject= WebbForm.objects.get(id=int(formId))
    if '/account' in request.META['HTTP_REFERER'] and request.user==formObject.user:
        formObject.delete()
    return HttpResponse('')

def deleteResponse(request, responseID):
    responsObject = Responses.objects.get(id = int(responseID))
    if f'forms/responses/{responsObject.form.id}' in request.META['HTTP_REFERER'] and request.user==responsObject.form.user:
        responsObject.delete()
    return HttpResponse('')