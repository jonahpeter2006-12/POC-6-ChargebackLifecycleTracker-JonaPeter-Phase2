FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

ENV NEXT_PUBLIC_API_URL=https://poc6-chargeback-backend.onrender.com

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]