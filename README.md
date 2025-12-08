<div align="center">
<h1>Sistem Kasir Restoran Digital</h1>

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)
</div>

## 📌 Deskripsi
<div align="center">
Aplikasi ini adalah sistem kasir digital berbasis web yang dibangun menggunakan Flask.
Tujuan utamanya adalah mempermudah proses pemesanan dengan menyediakan fitur pengelolaan keranjang, perhitungan otomatis (subtotal, diskon, PPN, total), dan kemampuan untuk mengunduh struk dalam bentuk PDF lengkap dengan logo restoran.

Dikembangkan oleh Kelompok 3 sebagai project akhir (UTS) mata kuliah Dasar pemprograman.<br>
Universitas Bina Sarana Informatika (Cikarang).
</div>

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

## 📸 Screenshots

<details>
<summary>Click to view all screenshots</summary>

### 1. Login Page
- Modern design
- Error handling dengan animations

![Login Demo](https://i.ibb.co.com/pvmjfSdF/login-Page.png/200x200/667eea/ffffff?text=Login+Page)

### 2. Menu Display
- Card-based layout
- Category navigation
- Clear pricing

![Dashboard Demo](https://i.ibb.co.com/x86Q1Td7/maindashoard.png/200x200/764ba2/ffffff?text=Dashboard)

### 3. Shopping Cart
- Real-time updates
- Quantity controls
- Total breakdown

![Dashboard Demo](https://i.ibb.co.com/rKBkZYKS/cart.png/200x200/764ba2/ffffff?text=Dashboard)

### 4. Checkout Process
- Customer information
- Payment calculation
- Receipt generation

![Dashboard Demo](https://i.ibb.co.com/LDZq47bG/check-Out.png/200x200/764ba2/ffffff?text=Dashboard)

### 5. PDF Receipt
- Professional layout
- Complete transaction details
- Business information

![Receipt Demo](https://i.ibb.co.com/FL39Gx8D/struk.png/200x200/667eea/ffffff?text=PDF+Receipt)

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
- **Bootstrap 1.13.1** - Icons
- **Scrollrevealjs** - Animation Scrolling

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
git clone https://github.com/R-Mahendra/Kasir-Web-Apps-Python-flask-.git
cd Kasir-Web-Apps-Python-flask
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
python main.py
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

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Kelompok 3

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 👥 Team

**Kelompok 3 - Tim Pengembang**

| Name | NIM |
|------|--------|
| Reza Mahendra | 17250007 |
| Rifqy Ardian Adinata | 17250522 |
| Fitria Haryani | 17250015 |
| Muhamad Bagas Triandy | 17250036 |
| Cheril Aprillia Putri | 17250385 |

---

## 🙏 Acknowledgments

- **Flask** - Amazing Python web framework
- **ReportLab** - Powerful PDF generation library
- **Bootstrap** - Responsive frontend framework
- **Dosen Pembimbing** - Guidance and support
- **Anthropic Claude** - AI assistance for development

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
git clone https://github.com/R-Mahendra/Kasir-Web-Apps-Python-flask-.git
cd Kasir-Web-Apps-Python-flask

# 2. Install
pip install -r requirements.txt

# 3. Run
python main.py

# 4. Login
# URL: http://localhost:5000
# Email: zhaenx_id@yeswehack.com
# Password: zh43nx
```

---

## 📝 Changelog

### Version 5.1.0 (2025-12-08)
- ✨ Initial release
- ✅ Authentication system
- ✅ Cart management
- ✅ Payment processing
- ✅ PDF receipt generation
- ✅ Responsive UI

---

<div align="center">

### Made with ❤️ by Kelompok 3 | Universitas Bina Sarana Informatika (UBSI Cikarang)

**⭐ Star this repository if you found it helpful!**

[Report Bug](https://github.com/yourusername/restaurant-pos-system/issues) · [Request Feature](https://github.com/yourusername/restaurant-pos-system/issues)

---

© 2025 Kelompok 3. All Rights Reserved.

</div>
