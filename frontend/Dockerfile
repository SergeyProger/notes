FROM node:20-alpine

WORKDIR /app

# First copy only the dependency files so the layer can be cached
COPY package*.json ./

RUN npm install

# Copy the rest of the code
COPY . .

EXPOSE 5173

# Run Vite with the --host flag so the server is reachable from outside the container
CMD ["npm", "run", "dev", "--", "--host"]