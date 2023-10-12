FROM node:14.21.3-alpine
WORKDIR /erpigram/
COPY public/ /erpigram/public
COPY src/ /erpigram/src
COPY package.json /erpigram/
RUN npm install
CMD ["npm", "start"]
