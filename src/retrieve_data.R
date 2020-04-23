#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
cat(paste0(c("Argument 1: ", args[1]), collapse = "") , sep = "\n")
cat(paste0(c("Argument 2: ", args[2]), collapse = "") , sep = "\n")

#args = "dax"
#setwd(".")


library(quantmod)
library(data.table)

#retrieve cmd argument input
symbol_temp <- toupper(args[1])
target_path <- paste0(c(args[2], "/", symbol_temp), collapse = "")

# download data
getSymbols(symbol_temp, src="yahoo", from = "1950-01-01", to = Sys.Date())
kurs <- data.table(index(get(symbol_temp)), get(symbol_temp))

# rename columns
headers <- colnames(kurs)
headers_clean <- gsub("V1", "datum", headers)
colnames(kurs) <- headers_clean

# get from to dates for filename
from_date <- as.character(kurs[1, datum])
to_date <- as.character(kurs[.N, datum])

filename <- paste0(c(target_path,"/", from_date, "_", to_date, ".csv"), collapse = "")
dir.create(target_path, showWarnings = FALSE)
write.csv(kurs, filename, row.names = F)
