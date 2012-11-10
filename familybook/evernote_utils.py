import hashlib
import binascii
import re
from StringIO import StringIO

import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NoteTypes
from lxml import etree


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


def create_note(title, content, notebook_guid='', image_resource=None):
    hash_hex = ''
    note = Types.Note()
    if notebook_guid:
        note.notebookGuid = notebook_guid

    if image_resource:
        (resource, image_hash) = image_resource
        note.resources = [resource]
        hash_hex = binascii.hexlify(image_hash)

    note.title = title
    note.content = '''<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
    <en-note><caption>Here is the note:<br/>
    %s</caption>''' % content
    if hash_hex:
        note.content += '<en-media type="image/png" hash="%s"/>' % hash_hex
    note.content += '</en-note>'

    return note


def create_notebook(name):
    notebook = Types.Notebook()
    notebook.name = name

    return notebook


def parse_note(content):
    tree = etree.parse(StringIO(content), etree.HTMLParser())
    try:
        note_content = tree.xpath('//en-note')[0].text
    except:
        note_content = ''

    return note_content

