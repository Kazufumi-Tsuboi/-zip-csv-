#Change directrry at ~~
setwd("~~/DIM new/unzip/1000")
library(data.table)
library(dplyr)
library(ggplot2)

#list of csv in directry
files <- list.files(pattern = "\\.csv$") 

#Making empty data frame
df <- data.frame()

#Rreading csv in "files"
for(i in 1:length(files)){
  add <- fread(files[i])
  add  <- add %>%
    select( "date","area","population") %>%
    filter(area=='533946111'|area=='534030393') #Chosing area you want to analyze
  df <- rbind(df,add)
}

#Changing data type from numeric to character and to date
df$date <- as.character(df$date)
df$date <-  as.Date(df$date, format = "%Y%m%d")
df$area <- as.factor(df$area)
#plot
ggplot(data=df,mapping=aes(x=date,y=population,color=area))+geom_line()