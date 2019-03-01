FROM nginx

COPY nginx.conf /home/nginx/nginx.conf.template

CMD /bin/bash -c "envsubst '\$PORT' < /home/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'" 
