# VideoLock

AI-powered preventive media protection platform built using FastAPI, Next.js, MediaPipe Face Mesh, OpenCV, and Gemma.

---

## Prerequisites

* Python 3.11+
* Node.js 18+
* Git

---

# Clone the Repository

```bash
git clone https://github.com/Rohitxcd/buildwithgemma.git
cd buildwithgemma
```

---

# Backend Setup

## 1. Go to the backend

```bash
cd backend
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
```

### Linux / macOS

```bash
python3 -m venv .venv
```

---

## 3. Activate the virtual environment

### Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows (CMD)

```cmd
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Configure environment variables

Create a file named `.env` inside the `backend` folder.

```env
GEMMA_API_KEY=YOUR_API_KEY
```

---

## 6. Run the backend server

```bash
uvicorn app.main:app --reload
```

The backend will start at:

```
http://127.0.0.1:8000
```

Swagger API documentation:

```
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

Open a new terminal.

```bash
cd frontend
```

Install packages:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Frontend:

```
http://localhost:3000
```

---

# Tech Stack

* FastAPI
* Next.js
* MediaPipe Face Mesh
* OpenCV
* NumPy
* Gemma
* Tailwind CSS

---

# Project Structure

```
buildwithgemma/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── .env
│
└── frontend/
```
