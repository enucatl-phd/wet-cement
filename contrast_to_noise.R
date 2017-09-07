#!/usr/bin/env Rscript

library(ggplot2)
library(data.table)
library(argparse)
library(scales)

theme_set(theme_bw(base_size=12) + theme(
    legend.key.size=unit(1, 'lines'),
    text=element_text(face='plain', family='CM Roman'),
    legend.title=element_text(face='plain'),
    axis.line=element_line(color='black'),
    axis.title.y=element_text(vjust=0.1),
    axis.title.x=element_text(vjust=0.1),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    legend.key = element_blank(),
    panel.border = element_blank(),
    axis.line.x = element_line(color="black", size=0.5),
    axis.line.y = element_line(color="black", size=0.5)
))

commandline_parser = ArgumentParser(
        description="make plots")
commandline_parser$add_argument('-f', '--file',
            type='character', nargs=1,
            help='file with the data.table')
commandline_parser$add_argument('-o', '--output',
            type='character', nargs=1,
            help='output png file')
commandline_parser$add_argument('-p',
            type='character', nargs=1,
            help='output absorption png file')
args = commandline_parser$parse_args()

table = fread(paste("gunzip -c", args$f))
molten = melt(table, id.vars="status")
print(molten)

mean.ratio.dry = mean(molten[variable == "ratio" & status == "dry", value], na.rm=TRUE) 
mean.ratio.wet = mean(molten[variable == "ratio" & status == "wet", value], na.rm=TRUE) 
sd.ratio.dry = sd(molten[variable == "ratio" & status == "dry", value], na.rm=TRUE) 
ratio.cnr = abs(mean.ratio.dry - mean.ratio.wet) / sd.ratio.dry

print(mean.ratio.dry)
print(mean.ratio.wet)
print(sd.ratio.dry)

print(ratio.cnr)

mean.absorption.dry = mean(molten[variable == "absorption" & status == "dry", value], na.rm=TRUE) 
mean.absorption.wet = mean(molten[variable == "absorption" & status == "wet", value], na.rm=TRUE) 
sd.absorption.dry = sd(molten[variable == "absorption" & status == "dry", value], na.rm=TRUE) 
absorption.cnr = abs(mean.absorption.dry - mean.absorption.wet) / sd.absorption.dry

print(mean.absorption.dry)
print(mean.absorption.wet)
print(sd.absorption.dry)

print(ratio.cnr)

ratio_plot = ggplot(molten[variable == "ratio"]) +
    geom_density(aes(value, fill=status), alpha=0.4) +
    scale_fill_discrete(name=paste("CNR =", round(ratio.cnr, 2))) +
    xlab("log(vis reduction) / log(transmission)") +
    xlim(0, 3)
absorption_plot = ggplot(molten[variable == "absorption"]) +
    geom_density(aes(value, fill=status), alpha=0.4) +
    scale_fill_discrete(name=paste("CNR =", round(absorption.cnr, 2))) +
    xlab("-log(transmission)") +
    xlim(0.3, 0.6)

print(ratio_plot)
print(absorption_plot)
width = 4
aspect.ratio = 1
height = width * aspect.ratio
ggsave(args$o, ratio_plot, width=width, height=height, dpi=300)
ggsave(args$p, absorption_plot, width=width, height=height, dpi=300)
invisible(readLines(con="stdin", 1))
