#!/bin/bash
#PBS -l nodes=1:ppn=8,pmem=3700m,walltime=18:00:00
#PBS -A ngw-282-aa
#PBS -e /gs/project/ngw-282-ac/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/analysis_scripts_h3Based/profile_scans_def2/k_pi/k_pi_quanties/errout/116.4.40ERRORoutput.txt
#PBS -o /gs/project/ngw-282-ac/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/analysis_scripts_h3Based/profile_scans_def2/k_pi/k_pi_quanties/runout/116.4.40runoutput.txt   
#PBS -V
echo "$0: pbs job id = ${PBS_JOBID}"
echo "$0: pbs host = `hostname`"
echo "$0: start time = `date`"
export StartTime=`date +%s`
  
cd /gs/project/ngw-282-ac/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/analysis_scripts_h3Based/profile_scans_def2/k_pi/k_pi_quanties
python /gs/project/ngw-282-ac/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/analysis_scripts_h3Based/profile_scans_def2/k_pi/k_pi_quanties/quantiles_k_pi_h3a_h3a_def2_2nv_k_pi.py   4.40    116
	
export EndTime=`date +%s`
echo "$0: end time = `date`"
echo "$0: Job Duration = `expr $EndTime - $StartTime` seconds"
echo "$0: done processing"
exit 0
