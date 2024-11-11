# Use an official Node.js runtime as a parent image
FROM node:18

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

RUN ln -s /usr/bin/python3 /usr/bin/python

# Install OR-Tools using pip
RUN pip3 install --no-cache-dir --break-system-packages ortools

# Set the working directory for the application
WORKDIR /app

# Copy package.json and package-lock.json for the Express application
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the Express app will run on
EXPOSE 3000

# Start the Express application
CMD ["npm", "start"]