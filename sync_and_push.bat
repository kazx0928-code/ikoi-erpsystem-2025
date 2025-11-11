@echo off
chcp 65001 >nul
set "PROJECT_DIR=%USERPROFILE%\Desktop\ikoi_rent_receipt_project"
set "SYNC_FILE=%PROJECT_DIR%\sync_report.txt"

cd /d "%PROJECT_DIR%"

echo ======================================== > "%SYNC_FILE%"
echo いこい住宅ERP 自動同期&Gitプッシュレポート >> "%SYNC_FILE%"
echo 実行日時: %DATE% %TIME% >> "%SYNC_FILE%"
echo ======================================== >> "%SYNC_FILE%"

echo [環境情報] >> "%SYNC_FILE%"
python --version >> "%SYNC_FILE%" 2>&1
pip list >> "%SYNC_FILE%" 2>&1
echo %PATH% >> "%SYNC_FILE%"

echo [ファイル集約] >> "%SYNC_FILE%"
move "%USERPROFILE%\Desktop\*.py" "%PROJECT_DIR%\" 2>nul >> "%SYNC_FILE%"
move "%USERPROFILE%\Desktop\*.bat" "%PROJECT_DIR%\" 2>nul >> "%SYNC_FILE%"
move "%USERPROFILE%\Desktop\*.sh" "%PROJECT_DIR%\" 2>nul >> "%SYNC_FILE%"
xcopy "%USERPROFILE%\Desktop\receipts_pdf" "%PROJECT_DIR%\receipts_pdf" /E /I /Y 2>nul >> "%SYNC_FILE%"
xcopy "%USERPROFILE%\Desktop\ikoi_erp_db" "%PROJECT_DIR%\ikoi_erp_db" /E /I /Y 2>nul >> "%SYNC_FILE%"

echo [Gitプッシュ] >> "%SYNC_FILE%"
git add . >> "%SYNC_FILE%" 2>&1
git commit -m "auto: 環境同期&ファイル集約 %DATE% %TIME%" >> "%SYNC_FILE%" 2>&1
git push origin feature/owner-rent-receipt-v1 >> "%SYNC_FILE%" 2>&1

echo ======================================== >> "%SYNC_FILE%"
echo 自動同期&プッシュ完了！！ >> "%SYNC_FILE%"
echo ======================================== >> "%SYNC_FILE%"

start notepad "%SYNC_FILE%"
explorer "%PROJECT_DIR%"

echo 完了！！レポート確認してね！！
pause