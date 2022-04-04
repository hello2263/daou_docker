FROM nginx:stable

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./conf.d/nginx-prom.conf /etc/nginx/conf.d/nginx-prom.conf

CMD ["nginx", "-g", "daemon off;"]
