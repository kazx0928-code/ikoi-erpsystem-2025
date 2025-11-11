@echo off
cd /d "%~dp0"
git fetch origin feature/owner-rent-receipt-v1
git reset --hard origin/feature/owner-rent-receipt-v1
echo.
echo ========================================
echo 仮想と実機が完全に一致しました！！
echo rent_receipt_main.py が最新版になりました！
echo ========================================
echo.
pause