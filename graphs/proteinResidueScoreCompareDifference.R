# install.packages("ggplot2")
# load package
options(scipen=999)  # turn-off scientific notation like 1e+48
library(ggplot2)
theme_set(theme_bw())  # pre-set the bw theme.

# load data
rangeN = 1
dataFileName = paste("../results/proteinResidueScoreCompare",rangeN,".csv",sep = "")
proteinResidueScoreData = read.csv(dataFileName)

# absolute value of difference
proteinResidueScoreData["Energy.Score.Difference"] = lapply(proteinResidueScoreData["Energy.Score.Difference"], abs)

# Scatterplot
gg = ggplot(data = proteinResidueScoreData, 
            mapping = aes(
              xmin=Residue.Index.Start, 
              xmax=Residue.Index.End))
gg = gg + guides(fill=guide_legend(title="NULL"))
gg = gg + geom_errorbar(mapping = 
  aes(y=Energy.Score.Difference), color="#97596b")

#gg = gg + geom_smooth(method="loess", se=F)
#gg = gg + xlim(c(0, 500)) 
#gg = gg + ylim(c(0, 3000000))
subtitleName = paste("Range = ",rangeN," Residues",sep = "")
outputFileName = paste("proteinResidueScoreDifference",rangeN,".png",sep = "")
gg = gg + labs(subtitle=subtitleName, 
    y="Energy Score", 
    x="Residue Number", 
    title="Protein Residue Score Difference")

plot(gg)
ggsave(outputFileName, plot=gg, width = 16, height = 9, units = "cm")





