# Personal Finance Tracker+

A full-stack web application that helps users manage expenses, set monthly budgets, view dashboards, and receive smart suggestions to improve financial habits.

## 🔧 Features
- User authentication (signup/login)
- Expense management (add, edit, delete, filter, search)
- Budget limits per category with alerts
- Dashboard with pie and line charts
- Smart suggestions using Python (Flask + Pandas)
- Monthly reports stored in PostgreSQL

---

## 🖥️ Tech Stack
- **Frontend:** Next.js (App Router) + TailwindCSS
- **Backend:** Node.js + Express
- **Database:** MongoDB (primary), PostgreSQL (reports)
- **Charts:** recharts
- **AI Service:** Python Flask + Pandas

---

## 🚀 Project Structure
See full structure in the project folder.

---

## 🧪 Test Credentials
```bash
Email: abhay0701@gmail.com
Password: 12345
```

---

## 🛠️ How to Run Locally

### Backend (Express API)
```bash
cd backend
cp .env.example .env
npm install
npm start
```

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

### Python Service (Flask)
```bash
cd python-service
pyhton -m venv venv
venv/scripts/activate/
pip install -r requirements.txt
python app.py
```

### SQL Reports
```
This is handled by python services
```

---

## 🌐 Deployment
- **Frontend:** Render
- **Backend + Flask:** Render

---

## 📁 Environment Variables

### `.env.example` (backend)
```env
MONGO_URI=
JWT_SECRET=your_jwt_secret
PORT=5000
```

### `.env.local` (frontend)
```env
NEXT_PUBLIC_API_BASE=http://localhost:5000
NEXT_PUBLIC_ANALYTICS=http://localhost:5001
```

### `python-service` require .env 
```
POSTGRES_HOST=
POSTGRES_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=
EXPRESS_API=http://localhost:5000
JWT_SECRET=your_jwt_secret
```

---

## 📊 Extra Features
- Alerts at 80% and 100% of budget
- Chart visualizations for spending
- AI-driven savings suggestions

---

## 📹 Demo + Submission
- [Live Demo URL](https://personalfinancetracker-y5w6.onrender.com/))
- [GitHub Repository](https://github.com/abhaystd)

---

Built with ❤️ for the AB YA
