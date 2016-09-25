library(ggplot2)
library(stringr)
library(dplyr)

#setwd("C:/Users/Alastair/Documents/HillRacingAnalysis")
setwd("C:/Users/s0822514/Dropbox/HillRacingAnalysis")
#dump("add2", file="time.to.seconds.R")
source("time.to.seconds.R")

Races <- distinct(read.csv("Races",row.names = NULL))
Races$Distance<-as.numeric(str_split_fixed(as.character(Races$Distance)," ",2)[,1])
Races$Climb<-as.numeric(str_split_fixed(as.character(Races$Climb)," ",2)[,1])
t<-str_split_fixed(as.character(Races$M_record_time)," ",3)[,1]
Races$M_record_time <-time.to.seconds(t)
t<-str_split_fixed(as.character(Races$F_record_time)," ",3)[,1]
Races$F_record_time <-time.to.seconds(t)
Races$M_record_year<-as.numeric(gsub("\\)|\\(", "",Races$M_record_year))
Races$F_record_year<-as.numeric(gsub("\\)|\\(", "",Races$F_record_year))
Races$M_record_holder<-gsub(" - ", "",Races$M_record_holder)
Races$F_record_holder<-gsub(" - ", "",Races$F_record_holder)

#Runs$Time <-time.to.seconds(Runs$Time)
#Runs$Runnerid<-paste(as.character(Runs$Runner),as.character(Runs$Club))
#Runs<-Runs[,c(8,1:7)]

