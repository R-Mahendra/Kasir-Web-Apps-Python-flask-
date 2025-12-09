import json
import io
import datetime
from decimal import Decimal
from flask import (
    Flask,
    redirect,
    send_file,
    render_template,
    request,
    session,
    jsonify,
    url_for,
)
from flask_login import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash


# ========================================================================
# INISIALISASI APLIKASI FLASK
# ========================================================================

# Import Flask untuk membuat web application
app = Flask(__name__)

# Secret key untuk enkripsi session cookies
# Digunakan untuk sign data session agar tidak bisa dimanipulasi oleh client
# Harus random dan rahasia untuk keamanan aplikasi
# Key ini di-generate menggunakan cryptographic random generator
app.secret_key = "53616c7465645f5ff22da9cb2932309bc5d27f5fb2f59d57bca3150476f82a19"


app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = 3600


USERS = {"zhaenx_id@yeswehack.com": generate_password_hash("zh43nx")}


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "logged_in" not in session or not session.get("logged_in"):
            return redirect(url_for("login"))

        # Session timeout 1 jam
        login_time = session.get("login_time")
        if login_time:

            current_time = datetime.datetime.now().timestamp()

            if current_time - login_time > 3600:  # 3600 detik = 1 jam
                session.clear()
                return redirect(url_for("login", timeout="true"))

        return f(*args, **kwargs)

    return decorated_function


# ========================================================================
# AUTHENTICATION ROUTES
# ========================================================================
@app.before_request
def blocker():
    safe_paths = ["/login"]

    if request.path.startswith("/static"):
        return

    if not session.get("logged_in"):
        if request.path not in safe_paths:
            return redirect(url_for("login"))


@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login page and authentication handler
    """
    if session.get("logged_in"):
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Input kosong
        if not email or not password:
            return (
                render_template("login.html", error="Email dan password harus diisi"),
                401,
            )

        # Cek kredensial
        if email in USERS and check_password_hash(USERS[email], password):
            session.clear()
            session["logged_in"] = True
            session["email"] = email
            session["login_time"] = datetime.datetime.now().timestamp()
            session.permanent = True

            session["jumlahcart"] = []
            session["cart_count"] = 0

            next_page = request.args.get("next")
            return redirect(next_page if next_page else url_for("index"))

        else:
            return (
                render_template("login.html", error="Email atau password salah...!"),
                401,
            )

    # GET request
    timeout = request.args.get("timeout")
    error_msg = "Session expired, silakan login kembali" if timeout else None
    return render_template("login.html", error=error_msg)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Logout handler - clear session dan redirect ke login

    Security measures:
    1. Clear all session data
    2. Mark session for deletion
    3. Redirect ke login page
    """
    # Clear semua data di session
    # Ini akan hapus: logged_in, username, cart, pembeli, dll
    session.clear()
    response = redirect(url_for("login"))

    # Clear all cookies
    for cookie_name in request.cookies:
        response.set_cookie(
            cookie_name,
            "",
            expires=0,
            max_age=0,
            path="/",
            secure=False,
            httponly=True,
            samesite="Lax",
        )

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response


@app.route("/")
@login_required
def index():

    if not session.get("logged_in"):
        return redirect("/login")
    # Ambil data cart dari session.
    # Kalau belum ada, default-nya list kosong.
    cart = session.get("jumlahcart", [])

    # Render halaman index.html
    # Kirim data menu dan cart ke template
    return render_template("index.html", menu=menu, cart=cart)


# ========================================================================
# KONSTANTA APLIKASI
# ========================================================================

# Konstanta untuk perhitungan pajak dan diskon
# Menggunakan Decimal untuk akurasi tinggi dalam perhitungan finansial
# Float memiliki masalah precision: 0.1 + 0.2 != 0.3
# Decimal mengatasi masalah ini dan cocok untuk financial calculation

PAJAK = Decimal("0.10")  # PPN 10% sesuai regulasi perpajakan Indonesia
DISKON = Decimal("0.10")  # Diskon promosi 10% untuk semua transaksi


# ========================================================================
# LOAD DATA MENU DARI FILE JSON
# ========================================================================


def load_menu():
    """
    Memuat data menu dari file JSON dengan error handling yang robust

    Fungsi ini dipanggil sekali saat aplikasi start untuk load semua data menu
    dari file eksternal (data/menu.json) ke dalam memory

    Returns:
        dict: Dictionary berisi data menu yang sudah di-parse dari JSON
              Format: {"kategori": [{"id": 1, "nama": "...", "price": ...}, ...]}
        dict: Dictionary kosong {} jika terjadi error (file tidak ada atau invalid)

    Error Handling:
        - FileNotFoundError: File menu.json tidak ditemukan
        - JSONDecodeError: Syntax error di file JSON (koma kurang, quote salah, dll)
    """
    try:
        # Buka file menu.json dengan mode read
        # encoding="utf-8" untuk support karakter Indonesia (é, ñ, dll)
        # Context manager (with) otomatis close file setelah selesai
        with open("data/menu.json", "r", encoding="utf-8") as file:
            # Parse JSON string menjadi Python dictionary
            # json.load() membaca file dan convert ke dict/list Python
            return json.load(file)

    except FileNotFoundError:
        # Exception ini muncul jika file tidak ditemukan
        # Bisa karena path salah atau file memang tidak ada

        # Log error ke console/file untuk debugging
        # Penting untuk troubleshooting di production environment
        app.logger.error("menu.json not found")

        # Return empty dict agar aplikasi tidak crash
        # Aplikasi tetap bisa jalan, hanya menu-nya kosong
        return {}

    except json.JSONDecodeError:
        # Exception ini muncul jika file JSON tidak valid
        # Contoh: ada koma yang kurang, bracket tidak closing, dll

        # Log error untuk debugging
        app.logger.error("Invalid JSON in menu.json")

        # Return empty dict agar aplikasi tidak crash
        return {}


