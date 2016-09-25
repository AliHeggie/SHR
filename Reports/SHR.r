library(ggplot2)
library(stringr)
library(dplyr)

#setwd("C:/Users/Alastair/Dropbox/HillRacingAnalysis")
setwd("C:/Users/s0822514/Dropbox/HillRacingAnalysis")
dump("add2", file="time.to.seconds.R")
source("time.to.seconds.R")
trim <- function (x) gsub("\n| \n", "", x)

#Create Races data Frame
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

#Create Runs data frame
Runs <- read.csv("SHR",row.names = NULL)
Runs$Date <- as.Date(Runs$Date,"%d/%m/%Y")
Runs$Time <-time.to.seconds(Runs$Time)
Runs$Runnerid<-paste(as.character(Runs$Runner),as.character(Runs$Club))
Runs<-Runs[,c(8,1:7)]
Runs$Race<-trim(Runs$Race)
Runs$Race<-as.factor(Runs$Race)
Runs$X.Winner<-as.numeric(gsub("%","",Runs$X.Winner))
Runs<-left_join(Runs,Races)



###WOULD LIKE AN NRUNNERS STAT FOR RACES
Results<-left_join(summarise(group_by(Runs,Race,Date),n_runners = n(),avg_time = mean(Time)),Races)

#Create Runners data Frame)
Runners<-summarise(group_by(left_join(Runs,Races),Runner,Club),n_races = n(),avg_Winner_Pct = mean(X.Winner), avg_distance = mean(Distance), avg_climb=mean(Climb))



#Create Clubs data Frame
