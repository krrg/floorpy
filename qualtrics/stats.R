
library(data.table)

id_source_score <- as.data.frame(fread("out/id_source_score.csv", header = TRUE))
t.test(SCORE~SOURCE, data=id_source_score)

agg <- aggregate(id_source_score$SCORE, list(plan_id = id_source_score$ID, source=id_source_score$SOURCE), mean)
agg[order(agg$x),]




# boxplot(split(sus_scores$SUS_OVERALL, sus_scores$TFA), main="Website SUS Scores", ylim=c(0, 100))
# boxplot(split(sus_scores$SUS_TFA, sus_scores$TFA), main="Authentication SUS Scores", ylim=c(0, 100))

# boxplot(sus_scores$SUS_TFA)
# kruskal.test(timings)


