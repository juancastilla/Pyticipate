set FLASK_ENV=development
set FLASK_DEBUG=1
set SCENARIO_LANG=es-cl
set SCENARIO_PY=scenario_SIMR.py
set GLOBAL_DATA_PY=global_data_SIMR.py
set FLASK_APP=../pyticipate/scenario_webapi.py
flask run --host 0.0.0.0 --port 5000 --with-threads