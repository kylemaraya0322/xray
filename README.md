# X-ray Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

A Django-based web application for managing patients, employees, and AI-powered chest X-ray diagnosis (PTB vs Normal). Built with Django 5.2, Tailwind CSS, and Ultralytics YOLOv11 for inference.

---

## 🚀 Features

- **Patient CRUD**: Manage patients using a single-template modal interface.
- **Employee Management**: CRUD operations for employees with image upload and zero-padded employee IDs.
- **AI Diagnosis**: Upload chest X-rays, run YOLOv11 inference, and update patient records.
- **Live Dashboards**: Real-time metrics and auto-refresh via AJAX for admin and staff dashboards.
- **Dark Theme**: Consistent dark-mode UI using Tailwind CSS.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.13, Django 5.2
- **Frontend**: Tailwind CSS, Font Awesome, Chart.js
- **AI**: PyTorch, torchvision, Ultralytics YOLOv11, PIL
- **Database**: SQLite (default) or PostgreSQL/MySQL (configurable)
- **Storage**: Local `MEDIA_ROOT` for uploads

---

## 📋 Prerequisites

- Python 3.13+
- Git
- (Optional) CUDA-enabled GPU for faster inference

---

## ⚙️ Installation

1. **Clone the repo**

```bash
git clone https://github.com/YourUsername/your-repo.git
cd your-repo
```

2. **Create & activate a virtual environment**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install Python dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Place your YOLOv11 weights**

Create a folder `ml_models/` in the project root and copy your trained weights `best.pt`:

```plaintext
your-repo/
├── ml_models/
│   └── best.pt
└── manage.py
```

5. **Configure settings.py**

Make sure these are included:

```python
INSTALLED_APPS = [
    # ... other apps ...
    'patient',
    'employee',
    'diagnosis',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

6. **Database Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

If adding models in a specific app:

```bash
python manage.py makemigrations diagnosis
```

7. **Create a Superuser**

```bash
python manage.py createsuperuser
```

Follow the prompts to set your admin credentials.

---

## ▶️ Running the Development Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and navigate:

- Patients → `/patients/`
- Employees → `/employees/`
- AI Diagnosis → `/diagnosis/`
- Admin Dashboard → `/admin/dashboard/`
- Staff Dashboard → `/staff/dashboard/`

---

## 💡 How It Works

- **Patient & Employee CRUD**: Single modals on their respective index pages.
- **AI Diagnosis**: Upload X-ray in modal → View calls `run_ai_model()` in `diagnosis/ml.py` → YOLOv11 loads `ml_models/best.pt` → Outputs "PTB" or "Normal" → Updates the patient's diagnosis.
- **Dashboards**: Poll JSON APIs (`/stats/`) every 30 seconds to auto-refresh metrics.

---

## 🛠️ Contributing

1. Fork this repository.
2. Create a feature branch:

```bash
git checkout -b feature/YourFeature
```

3. Commit your changes:

```bash
git commit -m "Add awesome feature"
```

4. Push to your fork:

```bash
git push origin feature/YourFeature
```

5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

- GitHub: [@kylemaraya0322](https://github.com/kylemaraya0322)
- Email: kylemaraya0322@gmail.com

---

