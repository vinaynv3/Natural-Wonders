<h1 align="center">Natural Wonders</h1>

Natural Wonders is a repository API that contains detailed information about some of the magnificent, beautiful and breathtaking landscapes around the world, each landscape has extensive APIs that help in introducing each landscape's name, country its located in and a brief description about itself. Landscape extensive APIs help in adding and managing its geography, statistics and flora fauna, every landscape has one picture, and associated pictures of the species live in there. 
Landscape climate, latitude/longitude, type information is associated with geography key, total annual visitors, popularity (stars), altitude above sea level , UNESCO recognition status can be found in under key called stats, finally species live in there are been classified based on  specie name, picture, class(mammal,reptile,bird,etc.,), endangered status can be found in keyword species.
![image](https://github.com/vinaynv3/Natural-Wonders/blob/master/src/static/naturalwonders.jpg)
<img src="./src/static/species.jpg " alt="InfiniteGraph Logo" width="960" height="330">

## Table of Contents
1. [Docs](#docs)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [FinalWords](#finalwords)

### Docs
***
APIs documentation details, see  [natural_wonders_docs](http://vinaynv3.pythonanywhere.com/)
#### Code Snippet - Shell
```
curl -request GET --url https://vinaynv3.pythonanywhere.com/locations/
```
Note: if you see any redirection issues, please endpoint has a ```/``` trailing slash. It’s similar to a folder in a file system. 
#### API Schema
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
app installation steps. 
```
$ git clone https://github.com/vinaynv3/Natural-Wonders.git
$ cd ../path/to/the/file
$ python3 -m venv <name_of_virtualenv>
$ pip install -r requirements.txt
$ cd app/scripts
$ bash db_setup.sh    #intialize database
$ bash dev_server.sh  #starts flask development server
```
Side information: To start the application  use ```flask run``` if you see any issue, verify ```FLASK_APP``` variable ```export FLASK_APP=<app_name>```
## FinalWords
***
I built this for eductional purpose, if you see any issues,let me know or any feedback would be appreciated, finally I value keeping my site open source, yes, you can use this code.
