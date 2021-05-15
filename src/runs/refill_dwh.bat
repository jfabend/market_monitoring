python .\src\runs\run_upload.py -i "C:\Data\Trading\market_monitoring\data"
python .\src\db\dateformat_transformation.py
python .\src\runs\run_core_update.py
python .\src\runs\run_dim_time_upload.py