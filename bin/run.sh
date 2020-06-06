#! /bin/bash
ln -s /Volumes/Files/DizzyHoG DizzyHoG
docker run -it -v /Volumes/Files/DizzyHoG/:/Dizzy/DizzyHoG dizzy:latest