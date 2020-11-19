CALL conda activate simcopiapo
SET PYTHON_PATH=%PYTHON_PATH%;%cd%\Source\simcopiapo;%cd%\Source\pyticipate
SET SCENARIO_LANG=es-cl
SET SCENARIO_PY=%cd%\Source\simcopiapo\scenario_SIMC.py
python "%cd%\Source\pyticipate\scenario_webapi.py"
