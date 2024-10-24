#!/bin/bash

# Used with Boomerang / kaniko flags to selectively build routes into a container. Ex:
# build-container-kaniko-flags=--build-arg "APP_LIST=docbuilder health wikipedia"

# set default value if variable is set but empty
if [ -z "$APP_LIST" ]; then
    APP_LIST='all'
fi

# copy only the selected app routes
if [ "$APP_LIST" != all ]; then
   mv ./app/routes ./app/tmp
   mkdir ./app/routes
   for app in $APP_LIST; do
        find ./app/tmp -mindepth 1 -type d -name "$app" -exec cp -r {} ./app/routes \;;
   done
   rm -fr ./app/tmp
fi
