# 1. Base Image: Use an official lightweight Python image
FROM python:3.11-slim

# 2. Environment Variables:
#    - PYTHONUNBUFFERED: Ensures logs are sent directly to stdout/stderr for Cloud Logging
#    - APP_HOME: Defines the working directory path
#    - PORT: Default port; Cloud Run injects the actual port to use
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV PORT 8080
# Optional: Set default log level if not provided by Cloud Run env var
# ENV LOG_LEVEL INFO
# Optional: Set default app name if not provided by Cloud Run env var
# ENV APP_NAME MyCloudRunChatBot

# 3. Set Working Directory
WORKDIR $APP_HOME

# 4. Install Dependencies:
#    - Copy only the requirements file first to leverage Docker layer caching.
#    - Install dependencies using pip, including gunicorn for production serving.
#    - Use --no-cache-dir to reduce image size.
COPY requirements.txt .
# Ensure gunicorn is included in your requirements.txt or install it separately:
# RUN pip install --no-cache-dir -r requirements.txt gunicorn
# If requirements.txt might not include gunicorn, uncomment the line above
# and comment out the line below.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Application Code:
#    - Copy the rest of your application code into the working directory.
#    - Assumes your Python script is named 'main.py' (adjust if needed).
#    - Assumes requirements.txt is in the same directory as the Dockerfile.
COPY . .

# 6. Expose Port:
#    - Inform Docker that the container listens on the specified port.
#    - Cloud Run uses this information but manages port mapping automatically.
EXPOSE $PORT

# 7. Run Application:
#    - Use gunicorn as the production WSGI server.
#    - Bind to 0.0.0.0 to accept connections from any IP (required by Cloud Run).
#    - Use the $PORT environment variable provided by Cloud Run.
#    - Adjust the number of workers (-w) based on expected load and Cloud Run instance size (e.g., 2-4 is common).
#    - Replace 'main:flask_app' if your Python file or Flask app instance variable is named differently.
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--workers", "2", "main.py"]

