# install.packages("ggplot2")
# load package
options(scipen=999)  # turn-off scientific notation like 1e+48
library(ggplot2)
theme_set(theme_bw())  # pre-set the bw theme.

# load data
rangeN = 20
dataFileName = paste("../results/proteinResidueScoreCompare",rangeN,".csv",sep = "")
proteinResidueScoreData = read.csv(dataFileName)

# Scatterplot
gg = ggplot(data = proteinResidueScoreData, 
            mapping = aes(
              xmin=Residue.Index.Start, 
              xmax=Residue.Index.End))
gg = gg + guides(fill=guide_legend(title="NULL"))
gg = gg + geom_errorbar(mapping = 
  aes(y=Protein..1.Energy.Score, color="a"))
gg = gg + geom_errorbar(mapping = 
  aes(y=Protein..2.Energy.Score, color="b"))

#gg = gg + geom_smooth(method="loess", se=F)
#gg = gg + xlim(c(0, 500)) 
#gg = gg + ylim(c(0, 3000000))
subtitleName = paste("Range = ",rangeN," Residues",sep = "")
outputFileName = paste("proteinResidueScoreCompare",rangeN,".png",sep = "")
gg = gg + labs(subtitle=subtitleName, 
    y="Energy Score", 
    x="Residue Number", 
    title="Protein Residue Score Comparison")
gg = gg + scale_color_manual(name ="Protein Chain", 
                  labels=c("Structure #1", "Structure #2"),
                  values=c("#97596b","#11a5c3"))
gg = gg + scale_shape_identity()
theme(legend.position = "right")

plot(gg)
ggsave(outputFileName, plot=gg, width = 16, height = 9, units = "cm")

