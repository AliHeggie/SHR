time.to.seconds <- function(time) {
  #browser()
  t<-str_split_fixed(as.character(time)," |:",3)
  #t <- strsplit(as.character(time), " |:")[[1]]

  seconds <- (as.numeric(t[,1]) * 60 * 60 
                + as.numeric(t[,2]) * 60 + as.numeric(t[,3]))   
 
  
  return(seconds)
}