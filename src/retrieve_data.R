#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
cat(paste0(c("Argument 1: ", args[1]), collapse = "") , sep = "\n")
cat(paste0(c("Argument 2: ", args[2]), collapse = "") , sep = "\n")

#args = "dax"
#setwd(".")


library(quantmod)
library(data.table)

symbol_temp <- toupper(args[1])
target_path <- paste0(c(args[2], "/", symbol_temp), collapse = "")

getSymbols(symbol_temp, src="yahoo")
kurs <- data.table(index(get(symbol_temp)), get(symbol_temp)) 
filename <- paste0(c(target_path,"/", symbol_temp, ".csv"), collapse = "")
dir.create(target_path, showWarnings = FALSE)
write.csv(kurs, filename, row.names = F)
