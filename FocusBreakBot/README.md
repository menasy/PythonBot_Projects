# 💠 FocusBreak Bot

Kişisel üretkenliği artırmak için tasarlanmış minimalist Telegram botu:
- 👀 **Göz Molası:** Her 1 saatte bir kısa mola hatırlatır.
- 🕌 **Namaz Uyarısı:** Vakitlerden **40 dk önce** bildirim gönderir.
- 💬 **Komutlar:** `/start` (başlat), `/break` (durdur), `/stop` (kapat).
- 💾 **Kayıtlar:** Tüm olaylar `log.txt` dosyasına yazılır.
- 🪄 **Windows’ta Sessiz Çalışma:** `.bat` + `.vbs` ile arka planda.

---

## 📦 Proje Yapısı

```
FocusBreak_bot/
├── venv/                      # Sanal ortam
├── reminder_bot.py            # Ana bot dosyası
├── requirements.txt           # Python bağımlılıkları
├── .env                       # Ortam değişkenleri (kişisel)
├── .env.example               # Örnek .env
├── .gitignore                 # VCS hariç listesi
├── start_bot.bat              # Windows başlatma betiği
├── start_bot.vbs              # Sessiz (görünmez) başlatma
├── log.txt                    # Çalışma logları
└── README.md                  # proje dokümantasyonu
```

---

## 🧰 Gereksinimler

- **Windows 10/11**
- **Python 3.10+**
- **Telegram hesabı**
- İnternet bağlantısı

---

## 🤖 Telegram Bot Oluşturma (Kısaca)

1. Telegram’da **@BotFather** ile konuş → `/newbot`
2. İsim ve kullanıcı adı (username) ver → **Bot Token** al.
3. Botuna bir kez **/start** yaz (sohbeti başlatmak için).
4. **Chat ID** almak için:
   - Kolay yol: **@userinfobot**’a yaz → `Id:` satırını al.
   - Alternatif: Tarayıcıda şu endpoint’i aç (TOKEN’i değiştir):
     ```
     https://api.telegram.org/bot<TOKEN>/getUpdates
     ```
     Dönen JSON’daki `"chat":{"id": ...}` değeri chat_id’ndir.

> Bu değerleri `.env` içine koyacaksın (aşağıda).

---

## 🔐 Ortam Değişkenleri (.env)

Proje kökünde `/.env` dosyasını oluştur (veya `.env.example`’ı kopyalayıp düzenle):

```env
TG_BOT_TOKEN=1234567890:ABCDEF-GHIJKLMN_opQRStuvWXyz
TG_CHAT_ID=1234567890
VERCEL_PRAYER_TIME_API_URL=https://vakit.vercel.app/api/timesFromCoordinates?lat=41.0082&lng=28.9784
```

> `VERCEL_PRAYER_TIME_API_URL` İstanbul koordinatları ile gelir. Şehir değiştirirsen `lat`/`lng` değerlerini güncelle.

---

## 📦 Bağımlılıkların Kurulumu

Windows PowerShell’de (proje klasöründe):

```powershell
# Proje klasörüne geç (kendi dizinin)
cd <PROJE_KLASÖRÜ>

# Sanal ortam oluştur ve etkinleştir
python -m venv venv
venv\Scriptsctivate

# Bağımlılıkları kur
pip install -r requirements.txt
```

`requirements.txt` içeriği:

```txt
python-telegram-bot==13.15
apscheduler
requests
python-dotenv
```

---

## 🚀 Hızlı Çalıştırma (Geliştirme Modu)

```powershell
cd <PROJE_KLASÖRÜ>
venv\Scriptsctivate
python reminder_bot.py
```

Başlangıç mesajı Telegram’da **tek ve kısa** gelir:

```
💠 FocusBreak — 29 Ekim 2025

Komutlar:
• /start — Hatırlatıcıları başlat
• /break — Hatırlatıcıları durdur
• /stop — Programı kapat
```

---

## 🪄 Windows’ta Sessiz Arka Plan Başlatma

> Aşağıdaki betiklerde **mutlak dizin** yerine **kendi proje klasörü yolunu** kullan. Kullanıcı adın gibi kişisel bilgileri README’ye yazma.

### 1) `start_bot.bat`

```bat
@echo off
cd /d "<PROJE_KLASÖRÜ>"
start "" /min cmd /c "venv\Scripts\python.exe reminder_bot.py"
exit
```

### 2) `start_bot.vbs`

> **Önemli:** ANSI veya “UTF-8 (BOM’suz)” kaydet.

```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """<PROJE_KLASÖRÜ>\start_bot.bat""", 0
Set WshShell = Nothing
```

- `start_bot.vbs`’ye çift tıkla → bot pencere açmadan başlar.
- Otomatik başlatma için: **Win + R →** `shell:startup` → `start_bot.vbs`’yi bu klasöre kopyala.

---

## 🧭 Kullanım

Telegram’da bot sohbetinde şu komutları kullan:

- **`/start`** → Hatırlatıcıları başlatır (göz + namaz).
- **`/break`** → Tüm hatırlatıcıları durdurur; program açık kalır.
- **`/stop`** → Programı **tamamen kapatır**.

> Göz molası bildirimi **her 1 saatte bir** gelir.  
> Namaz uyarıları ilgili vakitten **40 dk önce** planlanır ve gönderilir.

---

## 🧪 Doğrulama / Test

- `.env` değerleri doğru mu? (Token + Chat ID)
- `requirements.txt` kuruldu mu? (`venv\Lib\site-packages` kontrol)
- API canlı mı? Tarayıcıda aç:
  ```
  https://vakit.vercel.app/api/timesFromCoordinates?lat=41.0082&lng=28.9784
  ```
- `log.txt` güncelleniyor mu? (komutlar ve planlamalar yazılır)

---

## 🛠 Yapılandırma İpuçları

- **Saat Dilimi:** Kod, `Europe/Istanbul` ile zamanlar için güvenli planlama yapar.
- **API Zaman Aşımı:** `requests.get(..., timeout=20)` ile ağ gecikmelerinde dayanıklı.
- **Çift Planlama Önleme:** Job ID’ler ile aynı gün tekrarlı planlama engellenir.
- **Gizlilik:** `TOKEN` ve `CHAT_ID`’yi depoya **asla** koyma. `.gitignore` bu yüzden var.

---

## 🧯 Sorun Giderme

- **VBS “Geçersiz karakter” hatası:** Dosyayı **ANSI** veya **UTF-8 (BOM’suz)** kaydet; akıllı tırnak (“ ”) kullanma.
- **VBS “Dosya bulunamadı”:** `start_bot.vbs` içindeki **.bat tam yolunu** kontrol et.
- **Mesaj gelmiyor:** Bot sohbetini **/start** ile başlat; `TG_CHAT_ID` doğru mu bak.
- **API formatı değişti:** `.env`’deki `VERCEL_PRAYER_TIME_API_URL` değerini yeniden doğrula.
- **Kapatma:** Telegram’da `/stop` yaz → süreç tamamen sonlanır.

---

## 📜 Lisans

MIT License © 2025 — **Mehmet Nasim Yılmaz**