# Execute fungsi load_menu() saat aplikasi start
# Variable global 'menu' ini akan digunakan di seluruh aplikasi
# Load sekali saja untuk efisiensi (tidak load ulang setiap request)
menu = load_menu()


# ========================================================================
# HELPER FUNCTIONS - PERHITUNGAN FINANSIAL
# ========================================================================


def hitung_total(subtotal):
    """
    Menghitung diskon, PPN, dan total akhir berdasarkan subtotal

    Alur perhitungan sesuai aturan perpajakan Indonesia:
    1. Hitung diskon dari subtotal
    2. Kurangi subtotal dengan diskon = DPP (Dasar Pengenaan Pajak)
    3. Hitung PPN dari DPP (BUKAN dari subtotal!)
    4. Total = DPP + PPN

    Args:
        subtotal (int/float): Total harga semua item sebelum diskon dan pajak

    Returns:
        tuple: (diskon, ppn, total) - semua dalam format integer (Rupiah)

    Contoh:
        subtotal = 100000
        diskon, ppn, total = hitung_total(100000)
        # diskon = 10000 (10% dari 100000)
        # dpp = 90000 (100000 - 10000)
        # ppn = 9000 (10% dari 90000)
        # total = 99000 (90000 + 9000)
    """

    # Konversi subtotal ke Decimal untuk perhitungan akurat
    # str() diperlukan untuk menghindari floating point error
    # Decimal("100.50") lebih akurat dari Decimal(100.50)
    subtotal = Decimal(str(subtotal))

    # STEP 1: Hitung diskon 10% dari subtotal
    # Contoh: Rp 100.000 × 10% = Rp 10.000
    # int() untuk convert ke integer karena Rupiah tidak ada sen
    diskon = int(subtotal * DISKON)

    # STEP 2: Hitung DPP (Dasar Pengenaan Pajak)
    # DPP = Subtotal dikurangi diskon
    # Ini adalah harga yang akan dikenakan pajak
    # Contoh: Rp 100.000 - Rp 10.000 = Rp 90.000
    dpp = subtotal - diskon

    # STEP 3: Hitung PPN 10% dari DPP (PENTING: dari DPP, bukan subtotal!)
    # Sesuai aturan perpajakan, pajak dihitung SETELAH diskon
    # Contoh: Rp 90.000 × 10% = Rp 9.000
    ppn = int(dpp * PAJAK)

    # STEP 4: Hitung total yang harus dibayar
    # Total = DPP + PPN (harga setelah diskon + pajak)
    # Contoh: Rp 90.000 + Rp 9.000 = Rp 99.000
    total = dpp + ppn

    # Return tuple berisi 3 nilai: diskon, ppn, dan total
    # Semua di-convert ke int karena Rupiah tidak menggunakan desimal
    return int(diskon), int(ppn), int(total)


def calculate_totals(cart):
    """
    Menghitung semua total yang ada di keranjang belanja

    Fungsi wrapper yang menggabungkan:
    1. Perhitungan subtotal dari semua item di cart
    2. Perhitungan diskon, PPN, dan total menggunakan hitung_total()

    Args:
        cart (list): List of dictionaries, setiap item memiliki keys:
                    - id: ID unik item
                    - nama: Nama menu
                    - price: Harga per item
                    - qty: Jumlah quantity yang dipesan
                    - subtotal: price × qty

    Returns:
        tuple: (subtotal, diskon, ppn, total) - semua dalam integer

    Contoh cart:
        [
            {"id": 1, "nama": "Nasi Goreng", "price": 25000, "qty": 2, "subtotal": 50000},
            {"id": 2, "nama": "Es Teh", "price": 5000, "qty": 3, "subtotal": 15000}
        ]

        Hasil:
        subtotal = 65000  (50000 + 15000)
        diskon = 6500     (10% dari 65000)
        ppn = 5850        (10% dari 58500)
        total = 64350     (58500 + 5850)
    """

    # Hitung subtotal dengan cara:
    # 1. Loop setiap item di cart
    # 2. Kalikan price × qty untuk setiap item
    # 3. Jumlahkan semua hasil perkalian menggunakan sum()
    #
    # Generator expression (... for item in cart) lebih efisien dari loop biasa
    # karena tidak membuat list intermediate di memory
    #
    # Contoh:
    # Item 1: 25000 × 2 = 50000
    # Item 2: 5000 × 3 = 15000
    # Subtotal = 50000 + 15000 = 65000
    subtotal = sum(int(item["price"]) * int(item["qty"]) for item in cart)

    # Panggil fungsi hitung_total untuk mendapatkan diskon, ppn, dan total
    # Fungsi ini menerapkan semua logic perpajakan yang kompleks
    diskon, ppn, total = hitung_total(subtotal)

    # Return semua nilai dalam satu tuple
    # Tuple ini akan di-unpack di tempat lain untuk update display
    return subtotal, diskon, ppn, total


# ========================================================================
# HELPER FUNCTIONS - PENCARIAN DATA
# ========================================================================


