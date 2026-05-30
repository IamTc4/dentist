# DentaFlow AI Backend

This is the FastAPI backend serving the DentaFlow AI frontend and handling demo requests.

## Setup Instructions

1. Make sure Python 3 is installed.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the backend server:
   ```bash
   python main.py
   ```
4. Access the web application at `http://localhost:8000`.

## Features
- **Frontend Serving**: The `code.html` landing page is served directly from the root endpoint `/`.
- **Demo Booking API**: A POST endpoint `/api/book-demo` accepts form submissions from the frontend and logs them to the console.
