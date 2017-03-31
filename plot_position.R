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
args = commandline_parser$parse_args()

table = fread(args$f)
print(table)

table[, time := as.POSIXct(time, origin="1970-01-01")]

plot = ggplot(table) +
    geom_point(aes(x=time, y=wet_fraction), size=1) +
    scale_x_datetime(
        breaks=date_breaks("30 min"),
        labels=date_format("%H:%M")
        )

print(plot)
width = 7
aspect.ratio = 1
height = width * aspect.ratio
ggsave(args$o, plot, width=width, height=height, dpi=300)
invisible(readLines(con="stdin", 1))
