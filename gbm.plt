set view map

unset surface

set style data pm3d

set xrange [0.0:200.0]
set yrange [0.0:200.0]
set zrange [0.0:1.0]

set pm3d implicit at b

set terminal png size 400, 400


set output 'data/pic/gbm_rotate_60.png'
splot 'data/gbm_u_59.dat' using 2:1:3 notitle
