import simplejson as json

from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

import evernote_facades
import logging


@csrf_exempt
def list_notebooks(request):
    response = evernote_facades.list_notebooks()
    return HttpResponse(json.dumps(response), mimetype='application/json')


@csrf_exempt
def list_notes(request, notebook_guid):
    notes = evernote_facades.list_notes(notebook_guid)
    response = []
    for note in notes:
        note = evernote_facades.load_note(note['NoteId'])
        response.append(note)
    return HttpResponse(json.dumps(response), mimetype='application/json')


@csrf_exempt
def load_note(request, guid):
    response = evernote_facades.load_note(guid)
    return HttpResponse(json.dumps(response), mimetype='application/json')


@csrf_exempt
def save_notebook(request):
    notebook_name = request.GET.get('notebookname')
    birthday_date = request.GET.get('birthdaydate')
    name = '%s - %s' % (notebook_name, birthday_date)

    response = evernote_facades.save_notebook(name)
    return HttpResponse(json.dumps(response), mimetype='application/json')


@csrf_exempt
def save_note(request):
    title = request.POST.get('title')
    content = request.POST.get('description')
    notebook_guid = request.POST.get('notebookid')
    post_file = request.FILES.get('image')

    response = evernote_facades.save_note(title, content, notebook_guid,
                                          post_file=post_file)
    return HttpResponse(json.dumps(response), mimetype='application/json')


