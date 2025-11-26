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

## 🎯 Outcome
A complete, feature-rich e-commerce platform that replicates real-world online store functionality using a modern responsive interface and smooth navigation.

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
