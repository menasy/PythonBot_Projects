@echo off
chcp 65001 > nul
title WiFi Otomatik Bağlantı
color 0A

echo.
echo ╔═══════════════════════════════════════╗
echo ║   WiFi Otomatik Bağlantı Başlatılıyor ║
echo ╚═══════════════════════════════════════╝
echo.

cd /d "%~dp0"

if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Sanal ortam bulunamadı!
    echo Lütfen önce: python -m venv .venv
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

python wifi_login.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Program başarıyla tamamlandı!
) else (
    echo.
    echo ❌ Program hata ile sonlandı!
)

echo.
echo Pencere 3 saniye içinde kapanacak...
timeout /t 3 /nobreak > nul