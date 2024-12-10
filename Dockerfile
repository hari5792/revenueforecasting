# # Step 1: Use an official Python runtime as the base image
# FROM python:3.10-slim

# # Step 2: Set the working directory in the container
# WORKDIR /app

# # Step 3: Copy the current directory contents into the container
# COPY . /app

# # Step 4: Install the required dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Step 5: Expose port 8501 for Streamlit (default Streamlit port)
# EXPOSE 8501

# # Step 6: Command to run the Streamlit app
# CMD ["streamlit", "run", "streamlit.py", "--server.headless=true", "--server.port=8501"]

# Use the official Streamlit image or your base image
FROM python:3.9-slim

# Install dependencies (if needed)
RUN pip install streamlit

# Copy your Streamlit app
COPY . /app
WORKDIR /app

# Expose the Streamlit port
EXPOSE 8501

# Run your Streamlit app with custom address and port
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]

