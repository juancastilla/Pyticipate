IF EXIST "%cd%\working" (
    RMDIR /S /Q "%cd%\working"
)
IF NOT EXIST "%cd%\working" (
    MKDIR "%cd%\working"
)
START /min CMD /k SERVER.BAT
TIMEOUT /t 5
CALL Electron\electron.exe Source\pyticipate\electron\main.js