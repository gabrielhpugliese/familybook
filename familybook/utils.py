import simplejson as json
import logging


class FileEncoder(json.JSONEncoder):
    def default(self, obj, *args, **kwargs):
        logging.error(type(obj))
        if isinstance(obj, str):
            return str(obj)
#        else:
#            return json.JSONEncoder(obj, *args, **kwargs)
