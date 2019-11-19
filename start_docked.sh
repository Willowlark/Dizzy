#! /bin/bash
docker build --tag=dizzy:latest .
docker run -it -v /Volumes/Files/DizzyHoG/:/Dizzy/DizzyHoG dizzy:latest
# docker tag dizzy:latest willowlark/dizzy:latest
# docker push willowlark/dizzy:latest