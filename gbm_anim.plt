set view map

unset surface

set style data pm3d

set xrange [0.0:200.0]
set yrange [0.0:200.0]
set zrange [0.0:1.0]

set pm3d implicit at b

set term gif animate size 400, 400

set output 'data/pic/gbm_u_sim1.gif'

do for [t = 0:198] 
{
	set title 't = '.t
	splot 'data/gbm_u_'.t.'.dat' using 2:1:3 notitle
}