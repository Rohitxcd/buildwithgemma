# 🛡️  VideoLock
<div align="center">

### **Protect Before They Clone.**

An AI-powered preventive media protection platform that safeguards images and videos **before** they can be exploited by face-swapping, deepfake generation, identity cloning, or AI manipulation.

Built with **FastAPI**, **Next.js**, **Gemma**, **MediaPipe Face Mesh**, and **OpenCV**.

</div>

---

## ✨ Features

- 🧠 **Gemma Vision Analysis** – Understands the uploaded media and assesses identity exposure.

- 🎯 **Adaptive Protection Strategy** – Selects the most effective protection pipeline based on risk.

- 👤 **Facial Landmark Protection** – Protects facial geometry against downstream face-swapping models.

- 🌊 **Frequency-aware Defense** – Applies imperceptible perturbations in the frequency domain.

- 🎨 **Texture-aware Protection** – Preserves visual quality while disrupting learned identity features.

- 🔍 **Protection Verification** – Re-evaluates protected media to measure remaining identity leakage.

- 📊 **AI-generated Protection Report** – Explains the protection strategy and confidence.

- ⚡ **Modern Web Dashboard** – Built with Next.js and Tailwind CSS.

---

# 📋 Prerequisites

- Python **3.11+**

- Node.js **18+**

- Git

---

# 📥 Clone the Repository

```bash

git clone https://github.com/Rohitxcd/buildwithgemma.git

cd buildwithgemma

```

---

# ⚙️ Backend Setup

## 📂 Step 1 — Navigate to Backend

```bash

cd backend

```

## 🐍 Step 2 — Create Virtual Environment

### Windows

```bash

python -m venv .venv

```

### Linux / macOS

```bash

python3 -m venv .venv

```

---

## ▶️ Step 3 — Activate Virtual Environment

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

## 📦 Step 4 — Install Dependencies

```bash

pip install -r requirements.txt

```

---

## 🔑 Step 5 — Configure Environment Variables

Create a `.env` file inside the **backend** directory.

```env

GEMMA_API_KEY=YOUR_API_KEY

```

---

## 🚀 Step 6 — Start the Backend Server

```bash

uvicorn app.main:app --reload

```

Backend:

```

http://127.0.0.1:8000

```

API Documentation:

```

http://127.0.0.1:8000/docs

```

---

# 💻 Frontend Setup

Open a new terminal.

```bash

cd frontend

```

Install dependencies:

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

# 🛠️ Tech Stack

| Category | Technology |

|-----------|------------|

| Backend | FastAPI |

| Frontend | Next.js |

| AI Reasoning | Gemma |

| Computer Vision | MediaPipe Face Mesh |

| Image Processing | OpenCV |

| Numerical Computing | NumPy |

| Styling | Tailwind CSS |

---

# 📁 Project Structure

```text

buildwithgemma/

│

├── backend/

│   ├── app/

│   ├── requirements.txt

│   └── .env

│

└── frontend/

```

---

# ▶️ Running the Project

### Start Backend

```bash

cd backend

uvicorn app.main:app --reload

```

### Start Frontend

```bash

cd frontend

npm run dev

```

---

<div align="center">

## 🛡️ Aegis

### **Protect Before They Clone.**

**AI-powered identity protection for the generative era.**

Built with ❤️ using **FastAPI • Next.js • Gemma • MediaPipe • OpenCV**

</div>
