## Install libwebkitgtk

    sudo nano /etc/apt/sources.list
    Add this entry to the file and save:

    deb http://cz.archive.ubuntu.com/ubuntu bionic main universe

    sudo apt-get update

    sudo apt-get install libwebkitgtk-1.0-0 -> if you are using Vega and jdk of 64 bits

    sudo apt-get install libwebkitgtk-1.0-0:i386 -> if you are using Vega and jdk of 32 bits

## Install pentaho PDI ce
    https://sourceforge.net/projects/pentaho/

## Run PDI
    cd pdi-ce-9.3.0.0-428/data-integration
    sh spoon.sh