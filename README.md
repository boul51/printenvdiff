# About this script

This script was written to extract the environment variables set by a script under the form:

    VAR_NAME=SOME_VALUE

It was developed to work with QtCreator and Yocto.  
Indeed, Yocto generates a bash script that needs to be called before starting QtCreator.  
This is painful because you need to restart QtCreator to build for a different target (eg PC).  
Instead, you can set the environment variables directly in QtCreator kit environment variables,  
but it is not always easy to extract the environment variables from the Yocto script.

Instead, this script sources the Yocto script, and generates a diff of the environment variables  
under a key value form, which can be directly copied-pasted to QtCreator kits settings.

This could also be useful in some situations where you want to have a summary of the environment  
variables modified by a script.

# Invokation

Example:

    ./printenvdiff.py --script /opt/poky/1.6.2/environment-setup-cortexa9hf-vfp-neon-poky-linux-gnueabi

Partial sample output:

    AR=arm-poky-linux-gnueabi-ar
    ARCH=arm
    AS=arm-poky-linux-gnueabi-as

## Options

### --no-compound

By default, the script tries to compose the new environment variables from the old ones.  
For instance, if the old PATH is ```/usr/bin```and the new PATH is ```/usr/local/bin:/usr/bin```,
the script will output:

    PATH=/usr/local/bin:${PATH}

The ```--no-compound``` option disables this feature. In the previous example, the script would output:

    PATH=/usr/local/bin:/usr/bin
