# install.packages("ggplot2")
# load package
options(scipen=999)  # turn-off scientific notation like 1e+48
library(ggplot2)
theme_set(theme_bw())  # pre-set the bw theme.

# load data
rangeN = 200
dataFileName = paste("../results/algorithmTimeComplexity",rangeN,".csv",sep = "")
algorithmTimeComplexityData = read.csv(dataFileName)

# Scatterplot
M = 0.52
gg = ggplot(data = algorithmTimeComplexityData, 
            mapping = aes(
              x=Protein.Chain.Length, 
              y=Run.Duration..milliseconds.))
gg = gg + guides(fill=guide_legend(title="NULL"))
gg = gg + geom_line(
  mapping = aes(color="a"))
gg = gg + stat_function(
  mapping = aes(color="b"), 
  fun=function(x) (M*x)^2)
gg = gg + stat_function(
  mapping = aes(color="c"), 
  fun=function(x) (M*x)*log2(M*x))
gg = gg + stat_function(
  mapping = aes(color="d"), 
  fun=function(x) M*x)

#gg = gg + geom_smooth(method="loess", se=F)
#gg = gg + xlim(c(0, 500)) 
#gg = gg + ylim(c(0, 3000000))
subtitleName = paste("Range = ",rangeN," Residues",sep = "")
outputFileName = paste("algorithmTimeComplexity",rangeN,".png",sep = "")
gg = gg + labs(subtitle=subtitleName, 
    y="Runetime (milliseconds)", 
    x="Protein Chain Length (# residues)", 
    title="Compute Energy Score Algorithm Time Complexity")
gg = gg + scale_color_manual(name ="Big O", 
                             labels=c("Actual", bquote(n^2), bquote("n log n"), bquote(n)),
                             values=c("#97596b","#11a5c3", "#a29201","#dcc900"))
gg = gg + scale_shape_identity()
theme(legend.position = "right")

plot(gg)
ggsave(outputFileName, plot=gg, width = 16, height = 9, units = "cm")





