# use latest python alphine image.
FROM python:rc-alpine3.12

# install system dependencies.
RUN apk update && apk add --no-cache \
  graphviz bash ttf-opensans curl fontconfig

# install fonts
RUN curl -O https://noto-website.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip \
&& mkdir -p /usr/share/fonts/NotoSansCJKjp \
&& unzip NotoSansCJKjp-hinted.zip -d /usr/share/fonts/NotoSansCJKjp/ \
&& rm NotoSansCJKjp-hinted.zip \
&& fc-cache -fv

RUN pip3 install graphviz
RUN pip3 install flask

# define required environment variable
ENV HOME=/opt/app-root PYTHONUNBUFFERED=true

# add you application artifact(s) and entrypoint script
# for interpreted languages like python, there is no build step and artifact is the source code itself
COPY . ${HOME}/
#RUN mkdir -p ${HOME}/diagrams
#ADD diagrams ${HOME}/diagrams
#RUN mkdir -p ${HOME}/resources
#ADD resources ${HOME}/resources
#RUN mkdir -p ${HOME}/webserver
#ADD webserver ${HOME}/webserver
#ADD templates/* ${HOME}/templates

#RUN mkdir -p ${HOME}/static
#ADD static/* ${HOME}/static/

RUN chown -R 1001:1001 ${HOME}

# set the image working directory and user - other than root/0
WORKDIR ${HOME}
USER 1001

RUN export PYTHONPATH=.

# define the starting command: calling 'sh run.sh'' instead of just 'run.sh' is a good habit that prevent you from setting x right to run.sh
CMD ["sh", "/opt/app-root/webserver/run-server.sh"]

