.. Landscapes documentation master file, created by
   sphinx-quickstart on Mon Nov  8 17:58:37 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Natural Wonders REST API Docs
=============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Overview
--------

Repository API that contains detailed information about some of the magnificent,
beautiful and breathtaking landscapes around the world, each landscape has
extensive APIs that help in introducing each landscape's name, country its
located in and a brief description about itself.
Landscape extensive APIs help in adding and managing its geography, statistics
and flora fauna, every landscape has one picture, and associated pictures of
the species live in there. Landscape climate, latitude/longitude, type
information is associated with geography key, total annual visitors,
popularity (stars), altitude above sea level , UNESCO recognition status can
be found in under key called stats, finally species live in there are been
classified based on specie name,picture, class (mammal,reptile,bird,etc.,),
endangered status can be found in keyword species.

Installation
------------

To experiment natural wonders code, follow the steps below and
install it using pip:

.. code-block:: console

    $ git clone https://github.com/vinaynv3/Natural-Wonders.git
    $ cd ../path/to/the/file
    $ python3 -m venv <name_of_virtualenv>
    $ pip install -r requirements.txt
    $ cd app/scripts
    $ bash db_setup.sh    #intialize database
    $ bash dev_server.sh  #starts flask development server

API schema
----------

.. code-block:: console

    [
    {
      name: <str:required>,
      about: <str:required>,
      country: <str:required>",
      Picture: {
        picture: <img_file>
      },
      Geography: {
        lat_long: <str>,
        climate: <str:required>,
        landscape": <str:required>
      },
      stats: {
        yearly_visitors: <int>,
        stars: <str>,
        altitude: <str>,
        unesco_heritage: <bool>
      },
      species: {
        species_name: <str:required>,
        endangered: <bool>,
        pic: <file>,
        sp_class: <str>
                }
       }
     ]


Endpoints
---------


- Access list of landscapes, add a new landscape or list of landscapes

    http://vinaynv3.pythonanywhere.com/locations/

    .. code-block:: console

        import requests
        requests.get('http://vinaynv3.pythonanywhere.com/locations/')

        [{'name': 'amazon rainforest',
          'about': 'There is no place on earth quite like it,....'
          'country': 'south america (brazil,peru,columbia)',
          'geography': {'climate': 'tropical',
                        'landscape': 'forest',
                        'lat_long': '3.4653° S, 62.2159° W'},
          'picture': {'_dwnld': '/locations/amazon-rainforest/pic/amazon.jpg',
                      'picture': 'amazon.jpg'},
          'stats': {'above_sealevel': 105,
                    'stars': 1,
                    'unesco_heritage': True,
                    'yearly_visitors': 10000}},
          'species':
          [{'_dwnld_pic':
          '/locations/amazon-rainforest/species/parrots/parrots.png',
          '_specie': '/locations/amazon-rainforest/species/parrots/',
          'endangered': False,
          'pic': 'parrots.png',
          'sp_class': 'bird',
          'sp_slug': 'parrots',
          'species_name': 'parrots'},
        {'_dwnld_pic': '/locations/amazon-rainforest/species/myrtle/myrtle.jpg',
        .....}.....]

    :methods: GET,POST
    :return: list:[dict:{name:str,about:str,country:str},...]


- Access a landscape details with GET, modify it with PUT and record can be
  removed through DELETE

  http://vinaynv3.pythonanywhere.com/locations/{name}/

  :methods: GET,PUT,DELETE
  :return: dict:{name:str,about:str,country:str}


- Access a landscape geography details with GET, if record doesn't exist add
  one with POST, modify existing one with PUT and geography record can be
  removed through DELETE

  http://vinaynv3.pythonanywhere.com/locations/{name}/geo/

  :methods: GET,POST,PUT,DELETE
  :return: dict:{lat_long:str,climate:str,landscape:str}



- Access a landscape stats details with GET, if record doesn't exist add one
  with POST, modify existing one with PUT and stats record can be removed
  through DELETE

  http://vinaynv3.pythonanywhere.com/locations/{name}/stats/

  :methods: GET,POST,PUT,DELETE
  :return: dict:{yearly_visitors:int,stars:int,above_sealevel:int,
                  unesco_heritage:bool}
  :note: altitude above sealevel measured in meters(m)


- Access a landscape image with GET, if record doesn't exist add one with
  POST, modify existing one with PUT.

  http://vinaynv3.pythonanywhere.com/locations/{name}/pic/

  :methods: GET,POST,PUT,DELETE
  :return: dict: {picture:file}
  :note: content type:multipart/formdata, allowed extensions
         ('png', 'jpg', 'jpeg', 'gif')


- Download landscape image with GET, remove it from database with DELETE.

  http://vinaynv3.pythonanywhere.com/locations/{name}/pic/{filename}

  :methods: GET,DELETE
  :return: file:{image}

- Access list of species living at location, list of species can be added
  through POST, caution, all species can be removed through DELETE

    http://vinaynv3.pythonanywhere.com/locations/{name}/species/

    :methods: GET,POST,DELETE
    :return: list:[dict:{name:str,endangered:bool,sp_class:str},...]
    :note: cannot add picture at this endpoint, use per specie path to add one


- Access specie details, can be modified through PUT, caution, remove it
  through DELETE

  http://vinaynv3.pythonanywhere.com/locations/{name}/species/{specie_name}/

  :methods: GET,PUT,DELETE
  :return: dict:{name:str,endangered:bool,sp_class:str,pic:file}


- Download specie image with GET, remove it from database with DELETE

  http://vinaynv3.pythonanywhere.com/locations/{name}/species/{specie_name}/{file}

  :methods: GET,PUT,DELETE
  :return: dict:{name:str,endangered:bool,sp_class:str,pic:file}



Contribute
----------

- Issue Tracker: https://github.com/vinaynv3/Natural-Wonders/issues
- Source Code: https://github.com/vinaynv3/Natural-Wonders/
