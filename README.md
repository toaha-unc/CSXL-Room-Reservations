# 🏢 CSXL Room Reservations

A full-stack room reservation system built for the [Computer Science eXperience Lab (CSXL)](https://csxl.unc.edu) at the University of North Carolina. This project provides students and faculty with a simple, reliable way to reserve available lab rooms via a responsive web interface.

## 🔧 Tech Stack

- **Frontend:** Angular with Angular Material UI  
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL

---

## 🚀 Features

- 📅 **Room Reservation Interface**  
  Clean and intuitive Angular Material UI design for browsing and booking available lab rooms.

- ⚡ **High-Performance Backend**  
  FastAPI enables fast, scalable, and asynchronous handling of reservation requests.

- 🗃️ **Persistent Data Management**  
  PostgreSQL ensures reliable storage and efficient querying of room availability and reservations.

---

## 🛠️ Getting Started

### Prerequisites

- Node.js & Angular CLI
- Python 3.9+
- PostgreSQL

### Clone the Repository

```bash
git clone https://github.com/toaha-unc/CSXL-Room-Reservations
cd csxl-room-reservations
```

### Frontend Setup

```bash
cd frontend
npm install
ng serve
```

### Backend Setup

```bash
cd backend
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Database Setup

Ensure PostgreSQL is running and update your connection string in `backend/config.py`.

```sql
CREATE DATABASE csxl_reservations;
```

Run migrations (if applicable) to create tables.

---

## 🤝 Contributing

Contributions, suggestions, and feedback are welcome!  
Feel free to open issues or submit pull requests.

---

## 📄 License

MIT License
