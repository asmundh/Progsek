INSTALL

pip install -r requirements.txt

RUN

gunicorn --workers=2 vulnapp 
 