def find_item_in_cart(cart, item_id):
    """
    Mencari item di keranjang belanja berdasarkan ID

    Fungsi ini digunakan untuk operasi:
    - PLUS: Cari item dulu sebelum tambah qty
    - MINUS: Cari item dulu sebelum kurangi qty
    - REMOVE: Cari item dulu sebelum hapus dari cart

    Args:
        cart (list): List of items dalam cart (dari session)
        item_id (str/int): ID item yang ingin dicari

    Returns:
        dict: Reference ke item yang ditemukan (bukan copy!)
              Item memiliki keys: id, nama, price, qty, subtotal, img
        None: Jika item dengan ID tersebut tidak ada di cart

    Important Notes:
        - Return adalah REFERENCE, bukan copy
        - Perubahan pada return value akan affect cart langsung
        - Tidak perlu save lagi ke session setelah modify

    Contoh penggunaan:
        item = find_item_in_cart(cart, "5")
        if item:
            item["qty"] += 1  # Langsung mengubah qty di cart
            item["subtotal"] = item["qty"] * item["price"]
        else:
            print("Item tidak ditemukan")
    """

    # Loop setiap item yang ada di keranjang
    for item in cart:
        # Bandingkan ID sebagai string untuk menghindari type mismatch
        # ID bisa datang sebagai:
        # - int dari JSON parsing ({"id": 5})
        # - string dari form POST (request.form["id"] = "5")
        #
        # Dengan convert keduanya ke string, kita pastikan perbandingan akurat
        # str(5) == str("5") → "5" == "5" → True
        if str(item["id"]) == str(item_id):
            # Item ditemukan!
            # Return reference ke item (bukan copy)
            # Ini adalah Python feature: objects di-pass by reference
            return item

    # Loop selesai tapi tidak ada yang match
    # Return None untuk indicate "not found"
    # Caller bisa cek dengan: if item: atau if item is None:
    return None


def find_menu_item(item_id):
    """
    Mencari item di database menu berdasarkan ID

    Fungsi ini dipanggil saat user klik "Add to Cart"
    Kita hanya punya ID dari button, perlu ambil data lengkap dari menu database

    Args:
        item_id (str/int): ID item yang ingin dicari

    Returns:
        dict: Data item lengkap dari menu dengan keys:
              - id: ID unik item
              - nama: Nama menu
              - price: Harga per item
              - img: Path ke gambar menu
              - kategori: Kategori menu (optional)
        None: Jika item tidak ditemukan di database menu

    Struktur menu database:
        {
            "makanan": [
                {"id": 1, "nama": "Nasi Goreng", "price": 25000, "img": "nasi_goreng.jpg"},
                {"id": 2, "nama": "Mie Goreng", "price": 20000, "img": "mie_goreng.jpg"}
            ],
            "minuman": [
                {"id": 10, "nama": "Es Teh", "price": 5000, "img": "es_teh.jpg"},
                {"id": 11, "nama": "Es Jeruk", "price": 7000, "img": "es_jeruk.jpg"}
            ],
            "snack": [...]
        }

    Contoh penggunaan:
        menu_data = find_menu_item("1")
        if menu_data:
            cart.append({
                "id": menu_data["id"],
                "nama": menu_data["nama"],
                "price": menu_data["price"],
                "img": menu_data["img"],
                "qty": 1
            })
    """

    # Loop setiap kategori di menu
    # menu.items() return tuples: ("makanan", [...]), ("minuman", [...])
    # kategori = "makanan", items = list of menu items
    for kategori, items in menu.items():

        # Loop setiap item dalam kategori tersebut
        # m = menu item dictionary
        for m in items:
            # Bandingkan ID sebagai string (alasan sama seperti find_item_in_cart)
            if str(m["id"]) == str(item_id):
                # Item ditemukan!
                # Return seluruh data item dari database menu
                # Data ini akan digunakan untuk populate cart
                return m

    # Item tidak ditemukan di semua kategori
    # Return None untuk indicate "not found"
    # Ini bisa terjadi jika:
    # - ID invalid/tidak ada di database
    # - Menu database corrupt
    # - Ada bug di frontend yang kirim ID salah
    return None


# ========================================================================
# HELPER FUNCTION - UPDATE SESSION CART
# ========================================================================


def update_session_cart(cart):
    """
    Menyimpan cart ke session dan menghitung total quantity

    Fungsi ini dipanggil setiap kali ada perubahan pada cart untuk:
    1. Persist data ke server-side session
    2. Menghitung total items untuk badge counter
    3. Mark session sebagai modified (penting untuk Flask session)

    Args:
        cart (list): List of dictionaries berisi items di cart

    Important Notes:
        - session.modified = True WAJIB dipanggil
        - Tanpa ini, perubahan pada list/dict tidak akan tersimpan
        - Ini adalah common pitfall dalam Flask session management
    """

    # Simpan cart ke session dengan key "jumlahcart"
    # Data ini akan persist selama session aktif (hingga browser close)
    session["jumlahcart"] = cart

    # Hitung total quantity dari semua item untuk badge counter
    # sum() dengan generator expression lebih efisien daripada loop
    # Contoh: jika cart punya 3 items dengan qty [2, 1, 3]
    # maka cart_count = 2 + 1 + 3 = 6
    session["cart_count"] = sum(i["qty"] for i in cart)

    # CRITICAL: Mark session as modified
    # Flask session menggunakan signed cookies yang hanya diupdate jika modified
    # Tanpa ini, perubahan pada mutable objects (list/dict) tidak tersimpan
    # Ini adalah best practice untuk semua session modifications
    session.modified = True


# ========================================================================
# API ENDPOINT - CART UPDATE
# ========================================================================


