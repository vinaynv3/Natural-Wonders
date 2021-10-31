from .datahandler import *
from .filehandler import *


data_handlers = {'LocationsAPI':LocationList,
                'LocationAPI':LocationName,
                'LocationGeoAPI':LocationGeo,
                'LocationStatsAPI':LocationStats,
                'LocationPicAPI':LocationPic,
                'PicDownloadAPI':LocationDwnldPic,
                'LocationSpeciesAPI':LocationSpecies,
                'LocationSpecieAPI':LocationSpeciesPics}


# request data management factory for endpoints for url /locations/ and after
def request_data_handler(request,view_cls_name,delete=False,
                            placeholder=None,pic=None,specie=None):

    cls = data_handlers.get(view_cls_name,None)
    if cls:
        obj = cls(data=request,placeholder=placeholder,picture=pic,specie=specie)
        return obj.process_request()
