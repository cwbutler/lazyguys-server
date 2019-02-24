FROM nginx

COPY default.conf.template /etc/nginx/conf.d/app.conf.template
COPY nginx.conf /etc/nginx/conf.d/default.conf

CMD /bin/bash -c "envsubst '\$PORT' < /etc/nginx/conf.d/app.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'" 