@app.route("/cart/update", methods=["POST"])
@login_required
def cart_update():
    """
    Endpoint untuk menangani semua operasi pada cart

    Supported Actions:
        - "add": Tambah item baru atau increase qty jika sudah ada
        - "plus": Increase quantity item yang sudah ada
        - "minus": Decrease quantity, auto-remove jika qty = 0
        - "remove": Hapus item dari cart (regardless of qty)

    Request Body (JSON):
        {
            "action": "add|plus|minus|remove",
            "id": "item_id"
        }

    Response (JSON):
        Success (200):
        {
            "cart": [...],           # Updated cart data
            "count": 5,              # Total quantity for badge
            "subtotal": 100000,      # Total sebelum diskon
            "diskon": 10000,         # Potongan harga
            "ppn": 9000,             # Pajak
            "total": 99000           # Total akhir
        }

        Error (400/404/500):
        {
            "error": "Error message"
        }

    HTTP Status Codes:
        200: Success
        400: Bad request (invalid input)
        404: Item not found
        500: Internal server error
    """

    try:
        # ============================================================
        # STEP 1: VALIDASI REQUEST & EXTRACT PARAMETERS
        # ============================================================

        # Parse JSON dari request body
        # request.get_json() return None jika:
        # - Request tidak mengandung JSON
        # - Content-Type header bukan application/json
        # - JSON syntax error (invalid format)
        data = request.get_json()

        # Validasi: pastikan request body mengandung JSON
        # Return 400 Bad Request jika tidak ada data
        if not data:
            return jsonify({"error": "Invalid request"}), 400

        # Extract action dan item_id dari JSON payload
        # .get() method return None jika key tidak ada (safe)
        action = data.get("action")  # Expected: "add"|"plus"|"minus"|"remove"
        item_id = data.get("id")  # Expected: string atau integer ID

        # Validasi: pastikan parameter wajib tersedia
        # action harus ada dan tidak empty string
        # item_id harus ada (boleh 0, tapi tidak boleh None)
        if not action or item_id is None:
            return jsonify({"error": "Missing parameters"}), 400

        # ============================================================
        # STEP 2: LOAD CART & FIND TARGET ITEM
        # ============================================================

        # Ambil cart dari session
        # Default ke empty list jika:
        # - Session baru (first time user)
        # - Cart sudah di-clear sebelumnya
        # - Session expired dan di-reset
        cart = session.get("jumlahcart", [])

        # Cari apakah item dengan ID ini sudah ada di cart
        # find_item_in_cart return:
        # - Reference ke item dict jika ada (modifiable)
        # - None jika tidak ada
        target = find_item_in_cart(cart, item_id)

        # ============================================================
        # STEP 3: HANDLE ACTION - ADD
        # ============================================================

        if action == "add":
            # ADD action punya 2 skenario berbeda

            # SKENARIO 1: Item BELUM ada di cart (target = None)
            if not target:
                # Item baru, perlu ambil data lengkap dari menu database
                menu_item = find_menu_item(item_id)

                # Validasi: pastikan item exists di menu
                # Bisa tidak ada jika:
                # - ID invalid/typo
                # - Item sudah dihapus dari menu
                # - Bug di frontend yang kirim ID salah
                if not menu_item:
                    return jsonify({"error": "Item not found"}), 404

                # Buat dictionary baru untuk item
                # Copy data dari menu_item dan tambah qty & subtotal
                cart.append(
                    {
                        "id": menu_item["id"],  # ID unik item
                        "nama": menu_item["nama"],  # Nama menu
                        "price": menu_item["price"],  # Harga per item
                        "img": menu_item["img"],  # Path gambar
                        "qty": 1,  # Quantity awal = 1
                        "subtotal": menu_item["price"],  # price × qty = price × 1
                    }
                )

            # SKENARIO 2: Item SUDAH ada di cart (target != None)
            else:
                # Tinggal tambah quantity dan update subtotal
                # target adalah reference, jadi modifikasi langsung affect cart
                target["qty"] += 1
                target["subtotal"] = target["qty"] * target["price"]

        # ============================================================
        # STEP 4: HANDLE ACTION - PLUS
        # ============================================================

        elif action == "plus":
            # PLUS hanya bisa dilakukan pada item yang SUDAH ada
            # Validasi: jika item tidak ada, return error
            # Seharusnya tidak terjadi karena button plus hanya muncul di cart
            # Tapi kita tetap validate untuk robustness
            if not target:
                return jsonify({"error": "Item not in cart"}), 404

            # Tambah quantity dan update subtotal
            # Logic sama dengan ADD skenario 2
            target["qty"] += 1
            target["subtotal"] = target["qty"] * target["price"]

        # ============================================================
        # STEP 5: HANDLE ACTION - MINUS
        # ============================================================

        elif action == "minus":
            # MINUS juga hanya untuk item yang sudah ada
            if not target:
                return jsonify({"error": "Item not in cart"}), 404

            # Kurangi quantity
            target["qty"] -= 1

            # CRITICAL LOGIC: Auto-remove jika qty = 0
            # Ini memberikan UX yang baik:
            # - User tidak perlu klik remove button terpisah
            # - Tinggal tekan minus sampai item hilang
            # - Lebih intuitive untuk mobile users
            if target["qty"] <= 0:
                # Hapus item dari cart
                # cart.remove() mencari dan menghapus object dari list
                cart.remove(target)
            else:
                # Qty masih positif, update subtotal
                target["subtotal"] = target["qty"] * target["price"]

        # ============================================================
        # STEP 6: HANDLE ACTION - REMOVE
        # ============================================================

        elif action == "remove":
            # REMOVE menghapus item regardless of quantity
            # Validasi: item harus ada
            if not target:
                return jsonify({"error": "Item not in cart"}), 404

            # Hapus item dari cart
            # Tidak peduli qty-nya berapa, langsung dihapus
            # Di frontend ada confirmation dialog untuk prevent accidental delete
            cart.remove(target)

        # ============================================================
        # STEP 7: HANDLE INVALID ACTION
        # ============================================================

        else:
            # Action tidak dikenali (bukan add/plus/minus/remove)
            # Ini defensive programming - jangan assume input selalu valid
            # Bisa terjadi jika:
            # - Typo di frontend code
            # - Malicious request
            # - API misuse
            return jsonify({"error": "Invalid action"}), 400

        # ============================================================
        # STEP 8: UPDATE SESSION & CALCULATE TOTALS
        # ============================================================

        # Simpan cart yang sudah dimodifikasi ke session
        # Function ini juga menghitung cart_count untuk badge
        update_session_cart(cart)

        # Hitung semua total finansial untuk response
        # calculate_totals return tuple: (subtotal, diskon, ppn, total)
        subtotal, diskon, ppn, total = calculate_totals(cart)

        # ============================================================
        # STEP 9: RETURN SUCCESS RESPONSE
        # ============================================================

        # Return JSON response dengan semua data yang dibutuhkan frontend
        # Status code 200 (OK) adalah default untuk return tanpa error
        return jsonify(
            {
                "cart": cart,  # List lengkap items di cart
                "count": sum(i["qty"] for i in cart),  # Total qty untuk badge
                "subtotal": subtotal,  # Total sebelum diskon
                "diskon": diskon,  # Potongan harga
                "ppn": ppn,  # Pajak
                "total": total,  # Total akhir yang harus dibayar
            }
        )

    # ============================================================
    # EXCEPTION HANDLING
    # ============================================================

    except Exception as e:
        # Catch-all untuk unexpected errors
        # Contoh errors yang bisa terjadi:
        # - KeyError jika item structure tidak sesuai
        # - TypeError jika ada type mismatch
        # - Any runtime errors

        # Log error untuk debugging
        # Di production, log ini akan masuk ke file atau monitoring system
        app.logger.error(f"Error in cart_update: {str(e)}")

        # Return generic error message
        # JANGAN expose detail error ke client untuk security
        # Status code 500 = Internal Server Error
        return jsonify({"error": "Internal server error"}), 500


