
# ███▄ ▄███▓▓█████  ███▄    █  ▄▄▄        ██████▓██   ██▓
#▓██▒▀█▀ ██▒▓█   ▀  ██ ▀█   █ ▒████▄    ▒██    ▒ ▒██  ██▒
#▓██    ▓██░▒███   ▓██  ▀█ ██▒▒██  ▀█▄  ░ ▓██▄    ▒██ ██░
#▒██    ▒██ ▒▓█  ▄ ▓██▒  ▐▌██▒░██▄▄▄▄██   ▒   ██▒ ░ ▐██▓░
#▒██▒   ░██▒░▒████▒▒██░   ▓██░ ▓█   ▓██▒▒██████▒▒ ░ ██▒▓░
#░ ▒░   ░  ░░░ ▒░ ░░ ▒░   ▒ ▒  ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░  ██▒▒▒
#░  ░      ░ ░ ░  ░░ ░░   ░ ▒░  ▒   ▒▒ ░░ ░▒  ░ ░▓██ ░▒░
#░      ░      ░      ░   ░ ░   ░   ▒   ░  ░  ░  ▒ ▒ ░░
#       ░      ░  ░         ░       ░  ░      ░  ░ ░
#                                                ░ ░
# wifi-automation
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv
import os

load_dotenv()

# Kullanıcı Bilgileri (.env dosyasından)
TC_KIMLIK_NO = os.getenv("TC_ID")
AD = os.getenv("NAME")
SOYAD = os.getenv("SURNAME")
DOGUM_YILI = os.getenv("BIRTH_YEAR")

# URL Ayarı
WIFI_URL = sys.argv[1] if len(sys.argv) > 1 else "http://github.com/menasy"

# Chrome Ayarları
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

service = webdriver.ChromeService()
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 20)

try:
    print("🌐 WiFi otomatik giriş başlatılıyor...")
    driver.get(WIFI_URL)
    time.sleep(4)
    
    # Form Kontrolü ve Yönlendirme
    form_found = False
    for attempt in range(5):
        try:
            driver.find_element(By.XPATH, "//input[@id='idnumber']")
            form_found = True
            break
        except NoSuchElementException:
            try:
                redirect_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Bağlan')]")
                windows_before = len(driver.window_handles)
                driver.execute_script("arguments[0].click();", redirect_button)
                time.sleep(3)
                
                if len(driver.window_handles) > windows_before:
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(2)
                
                try:
                    driver.find_element(By.XPATH, "//input[@id='idnumber']")
                    form_found = True
                    break
                except NoSuchElementException:
                    time.sleep(2)
            except NoSuchElementException:
                time.sleep(2)
    
    if not form_found:
        raise Exception("❌ Login formu bulunamadı!")
    
    print("✓ Login formu yüklendi")

    # Form Doldurma
    print("\n📝 Form bilgileri giriliyor...")
    wait.until(EC.visibility_of_element_located((By.ID, "idnumber"))).send_keys(TC_KIMLIK_NO)
    driver.find_element(By.ID, "name").send_keys(AD)
    driver.find_element(By.ID, "surname").send_keys(SOYAD)
    driver.find_element(By.ID, "birthyear").send_keys(DOGUM_YILI)
    print("✓ Form dolduruldu")
    time.sleep(1)

    # Birinci Sözleşme
    print("\n📄 Hizmet sözleşmesi işleniyor...")
    sozlesme1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//form//div[2]//label//u//a")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sozlesme1)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", sozlesme1)
    time.sleep(2)
    
    kapat1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//form//div[1]//button[@data-dismiss='modal']")))
    driver.execute_script("arguments[0].click();", kapat1)
    time.sleep(1.5)
    
    checkbox1 = wait.until(EC.presence_of_element_located((By.XPATH, "//form//div[2]//input[@type='checkbox']")))
    time.sleep(0.5)
    if not driver.execute_script("return arguments[0].checked;", checkbox1):
        driver.execute_script("arguments[0].click();", checkbox1)
        time.sleep(0.5)
    print("✓ Hizmet sözleşmesi onaylandı")

    # İkinci Sözleşme (KVKK)
    print("\n🔒 KVKK sözleşmesi işleniyor...")
    try:
        sozlesme2 = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div[4]/div/div/div/div[1]/form/div[4]/div/label/u/a")
        ))
    except:
        sozlesme2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//form//div[4]//label//u//a")))
    
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sozlesme2)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", sozlesme2)
    time.sleep(2.5)
    
    try:
        kapat2 = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div[4]/div/div/div/div[1]/form/div[3]/div/div/div[3]/button")
        ))
    except:
        kapat2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//form//div[3]//button[@data-dismiss='modal']")))
    
    driver.execute_script("arguments[0].click();", kapat2)
    time.sleep(1.5)
    
    try:
        checkbox2 = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/div[4]/div/div/div/div[1]/form/div[4]/div/input")
        ))
    except:
        checkbox2 = wait.until(EC.presence_of_element_located((By.ID, "agree-kvkk")))
    
    time.sleep(0.5)
    if not driver.execute_script("return arguments[0].checked;", checkbox2):
        driver.execute_script("arguments[0].click();", checkbox2)
        time.sleep(0.5)
    print("✓ KVKK sözleşmesi onaylandı")

    # Bağlan
    print("\n🔌 WiFi'ye bağlanılıyor...")
    baglan = wait.until(EC.element_to_be_clickable((By.XPATH, "//form//div[5]/button[contains(@class, 'connect-btn')]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", baglan)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", baglan)
    print("✓ Bağlantı isteği gönderildi")
    
    # Bağlantı Kontrolü
    print("\n⏳ Bağlantı kuruluyor (40 saniye)...")
    time.sleep(40)
    
    try:
        driver.get("http://www.github.com/menasy")
        if "github.com/menasy" in driver.current_url:
            print("\n✅ İnternet bağlantısı başarılı!")
        else:
            print("\n⚠️  Bağlantı durumu belirsiz")
    except:
        print("\n⚠️  Bağlantı testi yapılamadı")
    
    time.sleep(5)

except TimeoutException:
    print(f"\n❌ Zaman aşımı! Son URL: {driver.current_url}")
    try:
        driver.save_screenshot(f"error_{int(time.time())}.png")
        print("📸 Hata ekran görüntüsü kaydedildi")
    except:
        pass
    input("\nDevam etmek için Enter'a basın...")

except Exception as e:
    print(f"\n❌ Hata: {e}")
    try:
        driver.save_screenshot(f"error_{int(time.time())}.png")
        print("📸 Hata ekran görüntüsü kaydedildi")
    except:
        pass
    input("\nDevam etmek için Enter'a basın...")

finally:
    driver.quit()
    print("\n👋 Program sonlandırıldı")