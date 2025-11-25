# Alcohol Label Checker

A full-stack web app using OCR (AI) to verify alcohol label images against TTB-style form inputs.

## Features

- Upload a label image (e.g. whiskey bottle label)
- Enter key product details (Brand, Type, ABV, Volume)
- AI (OCR) extracts text and compares with form
- Results shown with match/fail per field

---

## Tech Stack

- **Frontend**: React + Tailwind CSS
- **Backend**: Flask + pytesseract
- **OCR**: Tesseract OCR (local)
- **Deployment**: Vercel (frontend), Render/Fly.io (backend)

---

## Getting Started

### Backend Setup (Flask + OCR)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py