# ========================================================================
# API ENDPOINT - CHECKOUT
# ========================================================================


@app.route("/checkout", methods=["POST"])
@login_required
def checkout():
    """
    Endpoint untuk memproses pembayaran

    Proses checkout meliputi:
    1. Validasi data pembeli (nama, cash)
    2. Validasi cart tidak kosong
    3. Hitung total pembayaran
    4. Validasi uang cukup
    5. Hitung kembalian
    6. Simpan data transaksi ke session
    7. Return rincian pembayaran

    Request Body (JSON):
        {
            "nama": "John Doe",
            "cash": 150000
        }

    Response (JSON):
        Success (200):
        {
            "nama": "John Doe",
            "cash": 150000,
            "subtotal": 100000,
            "ppn": 9000,
            "diskon": 10000,
            "total": 99000,
            "kembalian": 51000
        }

        Error (400):
        {
            "error": "Error message"
        }

    Validation Rules:
        - Nama: tidak boleh kosong atau hanya spasi
        - Cash: harus integer positif
        - Cart: minimal 1 item
        - Cash: harus >= total
    """

    try:
        # ============================================================
        # STEP 1: VALIDASI REQUEST & EXTRACT DATA
        # ============================================================

        # Parse JSON dari request body
        data = request.get_json()

        # Validasi: pastikan request mengandung JSON
        if not data:
            return jsonify({"error": "Invalid request"}), 400

        # ============================================================
        # STEP 2: VALIDASI NAMA PEMBELI
        # ============================================================

        # Extract nama pembeli
        # .get("nama", "") return empty string jika key tidak ada
        # .strip() remove leading/trailing whitespace
        nama = data.get("nama", "").strip()

        # Validasi: nama tidak boleh kosong
        # Empty string atau hanya spasi akan fail validation
        # Nama penting untuk:
        # - Identifikasi pembeli di struk
        # - Courtesy (sapaan ke customer)
        # - Audit trail jika perlu
        if not nama:
            return jsonify({"error": "Nama tidak boleh kosong"}), 400

        # ============================================================
        # STEP 3: VALIDASI JUMLAH UANG (CASH)
        # ============================================================

        try:
            # Convert cash ke integer
            # Rupiah tidak menggunakan desimal, jadi int sudah cukup
            # .get("cash", 0) return 0 jika key tidak ada
            cash = int(data.get("cash", 0))

        except (ValueError, TypeError):
            # ValueError: jika input bukan angka (contoh: "abc", "12.5abc")
            # TypeError: jika input adalah type yang tidak bisa di-convert

            # Return error message yang user-friendly
            # Jangan expose technical error (ValueError) ke user
            return jsonify({"error": "Jumlah uang tidak valid"}), 400

        # ============================================================
        # STEP 4: VALIDASI CART TIDAK KOSONG
        # ============================================================

        # Ambil cart dari session
        cart = session.get("jumlahcart", [])

        # Validasi: cart minimal harus punya 1 item
        # Empty cart bisa terjadi jika:
        # - User langsung akses /checkout tanpa shopping
        # - Session expired
        # - Cart di-clear tapi user masih di checkout page
        if not cart:
            return jsonify({"error": "Keranjang kosong"}), 400

        # ============================================================
        # STEP 5: HITUNG TOTAL PEMBAYARAN
        # ============================================================

        # Hitung subtotal dari semua item di cart
        # sum() dengan generator expression
        # Loop setiap item, kalikan price × qty, lalu jumlahkan
        subtotal = sum(int(item["price"]) * int(item["qty"]) for item in cart)

        # Hitung diskon, ppn, dan total akhir
        # Menggunakan helper function hitung_total()
        # yang mengapply semua logic perpajakan
        diskon, ppn, total = hitung_total(subtotal)

        # ============================================================
        # STEP 6: VALIDASI UANG CUKUP
        # ============================================================

        # Cek apakah cash yang diberikan >= total yang harus dibayar
        if cash < total:
            # Uang tidak cukup, return error dengan detail
            # Format angka dengan thousand separator (:,)
            # Contoh: 99000 → "99,000"
            # Ini memudahkan user untuk baca dan membandingkan
            return (
                jsonify(
                    {
                        "error": f"Uang tidak cukup. Total: Rp {total:,}, Uang: Rp {cash:,}"
                    }
                ),
                400,
            )

        # ============================================================
        # STEP 7: HITUNG KEMBALIAN
        # ============================================================

        # Kembalian = Uang yang diberikan - Total yang harus dibayar
        # Contoh: Rp 150.000 - Rp 99.000 = Rp 51.000
        kembalian = cash - total

        # ============================================================
        # STEP 8: SIMPAN DATA TRANSAKSI KE SESSION
        # ============================================================

        # Simpan semua data pembayaran ke session
        # Data ini akan digunakan untuk:
        # 1. Display rincian di halaman pembayaran
        # 2. Generate PDF struk
        # 3. Audit trail (bisa dipindah ke database nantinya)
        session["pembeli"] = {
            "nama": nama,  # Nama customer
            "cash": cash,  # Uang yang dibayar
            "subtotal": subtotal,  # Total sebelum diskon & pajak
            "ppn": ppn,  # Pajak 10%
            "diskon": diskon,  # Diskon 10%
            "total": total,  # Total akhir
            "kembalian": kembalian,  # Uang kembali
        }

        # CRITICAL: Mark session as modified
        # Tanpa ini, data pembeli tidak akan tersimpan
        session.modified = True

        # ============================================================
        # STEP 9: RETURN SUCCESS RESPONSE
        # ============================================================

        # Return semua data pembayaran ke frontend
        # Frontend akan display data ini di rincian pembayaran
        # dan enable tombol download struk
        return jsonify(
            {
                "nama": nama,
                "cash": cash,
                "subtotal": subtotal,
                "ppn": ppn,
                "diskon": diskon,
                "total": total,
                "kembalian": kembalian,
            }
        )

    # ============================================================
    # EXCEPTION HANDLING
    # ============================================================

    except Exception as e:
        # Catch-all untuk unexpected errors
        # Log error untuk debugging
        app.logger.error(f"Error in checkout: {str(e)}")

        # Return generic error message
        # Jangan expose detail error untuk security
        return jsonify({"error": "Internal server error"}), 500


