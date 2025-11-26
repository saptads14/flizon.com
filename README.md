# 🛒 FLIZON – E-Commerce Web Application

FLIZON is a clean, responsive, and modern e-commerce web application designed to deliver a seamless online shopping experience. It includes all essential online store features such as product browsing, category filtering, authentication, cart, wishlist, checkout, and an admin control panel for product management.

---

## 🚀 Features

### ✅ User Features
- **User Authentication**  
  - Sign Up, Login, Logout
  - Forgot/Reset Password  
- **Product Browsing**  
  - Category-based filtering (Fashion, Electronics, Furniture, etc.)  
  - Detailed product view with clean UI  
- **Add to Wishlist**  
- **Add to Cart**  
- **Dummy Checkout Process**   
- **Fully Responsive UI with animations**  

### ⚙️ Admin Features
- Add / Edit / Delete Products  
- Category Management   
- Admin Dashboard  

---

## 🛠️ Tech Stack

<p align="left">
  <img src="https://skillicons.dev/icons?i=python" height="50" />
  <img src="https://skillicons.dev/icons?i=django" height="50" />
  <img src="https://skillicons.dev/icons?i=html" height="50" />
  <img src="https://skillicons.dev/icons?i=css" height="50" />
  <img src="https://skillicons.dev/icons?i=javascript" height="50" />
  <img src="https://skillicons.dev/icons?i=vscode" height="50" />
  <img src="https://skillicons.dev/icons?i=git" height="50" />
  <img src="https://skillicons.dev/icons?i=github" height="50" />
  <img src="https://skillicons.dev/icons?i=sqlite" height="50" />
</p>

---

## 🎯 Outcome
A complete, feature-rich e-commerce platform that replicates real-world online store functionality using a modern responsive interface and smooth navigation.

---

## 📂 Directory Structure
```bash
ecommerce_store/
├─ ecommerce_store/        # Project package (settings, urls, wsgi, asgi)
├─ store/                  # Main ecommerce app
│   ├─ management/
│   ├─ migrations/
│   ├─ templates/store/
│   ├─ templatetags/
│   ├─ models.py
│   ├─ views.py
│   ├─ urls.py
│   ├─ forms.py
│   └─ context_processors.py
├─ static/                 # CSS, JS, images
├─ media/                  # Uploaded files
├─ db.sqlite3
├─ manage.py
└─ requirements.txt
```
---

## 💻 Setup & Installation Guide
  - Follow the steps below to set up the project locally.

1️⃣ Clone the Repository
```bash
git clone https://github.com/saptads14/flizon.com.git
cd flizon.com
```
2️⃣ Create & Activate Virtual Environment
```bash
# Create virtual environment (windows)
python -m venv .venv
.venv\Scripts\activate

# Create virtual environment (Linux/macOS)
python3 -m venv .venv
source .venv/bin/activate
```
3️⃣ Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
4️⃣ Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
5️⃣ Create Superuser
```bash
python manage.py createsuperuser
```
6️⃣ Collect Static Files (Optional/Production)
```bash
python manage.py collectstatic --noinput
```
7️⃣ Run Django Server
```bash
python manage.py runserver 0.0.0.0:8000
```
## Now visit:
```bash
# Frontend:
http://127.0.0.1:8000
# Admin Panel:
http://127.0.0.1:8000/admin
```
---

## 📄 License
This project is licensed for Educational and Learning Purposes Only.
You may use, modify, and study the code freely for personal or academic projects.
Commercial use, redistribution, or selling of this project is not permitted.

---

---

## 👋 Connect With Me

- **GitHub:** https://github.com/saptads14  
- **LinkedIn:** https://www.linkedin.com/in/saptadeep-halder04/
- **Email:** saptadeephalder2004@gmail.com 

---

## 💬 Suggestions or Feedback?

⭐ Feel free to open an **Issue** or create a **Pull Request**.  
💡 Your suggestions are always welcome — it helps make FLIZON better!

---

## 🙏 Thank You for Visiting!
**Saptadeep (saptads14)**  
