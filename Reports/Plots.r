df<-summarise(group_by(left_join(Runs,Races),Race,Date),entrants = length(Runner), Winning_time = min(Time),Distance = mean(Distance), Climb = mean(Climb))
ggplot(df)+geom_point(aes(x=Date,y=entrants,size = Distance, colour=Climb))

Runners<-summarise(group_by(left_join(Runs,Races),Runnerid),n_races = length(Runner),avg_Winner_Pct = mean(X.Winner), avg_distance = mean(Distance), avg_climb=mean(Climb))
ggplot(df)+geom_point(aes(x=avg_Winner_Pct,y=n_races))
