CALL conda env remove --name simrapel2
CALL conda create --name simrapel2 -y
CALL conda activate simrapel2
CALL conda install python=3.7 -y
CALL pip install numpy==1.16.4
CALL pip install pandas==0.24.2
CALL pip install flask==1.0.3 flask-headers
REM CALL pip install flopy==3.2.10
REM CALL pip install xlrd==1.2.0
CALL pip install ftfy==5.6
CALL pip install Installers\Python\Wheels\Fiona-1.8.6-cp37-cp37m-win_amd64.whl
CALL pip install Installers\Python\Wheels\GDAL-2.4.1-cp37-cp37m-win_amd64.whl
CALL pip install Installers\Python\Wheels\Shapely-1.6.4.post1-cp37-cp37m-win_amd64.whl
CALL pip install Installers\Python\Wheels\pyshp-2.1.0-py2.py3-none-any.whl
CALL pip install Installers\Python\Wheels\pyproj-1.9.6-cp37-cp37m-win_amd64.whl
CALL pip install Installers\Python\Wheels\geopandas-0.5.0-py2.py3-none-any.whl
CALL pip install Installers\Python\Wheels\rasterio-1.0.23-cp37-cp37m-win_amd64.whl
REM CALL pip install matplotlib==3.0.2
REM CALL pip install seaborn==0.9.0
REM CALL pip install python-docx==0.8.10
REM CALL pip install docxcompose==1.0.0a17
CALL conda deactivate
