# syntax=docker/dockerfile:1.4
FROM node:20.10.0 AS builder

WORKDIR /code
COPY package.json package-lock.json /code/
RUN npm install

COPY . .
EXPOSE 3000

CMD ["npm", "run", "dev"]
