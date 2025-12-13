FROM python:3.10-slim

# Update and install all dependencies in one layer (reduces image size)
RUN apt update && apt upgrade -y && \
    apt-get install -y \
    git \
    curl \
    wget \
    python3-pip \
    ffmpeg \
    bash \
    software-properties-common \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Try to install neofetch if available (optional)
RUN apt update && apt-get install -y neofetch 2>/dev/null || echo "Neofetch not available, skipping"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip wheel && \
    pip3 install --no-cache-dir -r requirements.txt

# Set working directory and copy application code
WORKDIR /app
COPY . .

# Expose port
EXPOSE 8000

# Run both Flask and your devgagan module
CMD flask run -h 0.0.0.0 -p 8000 & python3 -m devgagan
