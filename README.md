# CV-Shortlister-Backend

This is a Django project named "cv-shortlister". It includes [brief description of what the project does or its purpose].

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your local machine
- pip package manager installed
- Git installed (optional, if you want to clone the project repository)

## Getting Started

To set up this project locally, follow these steps:

1. Clone the repository to your local machine (if you haven't already):

   ```bash
   git clone https://github.com/AakibAlam/cv-shortlister-backend.git
   ```

2. Navigate to the project directory:

   ```bash
   cd cv-shortlister-backend
   ```

3. Create a virtual environment to isolate project dependencies:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - **Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - **Linux/macOS**:

     ```bash
     source venv/bin/activate
     ```

5. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Set up environment variables:

   - Create a `.env` file inside the project api directory.
   - Add the required environment variables to the `.env` file. For example:

     ```plaintext
     API_KEY="GEMINI_API_KEY"
     ```

## Running the Development Server

To start the development server, run the following command:

```bash
python manage.py runserver
```

Please utilize Postman or any other application designed for making HTTP requests. Subsequently, initiate a POST request using the following URL: http://localhost:8000/submit/. Ensure to include the PDF files within the request body, specifying the key name as "resume".

An example of request:
<img src="https://github.com/AakibAlam/cv-shortlister-backend/blob/main/example-request.png" align="center" width="100%"/>

## Frontend Part of this project

Github Repo: https://github.com/AakibAlam/cv-shortlister-frontend/

Deployed Link: https://parse.cvninja.studio/
