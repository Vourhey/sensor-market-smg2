#!/bin/sh

rrdtool graph $2 \
    -t "$3" -v 'мкЗв/ч' \
    --end now --height 300 --y-grid 0.01:10 -X 0 \
    DEF:avg=$1:radiation:AVERAGE:step=775 \
    DEF:max=$1:radiation:MAX:step=775 \
    DEF:min=$1:radiation:MIN:step=775 \
    CDEF:savg=avg,1,* \
    CDEF:smin=min,1,* \
    CDEF:smax=max,1,* \
    LINE1:smax#FF0000:"Максимум \l" \
    LINE1:savg#0000FF:"Среднее \l" \
    LINE1:smin#00FF00:"Минимум \l"

