FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy dependency files first
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy Vue source code
COPY . .

# Vite default port
EXPOSE 5173

# Start Vue dev server
CMD ["npm", "run", "dev", "--", "--host"]
