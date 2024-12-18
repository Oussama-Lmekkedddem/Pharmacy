FROM node:18 AS build

WORKDIR /app

COPY client/package*.json ./

RUN npm install

COPY client/ /app/

RUN npm run build --configuration=production

RUN npm install -g http-server

EXPOSE 4200

CMD ["http-server", "dist/client/browser", "-p", "4200", "--host", "0.0.0.0"]


# ng new client --strict --style=css --routing