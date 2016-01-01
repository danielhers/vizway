VIZWAY
======
This is a project for the [DataHack hackathon](http://datahack-il.com).
We are working with the data from the [ANYWAY project](https://github.com/hasadna/anyway).

The website presents accidents density according to cities is israel.
There is a color scale (between rad and orange) which indicates the amount of severe accidents as a fraction of all of the accidents.

# Dependencies
`matplotlib` requires `libpng` and `freetype`. If you are on Ubuntu Linux, install them by:

    sudo apt-get install libpng12-dev libfreetype6-dev

# Running
Download the [complete accidents file](https://drive.google.com/file/d/0B4yX8HDe1VaTdWdPMXV5c2gycW8/view?usp=sharing) and extract into `static/data/lms`. Then run:

    pip install -r requirements.txt
    python server.py

Wait until the markers finished loading, and then navigate to <http://localhost:8000>.

# Members
* Idit Minka
* Inbal Levi
* Dan Ofer
* Amos Sidelnik
* Daniel Hershcovich
