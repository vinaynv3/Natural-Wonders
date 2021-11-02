<h1 align="center">Natural Wonders</h1>

REST API contains detailed information about some of the magnificent, beautiful and breathtaking landscapes around the world, each landscape introduces itself with its name, location and description,followed by landscape properties such as geography, statistics and flora fauna living at the location, every landscape has one picture, and several pictures of the species. 
Landscape climate, latitude/longitude, type information is associated with geography, total annual visitors, popularity (stars), altitude above sea level , unesco recognitation status can be found in key stats, finally species live at the location are categorized based on  species name, picture, class, endangered status can be found in keyword species.
![image](https://github.com/vinaynv3/Natural-Wonders/blob/master/src/static/naturalwonders.jpg)
<img src="./src/static/species.jpg " alt="InfiniteGraph Logo" width="960" height="330">

## Table of Contents
1. [Docs](#Docs)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Collaboration](#instructions)
5. [FAQs](#faqs)
### Docs
***
api documentation details at  ![natural_wonders_docs](http://vinaynv3.pythonanywhere.com/)
```
      landscape_details_schema:list: [
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
```
## Technologies
***
A list of technologies used within the project:
* [Python3](https://www.python.org/): (version 3.8.10)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/): version 2.0.2
* [WSGI Server - Werkzeug](https://palletsprojects.com/p/werkzeug/): version 2.0.2
* [bash - linux shell](https://www.gnu.org/software/bash/): Version 5.0.1.7

## Installation
***
app nstallation steps. 
```
$ git clone https://github.com/vinaynv3/Natural-Wonders.git
$ cd ../path/to/the/file
$ python3 -m venv <name_of_virtualenv>
$ pip install -r requirements.txt
$ cd app/scripts
$ bash db_setup.sh    #intialize database
$ bash dev_server.sh  #starts flask development server
```
Side information: To start the application  use ```flask run``` verify app env variable ```export FLASK_APP=<app_name>```
## Collaboration
***
I built natural api for educational purpose and with a great admiration for the natural world, if you see any issues,let me know or any feedback would be appreciated.
