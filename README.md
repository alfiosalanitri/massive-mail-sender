# Massive Mail Sender

This is a Flask-based web application that allows users to send personalized HTML emails to one or multiple recipients. The app features a secure login page with password authentication and a user-friendly interface for composing emails. Users can input email addresses in a textarea, specify the subject, and customize the HTML body of the email.

## Build and Run the Application

### Prerequisites
- Ensure you have **Docker** installed on your machine.
- Clone this repository and navigate to its root directory.

### Steps to Build and Run the Docker Image

1. **Set up the Environment Variables**  
   Create a `.env` file in the root directory using the provided `.env.example` file. Populate it with the necessary values:
   ```bash
   cp .env.example .env
   ```

2. **Build the Docker Image**  
   Run the following command to build the Docker image:
   ```bash
   docker build -t massive-mail-sender .
   ```

3. **Run the Docker Container**  
   Start the application container with the following command:
   ```bash
   docker run -p 5000:5000 --env-file .env massive-mail-sender
   ```

   - The `--env-file` flag ensures that the environment variables from your `.env` file are loaded into the container.

4. **Access the Application**  
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

   You will be presented with the login screen. Use the password specified in the `.env` file to log in.

### Development Notes
- The application listens on port **5000**. If this port is already in use, modify the `docker run` command to map to a different port (e.g., `-p 8080:5000`).
- To rebuild the image after changes, use:
  ```bash
  docker build --no-cache -t massive-mail-sender .
  ```

### Troubleshooting
- Ensure all necessary environment variables are correctly set in the `.env` file.
- If emails are not being sent, double-check your SMTP settings in the `.env` file.

### Use the Prebuilt Docker Image

If you prefer not to build the image locally, you can use the prebuilt image from Docker Hub. 

1. **Pull the Prebuilt Image**  
   Download the image from Docker Hub by running:
   ```bash
   docker pull alfiosalanitri/massive-mail-sender
   ```

2. **Run the Container**  
   Start the container using the prebuilt image:
   ```bash
   docker run -p 5000:5000 --env-file .env alfiosalanitri/massive-mail-sender
   ```
   or with Docker Compose
   ```
    services:
        app:
            image: alfiosalanitri/massive-mail-sender
            ports:
            - "7000:5000"
            environment:
            - LOGIN_PASSWORD=1234
            - SMTP_SERVER=smtp.example.com
            - SMTP_PORT=587
            - SMTP_USER=user@example.com
            - SMTP_PASSWORD=your_password
            - MAIL_FROM=user@example.com
   ```

3. **Access the Application**  
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

This method skips the build step and allows you to quickly deploy the application!

Enjoy sending massive emails efficiently! 🚀