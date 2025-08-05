# TaskNest 🪺

A modern, Flask-based to-do application that makes task management simple, secure, and cloud-native.

[Live Demo](https://tasknest-nw6h.onrender.com) • [GitHub Repo](https://github.com/Monirules/TaskNest) • [Docker Hub](https://hub.docker.com/r/mim9/tasknest)

---

## Features

1. **User Registration & Login**  
   - Secure account creation with unique usernames  
   - Password protection and SQL-injection prevention  
   - Session management via Flask-Login  

2. **Dashboard & Task Management**  
   - Create, update, delete, and mark tasks as done  
   - Assign due dates and view upcoming deadlines  

3. **RESTful API & JWT Support**  
   - Per-user JSON endpoints for tasks at `/api/tasks`  
   - Token issuance (`/token`) for future integrations  

4. **Daily Inspirational Quote**  
   - Fetches a random quote from [Quotable](https://api.quotable.io/random)  

5. **Statistics Page**  
   - Chart.js bar chart showing completed, overdue, pending, and total tasks  

6. **Profile Page**  
   - View your username, user ID, and total task count  

---

## Tech Stack

- **Back-end:** Python 3 · Flask · Flask-Login · Flask-SQLAlchemy  
- **Database:** MySQL (Aiven Managed & Docker container)  
- **Front-end:** Bootstrap 5 · Chart.js · FullCalendar.js  
- **Containerization:** Docker · Docker Compose  
- **CI/CD & Hosting:** Docker Hub · Render.com  

---

## Quickstart

1. **Create & activate a virtual environment, install dependencies and run locally (Visit: http://localhost:5000)**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate    
   pip install -r requirements.txt
   cat > .env <<EOF
   SECRET_KEY=your_secret_key
   DATABASE_URL=mysql://root:root@localhost:3306/todolist_db
   EOF
   flask run


2. **Build, run with Docker Compose, and push to Docker Hub**
  
  docker build -t mim9/tasknest:latest . \
  docker-compose up --build \
  Web app: http://localhost:5000 \
  MySQL: exposes port 3306 (optional: change to 3307 if conflict) \
  docker push mim9/tasknest:latest 

---

## Screenshots 

<img width="1613" height="913" alt="Homepage" src="https://github.com/user-attachments/assets/947e658f-5455-4bda-9b30-deffde1c5113" />
<img width="1359" height="876" alt="Dashboard 1" src="https://github.com/user-attachments/assets/3393a2b2-86ff-4533-9cf3-76f74d4c434c" />
<img width="1360" height="1038" alt="dashboard 2" src="https://github.com/user-attachments/assets/c56bb54e-0e7b-45fb-b945-9fad371880ac" />
<img width="1366" height="620" alt="Profile" src="https://github.com/user-attachments/assets/e2168962-6d74-4c33-aad8-6213f8191f05" />

<img width="1361" height="955" alt="Stats" src="https://github.com/user-attachments/assets/3e2e38e8-050b-4db6-bf39-8515afe29323" />
<img width="1364" height="781" alt="About" src="https://github.com/user-attachments/assets/9c6409bb-f17a-4b29-bba6-717bbcd1841e" />
<img width="1360" height="817" alt="API Page" src="https://github.com/user-attachments/assets/3f94e2e1-ed8c-4d96-8196-b0d6956b0c64" />















