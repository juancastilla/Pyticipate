REM SET PYTHON_PATH=%PYTHON_PATH%;C:\SourceCode\CC\simcopiapo;C:\SourceCode\CC\pyticipate;
SET PYTHON_PATH=%PYTHON_PATH%;C:\SourceCode\CC\simrapel;C:\SourceCode\CC\pyticipate;
SET FLASK_ENV=development
SET FLASK_DEBUG=1
SET SCENARIO_LANG=en-au
SET SCENARIO_PY=C:\SourceCode\CC\pyticipate\demo\scenario.py
REM SET SCENARIO_PY=C:\SourceCode\CC\simrapel\scenario_SIMR.py
REM SET SCENARIO_PY=C:\SourceCode\CC\simcopiapo\scenario_SIMC.py
REM SET FLASK_APP=scenario_webapi.py
python C:\SourceCode\CC\pyticipate\scenario_webapi.py