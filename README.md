# Label Verification App - Fullstack (Flask + Tesseract OCR)

This is a Flask-based backend that uses Tesseract OCR to extract and verify product label information. It compares extracted text against user-provided fields such as brand, product type, ABV, and volume.

## Live Demo
- **Frontend (User Interface):** [https://label-verification-c9ret5n6o-na-yangs-projects.vercel.app/](https://label-verification-c9ret5n6o-na-yangs-projects.vercel.app/)
- **Backend API:** Hosted on Render (Dockerized)
---

## Tech Stack
- **Frontend:** React, Vite (Deployed on Vercel)
- **Backend:** Python, Flask (Deployed on Render)
- **OCR Engine:** Tesseract OCR (Running inside a Docker container on Render)
---

## Local Development Setup

If you want to run this project locally on your machine, follow these steps.

### 1. Backend Setup (Flask + Tesseract)

#### Features

- Accepts label image uploads
- Extracts text using Tesseract OCR
- Field validation:
  - Brand name (case-sensitive match)
  - Product type (case-insensitive substring match)
  - ABV (regex-based pattern matching)
  - Volume (optional, regex-based match)
  - Government warning (case-insensitive match)
- Returns match results for each field
- CORS-enabled for frontend integration

#### Requirements

- Python 3.11
- Tesseract OCR installed
- Virtual environment (recommended)

#### Install Tesseract OCR
- **macOS**: `brew install tesseract`
- **Ubuntu**: `sudo apt install tesseract-ocr`
- **Windows**: Download from:  
  https://github.com/tesseract-ocr/tesseract  
  Then set the path in `app.py` if needed:

  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

#### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask app:
   ```bash
   python app.py
   ```

#### Running Tests
```python
pytest -v tests/test_app.py
```

### 2. Frontend Setup (React)
#### Requirements
- Node.js (v16+ recommended)
- npm or yarn

#### Fronend  Setup
1. Create the frontend app using Vite (if not already created):
    ```bash
    npm create vite@latest frontend
    ```
    - When prompted:
      - Project name: `frontend`
      - Select framework: `React`
2. Navigate into the frontend folder:
    ```bash
    cd frontend
    ```

3. Install dependencies:
    ```bash
    npm install
    ```

4. Start the development server:
    ```bash
    npm run dev
    ```

---
## Deployment Architecture
### Backend (Render)
The backend is deployed as a Docker Container on Render because Tesseract OCR requires system-level dependencies (C++ libraries) that cannot be installed in standard serverless environments.

* Dockerfile: Used to install Python slim and tesseract-ocr packages.

### Frontend (Vercel)
The React frontend is a static site deployed on Vercel.

* It communicates with the Render backend via API calls.
* Environment Variable: VITE_API_URL is set in the Vercel Dashboard to point to the Render backend URL.