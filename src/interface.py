from .datahandler import *

# request data management factory for endpoints for url /locations/ and after
def request_data_handler(request,view_cls_name,delete=False,
                            placeholder=None,pic=None):

    data_handlers = {'LocationsAPI':LocationList,
                    'LocationAPI':LocationName,
                    'LocationGeoAPI':LocationGeo}

    cls = data_handlers.get(view_cls_name,None)
    if cls:
        obj = cls(data=request, placeholder=placeholder,picture=pic)
        return obj.process_request()
