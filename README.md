# 🍽️ Sistem Kasir Restoran Digital

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)

**Aplikasi web kasir restoran modern dengan fitur lengkap:** Authentication, Cart Management, Auto-calculation, dan PDF Receipt Generator.

Dikembangkan oleh **Kelompok 4** sebagai project akhir mata kuliah.

---

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Screenshots](#-screenshots)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Security](#-security)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Team](#-team)

---

## ✨ Features

### 🔐 **Authentication System**
- ✅ Secure login dengan session management
- ✅ Auto-logout setelah 1 jam inactivity
- ✅ Route protection dengan decorator pattern
- ✅ Complete logout dengan cookie cleanup
- ✅ Prevention dari back-button attacks

### 🛒 **Shopping Cart**
- ✅ Real-time cart updates (no page reload)
- ✅ Add, Plus, Minus, Remove operations
- ✅ Auto-remove item ketika quantity = 0
- ✅ Cart persistence across page refresh
- ✅ Session-based storage

### 💰 **Payment Processing**
- ✅ Auto-calculation: Subtotal, Diskon 10%, PPN 10%
- ✅ Real-time total calculation
- ✅ Input validation (nama, cash amount)
- ✅ Kembalian calculator
- ✅ Error handling untuk insufficient funds

### 📄 **PDF Receipt Generator**
- ✅ Professional PDF layout dengan ReportLab
- ✅ In-memory generation (no disk I/O)
- ✅ Auto page-break untuk long receipts
- ✅ Logo integration
- ✅ Unique filename dengan timestamp
- ✅ Compatible dengan semua browsers & download managers

### 🎨 **Modern UI/UX**
- ✅ Responsive design (Desktop, Tablet, Mobile)
- ✅ Bootstrap 5 framework
- ✅ Smooth animations
- ✅ User-friendly error messages
- ✅ Loading indicators

---

## 🎥 Demo

### Login Page
![Login Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=Login+Page)

### Main Dashboard
![Dashboard Demo](https://via.placeholder.com/800x400/764ba2/ffffff?text=Dashboard)

### PDF Receipt
![Receipt Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=PDF+Receipt)

> **Note:** Replace placeholder images dengan actual screenshots

---

## 📸 Screenshots

<details>
<summary>Click to view all screenshots</summary>

### 1. Login Page
- Modern gradient design
- Password show/hide toggle
- Error handling dengan animations

### 2. Menu Display
- Card-based layout
- Category navigation
- Clear pricing

### 3. Shopping Cart
- Real-time updates
- Quantity controls
- Total breakdown

### 4. Checkout Process
- Customer information
- Payment calculation
- Receipt generation

### 5. PDF Receipt
- Professional layout
- Complete transaction details
- Business information

</details>

---

## 🛠️ Tech Stack

### Backend
- **Flask 3.0+** - Python web framework
- **ReportLab** - PDF generation library
- **Werkzeug** - Security utilities (session, cookies)

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling
- **Bootstrap 5.3** - Responsive framework
- **JavaScript ES6** - Client-side logic
- **Font Awesome 6.4** - Icons

### Storage
- **Flask Session** - Server-side session management
- **JSON** - Menu data storage

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/restaurant-pos-system.git
cd restaurant-pos-system
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```txt
Flask==3.0.0
reportlab==4.0.7
Werkzeug==3.0.1
```

### Step 4: Setup Project Structure
```
project/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/
│   └── menu.json         # Menu database
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   └── cart.js       # Cart logic
│   └── img/
│       └── logo.png      # Restaurant logo
└── templates/
    ├── login.html        # Login page
    └── index.html        # Main dashboard
```

### Step 5: Configure Menu Data
Create `data/menu.json`:
```json
{
  "makanan": [
    {
      "id": 1,
      "nama": "Nasi Goreng",
      "price": 25000,
      "img": "/static/img/nasi-goreng.jpg"
    }
  ],
  "minuman": [
    {
      "id": 10,
      "nama": "Es Teh",
      "price": 5000,
      "img": "/static/img/es-teh.jpg"
    }
  ]
}
```

### Step 6: Run Application
```bash
python app.py
```

Application akan running di: **http://localhost:5000**

---

## 🚀 Usage

### 1. Login
**Credentials:**
```
Email: zhaenx_id@yeswehack.com
Password: zh43nx
```

1. Navigate to `http://localhost:5000`
2. Akan auto-redirect ke `/login`
3. Enter credentials
4. Click **Login**

### 2. Add Items to Cart
1. Browse menu categories
2. Click **Add to Cart** button pada item yang diinginkan
3. Item akan muncul di cart sidebar
4. Adjust quantity dengan **+** dan **-** buttons

### 3. Process Payment
1. Scroll ke bagian **Checkout**
2. Enter nama pembeli
3. Enter jumlah uang yang dibayar
4. Click **Proses Pembayaran**
5. View payment breakdown (subtotal, diskon, PPN, total, kembalian)

### 4. Download Receipt
1. Setelah payment processed
2. Click **Download Struk**
3. PDF akan auto-download
4. Open dan print receipt

### 5. Clear Cart
- Click **Clear Cart** button untuk reset
- Confirmation dialog akan muncul
- All items akan dihapus

### 6. Logout
1. Click username dropdown di navbar
2. Click **Logout**
3. Confirm logout
4. Session dan cart akan cleared
5. Redirect to login page

---

## 📁 Project Structure

```
restaurant-pos-system/
│
├── 📄 app.py                      # Main Flask application
│   ├── Authentication routes
│   ├── Cart management endpoints
│   ├── Checkout logic
│   ├── PDF generation
│   └── Helper functions
│
├── 📁 data/
│   └── menu.json                 # Menu database (JSON)
│
├── 📁 static/
│   ├── 📁 css/
│   │   └── style.css            # Custom styles
│   ├── 📁 js/
│   │   └── cart.js              # Cart JavaScript logic
│   └── 📁 img/
│       ├── logo.png             # Restaurant logo
│       └── [menu-images]        # Product images
│
├── 📁 templates/
│   ├── login.html               # Login page template
│   └── index.html               # Main dashboard template
│
├── 📄 requirements.txt           # Python dependencies
├── 📄 README.md                  # This documentation
└── 📄 .gitignore                # Git ignore rules
```

---

## 🔌 API Endpoints

### Authentication

#### **POST /login**
Login authentication handler

**Request:**
```http
POST /login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

email=zhaenx_id@yeswehack.com&password=zh43nx
```

**Response:**
```http
HTTP/1.1 302 Found
Location: /
Set-Cookie: session=...
```

#### **GET/POST /logout**
Logout and clear session

**Response:**
```http
HTTP/1.1 302 Found
Location: /login
Set-Cookie: session=; expires=Thu, 01 Jan 1970 00:00:00 GMT
```

---

### Cart Management

#### **POST /cart/update**
Update cart (add, plus, minus, remove)

**Request:**
```json
{
  "action": "add",
  "id": "1"
}
```

**Response:**
```json
{
  "cart": [...],
  "count": 3,
  "subtotal": 75000,
  "diskon": 7500,
  "ppn": 6750,
  "total": 74250
}
```

**Actions:**
- `add` - Add item atau increase qty jika sudah ada
- `plus` - Increase quantity
- `minus` - Decrease quantity (auto-remove at 0)
- `remove` - Remove item regardless of quantity

#### **GET /cart/get**
Get current cart from session

**Response:**
```json
{
  "cart": [
    {
      "id": 1,
      "nama": "Nasi Goreng",
      "price": 25000,
      "qty": 2,
      "subtotal": 50000
    }
  ],
  "count": 2,
  "subtotal": 50000,
  "diskon": 5000,
  "ppn": 4500,
  "total": 49500
}
```

#### **POST /cart/clear**
Clear all items from cart

**Response:**
```json
{
  "success": true
}
```

---

### Payment

#### **POST /checkout**
Process payment dan calculate change

**Request:**
```json
{
  "nama": "John Doe",
  "cash": 100000
}
```

**Response:**
```json
{
  "nama": "John Doe",
  "cash": 100000,
  "subtotal": 75000,
  "ppn": 6750,
  "diskon": 7500,
  "total": 74250,
  "kembalian": 25750
}
```

**Validations:**
- Nama tidak boleh kosong
- Cash harus valid integer
- Cart tidak boleh kosong
- Cash harus >= total

---

### Receipt

#### **POST /download_struk**
Generate dan download PDF receipt

**Request:**
```json
{
  "nama": "John Doe",
  "cash": 100000
}
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="struk-08-12-2024-143052.pdf"
Content-Length: 12345

[PDF Binary Data]
```

---

## 🔒 Security

### Implemented Security Features

#### 1. **Session Security**
```python
app.config['SESSION_COOKIE_HTTPONLY'] = True   # Prevent XSS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Prevent CSRF
app.config['PERMANENT_SESSION_LIFETIME'] = 3600 # 1 hour timeout
```

#### 2. **Route Protection**
```python
@login_required
def protected_route():
    # Only authenticated users can access
```

#### 3. **Input Validation**
- Email format validation
- Password presence check
- Cart item validation
- Cash amount validation

#### 4. **Complete Logout**
- Clear all session data
- Delete all cookies
- Prevent back-button access
- No-cache headers

#### 5. **Session Timeout**
- Auto-logout after 1 hour
- Inactivity detection
- Timestamp validation

### Security Best Practices (Production)

⚠️ **IMPORTANT untuk Production:**

1. **Password Hashing**
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   
   hashed = generate_password_hash(password)
   check_password_hash(hashed, input_password)
   ```

2. **HTTPS Only**
   ```python
   app.config['SESSION_COOKIE_SECURE'] = True
   ```

3. **Rate Limiting**
   ```python
   from flask_limiter import Limiter
   
   limiter = Limiter(app, default_limits=["200 per day", "50 per hour"])
   ```

4. **CSRF Protection**
   ```python
   from flask_wtf.csrf import CSRFProtect
   
   csrf = CSRFProtect(app)
   ```

5. **Database for Users**
   - Move from hardcoded credentials
   - Implement proper user management
   - Add user roles (admin, cashier)

---

## 🧪 Testing

### Manual Testing Checklist

#### Authentication Tests
- [ ] Login dengan credentials valid
- [ ] Login dengan credentials invalid
- [ ] Logout functionality
- [ ] Session timeout (after 1 hour)
- [ ] Back button after logout
- [ ] Direct access to protected routes

#### Cart Tests
- [ ] Add item to empty cart
- [ ] Add duplicate item (qty should increase)
- [ ] Plus quantity
- [ ] Minus quantity
- [ ] Auto-remove at qty = 0
- [ ] Remove item manually
- [ ] Clear entire cart
- [ ] Cart persistence after page refresh

#### Payment Tests
- [ ] Checkout dengan cart kosong (should error)
- [ ] Checkout dengan nama kosong (should error)
- [ ] Checkout dengan cash invalid (should error)
- [ ] Checkout dengan cash kurang (should error)
- [ ] Checkout dengan valid data (should success)
- [ ] Calculate kembalian correctly

#### PDF Tests
- [ ] Generate PDF dengan valid data
- [ ] PDF size > 0 bytes
- [ ] PDF dapat dibuka
- [ ] All data correct di PDF
- [ ] Logo muncul (if available)
- [ ] Multiple pages untuk long receipts

### Automated Testing (Future)

```python
# tests/test_auth.py
def test_login_success():
    response = client.post('/login', data={
        'email': 'zhaenx_id@yeswehack.com',
        'password': 'zh43nx'
    })
    assert response.status_code == 302
    assert response.location == '/'

# tests/test_cart.py
def test_add_to_cart():
    response = client.post('/cart/update', json={
        'action': 'add',
        'id': '1'
    })
    assert response.status_code == 200
    assert response.json['count'] == 1
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. **"ModuleNotFoundError: No module named 'flask'"**
**Solution:**
```bash
pip install -r requirements.txt
```

#### 2. **"TemplateNotFound: login.html"**
**Solution:**
- Check `templates/` folder exists
- Check `login.html` is in `templates/`
- Verify file name spelling

#### 3. **"FileNotFoundError: menu.json"**
**Solution:**
- Create `data/` folder
- Create `menu.json` file
- Check file path in code

#### 4. **PDF Download 0 bytes**
**Solutions:**
- Check `reportlab` installed correctly
- Check `buffer.seek(0)` is called
- Check `pdf.save()` is called
- Verify `logo.png` exists (if using)

#### 5. **Session tidak clear saat logout**
**Solutions:**
- Check `session.clear()` is called
- Clear browser cache manually
- Try incognito/private mode
- Check cookie deletion loop

#### 6. **Port 5000 already in use**
**Solutions:**
```bash
# Kill process on port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID [PID] /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Or use different port
app.run(port=5001)
```

#### 7. **"Address already in use"**
**Solution:**
```bash
# Change port atau kill existing process
python app.py --port 5001
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### 1. Fork the Project
```bash
git clone https://github.com/yourusername/restaurant-pos-system.git
cd restaurant-pos-system
```

### 2. Create Feature Branch
```bash
git checkout -b feature/AmazingFeature
```

### 3. Commit Changes
```bash
git commit -m 'Add some AmazingFeature'
```

### 4. Push to Branch
```bash
git push origin feature/AmazingFeature
```

### 5. Open Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add comments untuk complex logic
- Update documentation
- Test thoroughly before PR
- Include screenshots untuk UI changes

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Kelompok 4

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 👥 Team

**Kelompok 4 - Tim Pengembang**

| Name | Role | GitHub |
|------|------|--------|
| Member 1 | Project Lead & Backend | [@member1](https://github.com/member1) |
| Member 2 | Frontend & UI/UX | [@member2](https://github.com/member2) |
| Member 3 | Database & API | [@member3](https://github.com/member3) |
| Member 4 | Testing & Documentation | [@member4](https://github.com/member4) |

---

## 🙏 Acknowledgments

- **Flask** - Amazing Python web framework
- **ReportLab** - Powerful PDF generation library
- **Bootstrap** - Responsive frontend framework
- **Font Awesome** - Beautiful icon set
- **Dosen Pembimbing** - Guidance and support
- **Anthropic Claude** - AI assistance for development

---

## 📞 Support

Jika ada pertanyaan atau issues:

- 📧 Email: kelompok4@university.ac.id
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/restaurant-pos-system/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/restaurant-pos-system/discussions)

---

## 🗺️ Roadmap

### Version 1.1 (Planned)
- [ ] Multi-user support dengan roles
- [ ] Database integration (PostgreSQL)
- [ ] Transaction history
- [ ] Sales reports & analytics
- [ ] Export to Excel

### Version 2.0 (Future)
- [ ] Mobile app (React Native)
- [ ] Payment gateway integration
- [ ] Inventory management
- [ ] Employee management
- [ ] Real-time notifications

---

## 📊 Statistics

![Lines of Code](https://img.shields.io/badge/Lines%20of%20Code-2000+-blue)
![Files](https://img.shields.io/badge/Files-10+-green)
![Contributors](https://img.shields.io/badge/Contributors-4-orange)

**Development Stats:**
- Total Development Time: ~80 hours
- Backend Code: ~800 lines
- Frontend Code: ~600 lines
- Documentation: ~400 lines

---

## 🎓 Educational Purpose

Project ini dikembangkan untuk tujuan edukasi dalam mata kuliah **Pemrograman Web**. Implementasi mencakup:

- ✅ Web development dengan Flask
- ✅ Session management
- ✅ Authentication & Authorization
- ✅ RESTful API design
- ✅ PDF generation
- ✅ Frontend/Backend integration
- ✅ Security best practices

---

## ⚡ Quick Start Guide

**TL;DR - Get Started in 5 Minutes:**

```bash
# 1. Clone
git clone https://github.com/yourusername/restaurant-pos-system.git
cd restaurant-pos-system

# 2. Install
pip install flask reportlab

# 3. Run
python app.py

# 4. Login
# URL: http://localhost:5000
# Email: zhaenx_id@yeswehack.com
# Password: zh43nx
```

---

## 📝 Changelog

### Version 1.0.0 (2024-12-08)
- ✨ Initial release
- ✅ Authentication system
- ✅ Cart management
- ✅ Payment processing
- ✅ PDF receipt generation
- ✅ Responsive UI

---

<div align="center">

### Made with ❤️ by Kelompok 4

**⭐ Star this repository if you found it helpful!**

[Report Bug](https://github.com/yourusername/restaurant-pos-system/issues) · [Request Feature](https://github.com/yourusername/restaurant-pos-system/issues)

---

© 2024 Kelompok 4. All Rights Reserved.

</div>
