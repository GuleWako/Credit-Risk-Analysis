# Step 1: Build the React app
FROM node:18 AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app files
COPY . .

# Build the app
RUN npm run build

# Step 2: Serve the app using nginx
FROM nginx:alpine

# Copy the build folder from the build stage
COPY --from=build app/dist /usr/share/nginx/html

# Expose port 400 to access the app
EXPOSE 4000

# Start nginx server
CMD ["nginx", "-g", "daemon off;"]
