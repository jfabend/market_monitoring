
library(quantmod)
library(data.table)
library(readxl)
library(tidyverse)

symbol_temp <- "^SP500FTR"
getSymbols(symbol_temp, src="yahoo")
kurs_sp_f <- data.table(index(get("SP500FTR")), get("SP500FTR")) 



symbol_temp <- "NFLX"
getSymbols(symbol_temp, src="yahoo")
kurs <- data.table(index(get(symbol_temp)), get(symbol_temp)) 
