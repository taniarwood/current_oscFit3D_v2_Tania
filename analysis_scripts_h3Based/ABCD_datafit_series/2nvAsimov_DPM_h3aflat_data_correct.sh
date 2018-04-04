#!/bin/bash
#PBS -l nodes=1:ppn=8,pmem=3700m,walltime=25:00:00
#PBS -A ngw-282-ad
#PBS -e /gs/project/ngw-282-ac/trwood/post_berlin_output/post_berlin_profiles_lowchi_azimov/OUTPUT_Asimov_DPM_h3aflat_data_correct_again_shiftedStartFrac3a.txt
#PBS -o /gs/project/ngw-282-ac/trwood/post_berlin_output/post_berlin_profiles_lowchi_azimov/RUNOUT_Asimov_DPM_h3aflat_data_correct_again_shiftedStartFrac3a.txt  
#PBS -V
echo "$0: pbs host = `hostname`"
echo "$0: start time = `date`"
export StartTime=`date +%s`
  
cd /gs/project/ngw-282-ac/trwood/post_berlin_output/post_berlin_profiles_lowchi_azimov/  
python /gs/project/ngw-282-ac/trwood/post_berlin_output/post_berlin_profiles_lowchi_azimov/2nuAsimov_DPM_h3aflat_data_correct_again_startingfracShifted3.py  0.120
	
export EndTime=`date +%s`
echo "$0: end time = `date`"
echo "$0: Job Duration = `expr $EndTime - $StartTime` seconds"
echo "$0: done processing"
exit 0
