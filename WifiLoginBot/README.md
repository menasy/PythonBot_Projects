# Python Captive Portal Bot 🚀

Bu proje, tekrarlayan captive portal (zorunlu Wi-Fi giriş ekranı) formunu otomatikleştirmek amacıyla Python ve Selenium kullanılarak geliştirilmiştir. Bot, bir web tarayıcısını otonom olarak kontrol ederek kullanıcı bilgilerini girer, gerekli sözleşmeleri onaylar ve ağa bağlantıyı tamamlar.

## ⚙️ Temel İşlevler

- **Form Doldurma:** Gerekli form alanlarını (`.env` dosyasından okunan bilgilerle) otomatik olarak doldurur.
- **Etkileşim Simülasyonu:** "Kullanım Şartları" ve "KVKK Metni" gibi linklere tıklar.
- **Popup Yönetimi:** Açılan sözleşme pencerelerini (popup/modal) otomatik olarak kapatır.
- **Koşullu Onay:** Sadece sözleşmeler okunduktan sonra aktif hale gelen onay kutularını (checkbox) işaretler.
- **Ağa Bağlanma:** Tüm adımlar tamamlandıktan sonra "Bağlan" butonuna basarak işlemi sonlandırır.

## 🔧 Kullanılan Teknolojiler

- **Dil:** Python 3.x
- **Otomasyon Kütüphanesi:** Selenium
- **Tarayıcı Sürücüsü:** ChromeDriver
- **Gizli Bilgi Yönetimi:** Python-Dotenv

---

## 🏁 Kurulum ve Başlangıç Rehberi

Bu projeyi yerel makinenizde kurmak ve çalıştırmak için aşağıdaki adımları izleyin.

### 1. Ön Gereksinimler

- **Python 3:** Bilgisayarınızda Python 3'ün kurulu olduğundan emin olun. [Python'u İndir](https://www.python.org/downloads/)
- **Google Chrome:** Selenium'un kontrol edebilmesi için Google Chrome tarayıcısı gereklidir. [Chrome'u İndir](https://www.google.com/chrome/)

### 2. Projeyi Klonlama

Projeyi bilgisayarınıza klonlayın ve proje klasörüne gidin:
```bash
git clone [https://github.com/menasy/PythonFormBot.git](https://github.com/menasy/PythonFormBot.git)
cd PythonFormBot
```
### 3. Sanal Ortam (.venv) Kurulumu

Projenin bağımlılıklarını sisteminizden izole etmek için bir sanal ortam oluşturup aktif hale getirin.

**a) Sanal Ortamı Oluşturma (Tüm İşletim Sistemleri):**
```bash
python -m venv .venv
```

**b) Sanal Ortamı Aktif Etme:**
- **Windows (CMD/PowerShell):**
  ```powershell
  .\.venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```
Komut satırınızın başında `(.venv)` ifadesini gördüğünüzde sanal ortam aktif demektir.

### 4. Gerekli Kütüphaneleri Yükleme

Projenin ihtiyaç duyduğu Python kütüphanelerini `requirements.txt` dosyasından yükleyin.

```bash
pip install -r requirements.txt
```
> **Not:** `requirements.txt` dosyası, `selenium` ve `python-dotenv` kütüphanelerini içermelidir.

### 5. ChromeDriver İndirme

Selenium'un Chrome'u kontrol edebilmesi için ChromeDriver'a ihtiyacı vardır.

**a) Chrome Sürümünüzü Öğrenin:** Chrome tarayıcınızda `Ayarlar > Chrome Hakkında` bölümünden sürüm numaranızı kontrol edin.

**b) ChromeDriver'ı İndirin:**
- [**Resmi ChromeDriver İndirme Sayfası (Chrome for Testing)**](https://googlechromelabs.github.io/chrome-for-testing/)

Yukarıdaki linkten, Chrome sürümünüze en yakın olan **Stable** versiyonu bulun ve işletim sisteminize uygun olan dosyayı indirin:
- **Windows:** `chromedriver-win64.zip`
- **Linux:** `chromedriver-linux64.zip`


**c) Dosyayı Proje Klasörüne Taşıyın:**
İndirdiğiniz `.zip` dosyasını açın ve içindeki `chromedriver.exe` (Windows için) veya `chromedriver` (macOS/Linux için) dosyasını projenizin ana klasörüne, `wifi_login.py` ile aynı yere kopyalayın.

### 6. Gerekli Kütüphaneleri Manuel Olarak Yükleme (Alternatif)
**d) Kütüphaneleri Yükleme:**
```bash
pip install selenium
pip install python-dotenv
```

### 7. Kişisel Bilgileri Yapılandırma (`.env` dosyası)

Kişisel bilgilerinizi güvenli bir şekilde saklamak için projenin ana klasöründe **`.env`** adında bir dosya oluşturun ve içine aşağıdaki bilgileri girin:

```env
# Bu dosyayı kendi bilgilerinizle doldurun
TC_ID = "11111111111"
NAME = "Mehmet Nasim"
SURNAME = "Yılmaz"
BIRTH_YEAR = "1907"
```
---

## 🚀 Script'i Çalıştırma

Tüm kurulum adımları tamamlandıktan sonra, sanal ortamınızın aktif olduğundan emin olun (`(.venv)` yazısını görmelisiniz) ve aşağıdaki komutla botu çalıştırın:
```bash
python wifi_login.py
```

---