# ========================================================================
# API ENDPOINT - CLEAR CART
# ========================================================================


@app.route("/cart/clear", methods=["POST"])
@login_required
def cart_clear():
    """
    Endpoint untuk menghapus semua item dari cart

    Fungsi ini:
    1. Mengosongkan cart (set ke empty list)
    2. Reset cart count ke 0
    3. Mark session as modified
    4. Return success response

    Use Cases:
        - User klik tombol "Clear All" / "Hapus Semua"
        - Memulai transaksi baru setelah pembayaran
        - Cancel order dan start over

    Request:
        POST /cart/clear
        (No body required)

    Response (JSON):
        {
            "success": true
        }

    Note:
        - Tidak ada validasi atau error handling khusus
        - Operation selalu berhasil (idempotent)
        - Memanggil endpoint ini multiple times aman
    """

    # Kosongkan cart dengan set ke empty list
    # Ini akan menghapus semua items yang ada
    # Previous cart data akan lost (tidak bisa undo)
    session["jumlahcart"] = []

    # Reset cart count badge ke 0
    # Ini untuk update icon cart counter di navbar
    session["cart_count"] = 0

    # CRITICAL: Mark session as modified
    # Tanpa ini, cart tidak akan ter-clear di server
    session.modified = True

    # Return success response
    # Frontend akan:
    # 1. Clear display cart items
    # 2. Reset all totals to "-" or 0
    # 3. Reset form inputs
    # 4. Update badge counter
    # 5. Show success message (optional)
    return jsonify({"success": True})


# ========================================================================
# API ENDPOINT - DOWNLOAD STRUK PDF
# ========================================================================


