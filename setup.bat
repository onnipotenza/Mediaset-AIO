@echo off
setlocal

REM Create the drivers folder if it doesn't exist
if not exist "drivers" mkdir "drivers"

REM Change directory to the drivers folder
cd "drivers"

REM Download Chrome driver using PowerShell
echo Downloading Chrome driver...
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/win64/chromedriver-win64.zip', 'chromedriver-win64.zip')"

REM Extract Chrome driver
echo Extracting Chrome driver...
powershell -Command "Expand-Archive -Path 'chromedriver-win64.zip' -DestinationPath '.\' -Force"
del "chromedriver-win64.zip"

REM Download ffmpeg using PowerShell
echo Downloading ffmpeg...
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.0-full_build.7z', 'ffmpeg-7.0-full_build.7z')"

REM Extract ffmpeg using 7-Zip
echo Extracting ffmpeg...
7z x -y "ffmpeg-7.0-full_build.7z" -o"ffmpeg-7.0-full_build"
del "ffmpeg-7.0-full_build.7z"

REM Download yt-dlp.exe using PowerShell
echo Downloading yt-dlp...
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://github.com/yt-dlp/yt-dlp/releases/download/2024.03.10/yt-dlp.exe', 'yt-dlp.exe')"

REM Move Chrome driver executable
echo Moving Chrome driver executable...
move "chromedriver-win64\chromedriver.exe" "chromedriver.exe"
rmdir /s /q "chromedriver-win64"

REM Move ffmpeg driver executable
echo Moving ffmpeg executables...
move "ffmpeg-7.0-full_build\ffmpeg-7.0-full_build\bin\ffmpeg.exe" "ffmpeg.exe"
move "ffmpeg-7.0-full_build\ffmpeg-7.0-full_build\bin\ffplay.exe" "ffplay.exe"
move "ffmpeg-7.0-full_build\ffmpeg-7.0-full_build\bin\ffprobe.exe" "ffprobe.exe"
rmdir /s /q "ffmpeg-7.0-full_build"

REM Setup virtual environment and install dependencies
echo Setting up virtual environment...
cd ".."
py -m pip install virtualenv
py -m virtualenv venv 
call venv\Scripts\activate
echo Installing dependencies...
py -m pip install -r requirements.txt

echo Setup complete!
pause
