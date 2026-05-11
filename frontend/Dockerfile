# Stage 1: Build the React application
# We use an official Node.js image. The 'alpine' tag means it's lightweight.
# We name this stage 'build' so we can refer to it later.
FROM node:18-alpine AS build

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker's cache.
# If these files don't change, Docker won't need to re-run 'npm install'.
COPY package*.json ./

# Install all project dependencies
RUN npm install

# Copy the rest of your application's source code
COPY . .

# Build the React app for production, creating an optimized 'dist' folder
RUN npm run build

# ---

# Stage 2: Serve the static files with a lightweight Nginx server
FROM nginx:1.25-alpine

# Copy the build output (the 'dist' folder) from the 'build' stage
# into the Nginx directory for serving static files.
COPY --from=build /app/dist /usr/share/nginx/html

# Copy your custom Nginx configuration to tell the server how to handle requests
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 to allow traffic to the container
EXPOSE 80

# The command to start the Nginx server when the container launches
CMD ["nginx", "-g", "daemon off;"]

