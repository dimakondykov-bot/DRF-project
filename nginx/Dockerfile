FROM nginx:latest

RUN mkdir -p /app/staticfiles /app/mediafiles

COPY nginx.conf /etc/nginx/nginx.conf

RUN chown -R nginx:nginx /app/staticfiles /app/mediafiles

EXPOSE 80
