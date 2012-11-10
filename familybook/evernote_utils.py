import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NoteTypes
import hashlib
import binascii


def create_image_resource(image):
    md5 = hashlib.md5()
    md5.update(image)
    image_hash = md5.digest()

    data = Types.Data()
    data.size = len(image)
    data.bodyHash = hash
    data.body = image

    resource = Types.Resource()
    resource.mime = 'image/png'
    resource.data = data

    return (resource, image_hash)


def create_note(title, content, image_resource=None):
    note = Types.Note()
    hash_hex = ''

    if image_resource:
        (resource, image_hash) = image_resource
        note.resources = [resource]
        hash_hex = binascii.hexlify(image_hash)

    note.title = title
    note.content = '''<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
    <en-note>Here is the note:<br/>
    %s ''' % content
    if hash_hex:
        note.content += '<en-media type="image/jpeg" hash="%s"/>' % hash_hex
    note.content += '</en-note>'

    return note


def create_notebook(name):
    notebook = Types.Notebook()
    notebook.name = name

    return notebook


def parse_note(notebook):
    pass
