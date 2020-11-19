CALL conda activate simrapel2
SET PYTHON_PATH=%PYTHON_PATH%;%cd%\Source\simrapel;%cd%\Source\pyticipate
SET SCENARIO_LANG=es-cl
SET SCENARIO_PY=%cd%\Source\simrapel\scenario_SIMR.py
set GLOBAL_DATA_PY=%cd%\Source\simrapel\global_data_SIMR.py
python "%cd%\Source\pyticipate\scenario_webapi.py"
