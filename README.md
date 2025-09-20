# Activity Tracker 🕒  

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Django](https://img.shields.io/badge/Django-4.0%2B-green)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

A web application built with **Django** that helps users track their daily activities such as **study, sports, movies, reading, and more**. The app allows you to log time, analyze productivity, and visualize how your day is spent.  

---

## 🚀 Features  

- User authentication (signup, login, logout).  
- Add, edit, and delete activities.  
- Categorized activities (Study, Sports/Gym, Movies, Reading, etc.).  
- Track sources (e.g., Books, Online Courses, Videos).  
- Activity triggers (e.g., Interest, Exam Prep, Fitness Goal).  
- Dashboard with **time visualization and productivity analysis**.  
- Mobile-friendly responsive UI.  

---

## 🛠️ Tech Stack  

- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, JavaScript (with responsive design)  
- **Database:** SQLite (default, can be changed to PostgreSQL/MySQL)  
- **Other tools:** Django ORM, Bootstrap/Tailwind (if used)  

---

## 📂 Project Setup  

Follow these steps to run the project locally:  

```bash
# 1. Clone the repository
git clone https://github.com/raaz2507/activityTracker-Django.git

# 2. Navigate into the project folder
cd activityTracker-Django

# 3. Create a virtual environment
python -m venv venv

# 4. Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run database migrations
python manage.py migrate

# 7. Create a superuser (admin account)
python manage.py createsuperuser

# 8. Run the development server
python manage.py runserver
```

Now visit `http://127.0.0.1:8000/` in your browser. 🎉  

---

## 📸 Screenshots / Demo  

Here are some previews of the Activity Tracker in action:  

### 🔑 Login / Signup  
![Login Page](screenshots/login.png)  

### 🏠 Dashboard  
![Dashboard](screenshots/dashboard.png)  

### 📊 Activity Tracking  
![Activity Tracking](screenshots/activity-tracking.png)  

*(You can replace these with your actual screenshots or GIFs)*  

---

## 📊 Future Enhancements  

- Add activity reminders & notifications.  
- Graphs & charts for advanced analytics.  
- Social sharing of progress.  
- Integration with Google Calendar.  

---

## 🤝 Contributing  

Contributions are welcome!  
1. Fork the project.  
2. Create your feature branch (`git checkout -b feature-name`).  
3. Commit your changes (`git commit -m 'Add new feature'`).  
4. Push to the branch (`git push origin feature-name`).  
5. Open a pull request.  

For significant changes, please open an issue first to discuss your idea.  

---

## 📜 License  

This project is licensed under the **MIT License** – free to use, modify, and distribute.  

---

## 👨‍💻 Author  

**Raaz**  
- GitHub: [raaz2507](https://github.com/raaz2507)  
