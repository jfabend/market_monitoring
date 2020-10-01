import os

my_symbols = ["^GSPC"]
retrieve_r_cmd = "Rscript .\\src\\retrieve_data.r __symbol__ C:/Data/Trading/market_monitoring/apidata"

for symbol in my_symbols:
    cmd_string = retrieve_r_cmd.replace("__symbol__", symbol)
    os.system(cmd_string)