# Start from Node alpine.
FROM node:alpine AS build

# Copy the app directory to container.
COPY ./app /app/

# Set working directory in container to app.
WORKDIR /app

# Install all required packages, then run build. This will generate a
# production ready build in frontend/app/build/, which we have mapped
# to /var/www/html via volumes for both the frontend app & the nginx
# service.
RUN npm install
RUN npm run build

# Next stage; Alpine nginx.
FROM nginx:alpine AS web

# Copy the built React app into web root.
COPY --from=build /app/build /var/www/html

# Delete default Nginx configuration.
RUN rm /etc/nginx/conf.d/default.conf

# Copy our config to container, under a template name.
COPY ./conf.d/csb.conf /etc/nginx/conf.d/csb.conf.template

# Copy snippets to container.
COPY ./snippets/ /etc/nginx/snippets/

# Expose 80, we'd also expose 443 but we don't support that in
# this project at the moment.
EXPOSE 80

# Copy the start script to container and assign permissions.
COPY ./scripts/start-nginx.sh /usr/local/bin/start-nginx.sh
RUN chmod +x /usr/local/bin/start-nginx.sh

# Set command to the start script.
CMD [ "/usr/local/bin/start-nginx.sh" ]