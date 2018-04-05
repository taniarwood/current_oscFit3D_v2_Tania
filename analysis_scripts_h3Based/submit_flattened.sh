#!/bin/bash
#PBS -l nodes=1:ppn=8,pmem=3700m,walltime=18:00:00
#PBS -A ngw-282-ad
#PBS -e /gs/project/ngw-282-ac/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/analysis_scripts_h3Based/OUTPUT/0.91_nupi_scale_start_2nuv_data_h3a_flattened.txt
#PBS -o /gs/project/ngw-282-ac/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/analysis_scripts_h3Based/RUNOUT/RUNOUT_0.91_nupi_scale_start_2nuv_data_h3a_flattened.py  
#PBS -V
echo "$0: pbs host = `hostname`"
echo "$0: start time = `date`"
export StartTime=`date +%s`
  
cd /gs/project/ngw-282-ac/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/analysis_scripts_h3Based/ 
python /gs/project/ngw-282-ac/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/analysis_scripts_h3Based/0.91_nupi_scale_start_2nuv_data_h3a_flattened.py  0.120
	
export EndTime=`date +%s`
echo "$0: end time = `date`"
echo "$0: Job Duration = `expr $EndTime - $StartTime` seconds"
echo "$0: done processing"
exit 0
