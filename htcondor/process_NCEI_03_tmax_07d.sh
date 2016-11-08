#!/bin/bash

tar -xzf python.tar.gz
export PATH=miniconda2/bin:$PATH
python process_NCEI_03_tmax_07d.py NCEI_WIS_$1 $1 /mnt/gluster/megarcia/WIS_Climatology/grids
