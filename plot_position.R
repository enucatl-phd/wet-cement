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

time_origin = table[1, time]
print(time_origin)
table[, sqrttime := sqrt(time - time_origin)]

plot = ggplot(table, aes(x=sqrttime, y=wet_fraction)) +
    geom_point(size=1) + 
    geom_smooth(data=table[sqrttime > 15 & sqrttime < 90], method='lm') +
    xlab(expression(sqrt(t (s)))) +
    ylab("water infiltration (relative)")

print(plot)
width = 4
aspect.ratio = 1
height = width * aspect.ratio
ggsave(args$o, plot, width=width, height=height, dpi=300)
invisible(readLines(con="stdin", 1))
