FROM nginx

COPY nginx.conf /nginx.conf.template

CMD /bin/bash -c "envsubst '\$APP_PORT' < /nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'" 