@app.route("/generate_struk", methods=["POST"])
@login_required
def generate_struk():
    """
    Generate dan download PDF struk pembayaran format thermal (80mm)
    Format struk seperti Indomaret/Alfamart
    """

    try:
        # ============================================================
        # STEP 1-4: VALIDASI & PERHITUNGAN (Sama seperti sebelumnya)
        # ============================================================

        cart = session.get("jumlahcart", [])
        if not cart:
            return jsonify({"error": "Keranjang kosong"}), 400

        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        nama = data.get("nama", "").strip()

        try:
            cash = int(data.get("cash", 0))
        except (ValueError, TypeError):
            return jsonify({"error": "Jumlah uang tidak valid"}), 400

        subtotal = sum(item["price"] * item["qty"] for item in cart)
        diskon, ppn, total = hitung_total(subtotal)
        kembalian = cash - total

        if cash < total:
            return jsonify({"error": "Uang tidak cukup"}), 400

        # ============================================================
        # STEP 5: INISIALISASI PDF - THERMAL SIZE (80mm width)
        # ============================================================

        buffer = io.BytesIO()

        # THERMAL PAPER SIZE
        # 80mm width = 226.77 points (80mm * 72/25.4)
        # Height flexible untuk accommodate content
        # Common thermal: 80mm x 200mm or longer
        THERMAL_WIDTH = 226.77  # 80mm in points
        THERMAL_HEIGHT = 600  # Flexible height, akan adjust otomatis

        pdf = canvas.Canvas(buffer, pagesize=(THERMAL_WIDTH, THERMAL_HEIGHT))

        # ============================================================
        # MARGINS & POSITIONING untuk thermal receipt
        # ============================================================

        LEFT_MARGIN = 10  # 10 points from left
        RIGHT_MARGIN = 216.77  # 10 points from right (226.77 - 10)
        CENTER_X = THERMAL_WIDTH / 2  # 113.385 points

        # Start from top
        y = THERMAL_HEIGHT - 70  # Start 40 points from top

        # ============================================================
        # STEP 6: HEADER - LOGO (Smaller, centered)
        # ============================================================

        try:
            logo = ImageReader("static/img/LogoUBSI.png")

            # Logo lebih kecil untuk thermal receipt
            logo_size = 60  # 50x50 points
            logo_x = (THERMAL_WIDTH - logo_size) / 2  # Center horizontally

            pdf.drawImage(
                logo,
                logo_x,
                y,
                width=logo_size,
                height=logo_size,
                preserveAspectRatio=True,
            )
            y -= 20  # Move down after logo

        except Exception as e:
            app.logger.warning(f"Logo not found: {str(e)}")

        # ============================================================
        # STEP 7: HEADER - STORE NAME & INFO
        # ============================================================

        # Store name - Bold, slightly larger
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawCentredString(CENTER_X, y, "RESTORAN KELOMPOK 3")
        y -= 15

        # Address - Smaller font for thermal
        pdf.setFont("Helvetica", 7)

        # Multi-line address untuk thermal receipt
        address_lines = [
            "Cikarang Square",
            "Jl. Cibarusah Raya No.168",
            "Pasirsari, Cikarang Sel",
            "Kab.Bekasi, Jawa Barat 17550",
        ]

        for line in address_lines:
            pdf.drawCentredString(CENTER_X, y, line)
            y -= 10

        # Date & Time
        pdf.drawCentredString(
            CENTER_X, y, datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        )
        y -= 15

        # Separator line
        pdf.setLineWidth(0.5)
        pdf.line(LEFT_MARGIN, y, RIGHT_MARGIN, y)
        y -= 15

        # ============================================================
        # STEP 8: CUSTOMER NAME
        # ============================================================

        pdf.setFont("Helvetica", 8)
        pdf.drawString(LEFT_MARGIN, y, f"Customer : {nama}")
        y -= 15

        # Separator
        pdf.line(LEFT_MARGIN, y, RIGHT_MARGIN, y)
        y -= 15

        # ============================================================
        # STEP 9: ITEMS LIST
        # ============================================================

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(LEFT_MARGIN, y, "PESANAN")
        pdf.drawRightString(RIGHT_MARGIN, y, "TOTAL")
        y -= 12

        # Thin separator
        pdf.setLineWidth(0.3)
        pdf.line(LEFT_MARGIN, y, RIGHT_MARGIN, y)
        y -= 12

        # Items - Regular font
        pdf.setFont("Helvetica", 8)

        for item in cart:
            # Item name
            item_name = item["nama"]

            # Truncate long names untuk fit thermal width
            # if len(item_name) > 25:
            #     item_name = item_name[:22] + "..."

            pdf.drawString(LEFT_MARGIN, y, item_name)
            y -= 10

            # Quantity and price on next line, indented
            qty_price_text = f"  {item['qty']} x Rp {item['price']:,}"
            item_total = item["price"] * item["qty"]

            pdf.drawString(LEFT_MARGIN, y, qty_price_text)
            pdf.drawRightString(RIGHT_MARGIN, y, f"Rp {item_total:,}")
            y -= 15

            # Check if need new page (thermal roll continues)
            if y < 100:
                pdf.showPage()
                y = THERMAL_HEIGHT - 40

        # ============================================================
        # STEP 10: TOTALS SECTION
        # ============================================================

        # Separator before totals
        pdf.setLineWidth(0.5)
        pdf.line(LEFT_MARGIN, y, RIGHT_MARGIN, y)
        y -= 15

        pdf.setFont("Helvetica", 8)

        # Subtotal
        pdf.drawString(LEFT_MARGIN, y, "Subtotal")
        pdf.drawRightString(RIGHT_MARGIN, y, f"Rp {subtotal:,}")
        y -= 12

        # Discount
        pdf.drawString(LEFT_MARGIN, y, "Diskon (10%)")
        pdf.drawRightString(RIGHT_MARGIN, y, f"Rp {diskon:,}")
        y -= 12

        # Tax
        pdf.drawString(LEFT_MARGIN, y, "PPN (10%)")
        pdf.drawRightString(RIGHT_MARGIN, y, f"Rp {ppn:,}")
        y -= 15

        # Bold separator for total
        pdf.setLineWidth(1)
        pdf.line(LEFT_MARGIN, y, RIGHT_MARGIN, y)
        y -= 15

        # TOTAL - Bold and larger
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(LEFT_MARGIN, y, "TOTAL")
        pdf.drawRightString(RIGHT_MARGIN, y, f"Rp {total:,}")
        y -= 15

        # Separator
        pdf.setLineWidth(0.5)
        pdf.line(LEFT_MARGIN, y, RIGHT_MARGIN, y)
        y -= 15

        # Payment details
        pdf.setFont("Helvetica", 8)
        pdf.drawString(LEFT_MARGIN, y, "Bayar")
        pdf.drawRightString(RIGHT_MARGIN, y, f"Rp {cash:,}")
        y -= 12

        pdf.drawString(LEFT_MARGIN, y, "Kembali")
        pdf.drawRightString(RIGHT_MARGIN, y, f"Rp {kembalian:,}")
        y -= 20

        # ============================================================
        # STEP 11: FOOTER
        # ============================================================

        # Separator
        pdf.setLineWidth(0.5)
        pdf.line(LEFT_MARGIN, y, RIGHT_MARGIN, y)
        y -= 15

        # Thank you message - centered
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawCentredString(CENTER_X, y, "TERIMA KASIH")
        y -= 10

        pdf.setFont("Helvetica", 7)
        pdf.drawCentredString(CENTER_X, y, "Atas Kunjungan Anda")
        y -= 15

        # Footer info
        pdf.setFont("Helvetica", 6)
        pdf.drawCentredString(CENTER_X, y, "Powered by Kelompok 3")
        y -= 10

        pdf.drawCentredString(
            CENTER_X, y, f"Struk: {datetime.datetime.now().strftime('%d%m%Y%H%M%S')}"
        )

        # ============================================================
        # STEP 12-18: FINALIZE & RETURN (Sama seperti sebelumnya)
        # ============================================================

        pdf.showPage()
        pdf.save()
        buffer.seek(0)

        print("PDF SIZE:", buffer.getbuffer().nbytes)

        tanggal = datetime.datetime.now().strftime("%d-%m-%Y-%H%M%S")
        fileDownload = f"struk-{tanggal}.pdf"

        response = send_file(
            buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=fileDownload,
        )

        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers["Content-Disposition"] = (
            f'attachment; filename="{fileDownload}"'
        )
        response.headers["Content-Length"] = str(buffer.getbuffer().nbytes)

        return response

    except Exception as e:
        print("ERROR:", e)

        if request.is_json:
            return jsonify({"error": str(e)}), 500
        else:
            return f"<html><body><h1>Error: {str(e)}</h1></body></html>", 500


