import functools

from django.conf import settings
from thrift.transport.THttpClient import THttpClient
from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from evernote.edam.userstore import UserStore
from evernote.edam.notestore import NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors


def with_evernote(func):
    @functools.wraps(func)
    def wraps(*args, **kwargs):
        user_store_http_client = THttpClient(settings.EVERNOTE_STORE_URI)
        user_store_protocol = TBinaryProtocol(user_store_http_client)
        user_store = UserStore.Client(user_store_protocol)

        note_store_url = user_store.getNoteStoreUrl(
            settings.EVERNOTE_DEVELOPER_TOKEN)
        note_store_http_client = THttpClient(note_store_url)
        note_store_protocol = TBinaryProtocol(note_store_http_client)
        note_store = NoteStore.Client(note_store_protocol)

        kwargs['user_store'] = user_store
        kwargs['note_store'] = note_store
        return func(*args, **kwargs)

    return wraps
