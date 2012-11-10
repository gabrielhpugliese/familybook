import logging

from django.conf import settings
import evernote.edam.notestore.ttypes as NoteTypes

from evernote_utils import (create_note, create_image_resource, create_notebook,
                            parse_note)
from decorators import with_evernote


@with_evernote
def save_note(title, content, user_store, note_store, post_file=None):
    image = ''

    if post_file:
        for chunk in post_file.chunks():
            image += chunk

    image_resource = create_image_resource(image)
    note = create_note(title, content, image_resource)
    try:
        note_store.createNote(settings.EVERNOTE_DEVELOPER_TOKEN, note)
        response = True
    except Exception, e:
        logging.error('Error saving note: %s' % str(e))
        response = False

    return response


@with_evernote
def list_notebooks(user_store, note_store):
    notebooks_lst = []
    notebooks = note_store.listNotebooks(settings.EVERNOTE_DEVELOPER_TOKEN)
    for notebook in notebooks:
        try:
            (person_name, birthday_date) = notebook.name.split(' - ')
            this_notebook = {'NotebookId': notebook.guid,
                             'NotebookName': notebook.name,
                             'PersonName': person_name,
                             'BirthdayDate': birthday_date}
        except:
            logging.info('could not parse notebook: %s' % notebook.name)
            continue
        notebooks_lst.append(this_notebook)

    return notebooks_lst


@with_evernote
def list_notes(notebook_guid, user_store, note_store):
    note_filter = NoteTypes.NoteFilter()
    note_filter.notebookGuid = notebook_guid
    notes = note_store.findNotes(settings.EVERNOTE_DEVELOPER_TOKEN,
                                 note_filter, 0, 100).notes
    notes_lst = []
    for note in notes:
        this_note = {'NoteTitle': note.title, 'NoteId': note.guid}
        notes_lst.append(this_note)

    return notes_lst


@with_evernote
def load_note(guid, user_store, note_store):
    note = None
    try:
        note = note_store.getNote(settings.EVERNOTE_DEVELOPER_TOKEN,
                                  guid,
                                  True,
                                  True,
                                  False,
                                  False)
    except Exception, e:
        logging.error('Error on note retrieval: %s' % str(e))

    note_content = parse_note(note.content)
    note_dct = {'description': note_content}
    try:
        image = '%s/%s?auth=%s' % (settings.EVERNOTE_RESOURCE_URI,
                                   note.resources[0].guid,
                                   settings.EVERNOTE_DEVELOPER_TOKEN)
        note_dct['image'] = str(image)
    except:
        logging.info('could not get any file from this note: %s' % guid)
        note_dct['image'] = ''

    return note_dct


@with_evernote
def save_notebook(name, user_store, note_store):
    notebook = create_notebook(name)
    try:
        notebook = note_store.createNotebook(settings.EVERNOTE_DEVELOPER_TOKEN,
                                             notebook)
        response = True
    except Exception, e:
        logging.error('Error saving notebook: %s' % str(e))
        response = False

    return response

