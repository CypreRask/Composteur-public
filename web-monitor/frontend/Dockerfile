# Stage 1: Build
FROM node:20-alpine as build

WORKDIR /app

COPY package.json ./
# Remove lockfile to force fresh install for Linux (avoid Windows binary issues)
RUN rm -f package-lock.json
RUN npm install

COPY . .
# Build Svelte/Vite App with verbose logging
RUN npm run build -- --debug

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy built assets from builder stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom Nginx config (Reverse Proxy)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
