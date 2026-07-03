# ---------- Stage 1 : build du React avec Node 20 ----------
FROM node:20-slim AS build

WORKDIR /app

# Cache Docker : on installe les deps avant de copier le code
COPY package*.json ./
RUN npm ci

# Copier le reste et builder
COPY . .
RUN npm run build

# ---------- Stage 2 : servir le dist/ avec nginx ----------
FROM nginx:alpine

# Copier le build depuis le stage précédent
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