# ========================================================================
# API ENDPOINT - GET CART FROM SESSION
# ========================================================================


@app.route("/cart/get", methods=["GET"])
@login_required
def cart_get():
    """
    Retrieve current cart from session

    Endpoint ini mengatasi masalah:
    "Cart hilang setelah page refresh"

    Problem:
        - JavaScript variables = client-side memory
        - Page refresh → JavaScript reset
        - Cart data hilang dari frontend

    Solution:
        - Cart tersimpan di server session
        - Page load → JavaScript call /cart/get
        - Backend return cart dari session
        - Frontend restore display

    Use Cases:
        1. Page refresh - restore cart state
        2. Initial page load - check existing cart
        3. After session restore - sync frontend-backend

    Request:
        GET /cart/get
        (No parameters required)

    Response (JSON):
        Success (200):
        {
            "cart": [...],        # List of items dengan qty, price, dll
            "count": 5,           # Total quantity untuk badge counter
            "subtotal": 100000,   # Total sebelum diskon
            "diskon": 10000,      # Diskon amount
            "ppn": 9000,          # Pajak amount
            "total": 99000        # Final total
        }

        Error (500):
        {
            "error": "Internal server error"
        }
    """

    try:
        # ============================================================
        # STEP 1: LOAD CART FROM SESSION
        # ============================================================

        # Ambil cart dari server session
        # session = Flask's secure cookie-based session
        # Default empty list jika:
        # - Session baru (first visit)
        # - Cart sudah di-clear
        # - Session expired
        cart = session.get("jumlahcart", [])

        # ============================================================
        # STEP 2: CALCULATE TOTALS
        # ============================================================

        # Hitung semua totals even jika cart kosong
        # Jika cart = [], calculate_totals akan return (0, 0, 0, 0)
        # Ini lebih consistent daripada conditional calculation
        subtotal, diskon, ppn, total = calculate_totals(cart)

        # ============================================================
        # STEP 3: RETURN JSON RESPONSE
        # ============================================================

        # Return JSON dengan format yang sama seperti /cart/update
        # API consistency = easier frontend implementation
        return jsonify(
            {
                "cart": cart,  # List semua items
                "count": sum(i["qty"] for i in cart),  # Total qty untuk badge
                "subtotal": subtotal,  # Total before discount
                "diskon": diskon,  # Discount amount
                "ppn": ppn,  # Tax amount
                "total": total,  # Final total
            }
        )

    # ============================================================
    # EXCEPTION HANDLING
    # ============================================================

    except Exception as e:
        # Catch unexpected errors
        # Possible causes:
        # - Session corruption
        # - Calculate error
        # - JSON serialization error

        # Log error untuk debugging
        # app.logger.error() write ke Flask log file
        # Includes timestamp, severity level, message
        app.logger.error(f"Error in cart_get: {str(e)}")

        # Return generic error response
        # Status 500 = Internal Server Error
        # Frontend akan display error message ke user
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
