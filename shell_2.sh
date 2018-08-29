ls_date=`date +%Y%m%d`
pg_dump -h 127.0.0.1 -U postgres postgres > /home/dbsave/postgres_save${ls_date}.bak
echo "DB saved."
python daily_info_script.py
