const Section = document.getElementById("zx__container");
const LinkDaftar = document.getElementById("LinkToRegis");
const LinkLogin = document.getElementById("LinkToLogin");

LinkDaftar.onclick = () => {
  Section.classList.add("zx__Animate");
};

LinkLogin.onclick = () => {
  Section.classList.remove("zx__Animate");
};

document.addEventListener("DOMContentLoaded", () => {
  const quotes = [
    "Hidup ini seperti sepeda, untuk tetap seimbang, kita harus terus bergerak.",
    "Pergi ke tempat yang belum pernah Anda kunjungi setidaknya sekali dalam hidup Anda.",
    "Hidup bukanlah tentang menunggu badai berlalu, tetapi tentang belajar bagaimana berdansa di hujan.",
    "Jangan hanya menjadi pengikut jejak orang lain; buatlah jejak Anda sendiri.",
    "Jangan takut gagal. Takutlah untuk tidak mencoba.",
    "Hidup adalah tentang membuat keputusan. Berani mengambil risiko dan tidak pernah menyesalinya.",
    "Ketika Anda berhenti bermimpi, Anda berhenti hidup.",
    "Ketika semuanya tampak gelap, ingatlah bahwa itu adalah hanya malam sebelum fajar.",
  ];

  let index = 0;
  const quoteText = document.querySelectorAll(".quoteText");

  function updateQuotes() {
    quoteText.forEach((el) => {
      el.innerText = quotes[index];
    });
    index = (index + 1) % quotes.length;
  }

  updateQuotes();
  setInterval(updateQuotes, 4000);
});

window.addEventListener("DOMContentLoaded", () => {
  if (window.innerWidth < 992) {
    const alertEl = document.getElementById("mobileAlert");
    const parent = document.getElementById("parentMobileAlert");
    const box = alertEl.querySelector(".alertBox");

    // tampilkan
    alertEl.classList.remove("d-none");
    parent.classList.remove("d-none");
    box.classList.add("show");
  }
});

// 1. Munculin alert langsung
const alertLogin = document.getElementById("alertlogin");
if (alertLogin) {
  alertLogin.classList.remove("d-none");
}

// 2. Sembunyikan setelah 4 detik
setTimeout(() => {
  if (alertLogin) {
    alertLogin.classList.add("d-none");
  }
}, 3000);

document.getElementById("loginForm").addEventListener("submit", function (e) {
  e.preventDefault(); // cegat submit asli

  const btn = document.getElementById("zx__SubmitLogin");

  // Ubah tombol → loading
  btn.innerHTML = `<span class="spinner-border spinner-border-md" aria-hidden="true"></span>`;
  btn.disabled = true;
  btn.style.pointerEvents = "none";

  // Delay 4 detik → submit manual
  setTimeout(() => {
    this.submit(); // submit form beneran
  }, 3000);
});
