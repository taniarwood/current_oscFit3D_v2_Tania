

import os, sys
#modules_dir = '/home/trwood/JP_fraction_original_jan26_test/modules'
modules_dir = '/gs/project/ngw-282-ac/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/modules'
#modules_dir = '/project/d/dgrant/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/modules'
sys.path.append(modules_dir)


# Importing modules
import argparse
import math
import pickle

#import dataLoader_corrected as dataLoader
import dataLoader_corrected_weight_e_pi as dataLoader
#import dataLoader
import numpy as np
import oscfit_default_values as defs
from copy import deepcopy
import jp_mpl as jplot

#import oscFit_JP_chi2 as oscFit  #13 bins
import oscFit_JP_chi2_12bins as oscFit   #12 bins (loose top numu bin) .. thinking on just cutting out those eventsgoing up to 500


parser = argparse.ArgumentParser(description='script for calculating neutrino flux forward fold bin nomrmalization profiles')
parser.add_argument('normbinfix', help='value to try the scan on')

args = parser.parse_args()

#for use if you want this in the outputfile naming
frac_use = str(args.normbinfix)
print frac_use, 'string'

#for use in the code
dfrac_use = float(frac_use)
print dfrac_use, 'float'

sysfile_use = '/gs/project/ngw-282-ac/trwood/jasper_home/pbs_submit/Andreis_daydream_for_Tests/DRAGON_detector_systematics_albrecht_DMP_h3a3.pckl'


#POINT OF CONFUSION:  do i need the atmos muons dataloader? :/ I think not but this seems like a general flawmaybe.. maybe i never have them in my faked data???

loader = dataLoader.dataLoader(observables =
      ['reco_energy', 'reco_zenith', 'delta_llh'],
      bin_edges   = [10**np.linspace(0.75,2.25,11),
	 np.arccos(np.linspace(-1.,1.,9))[::-1],
	 np.array([-3, 2, np.inf])],
   #   user = 'Chi2msu_no_background_noData_baselineONLY_flat_uncontained_mus2', 
      user = 'Chi2msu_no_background_noData_baselineONLY_flat_uncontained_mus_def2',
      LEaxis = [],
      detsys_nuspecs = {},
      detsys_muspecs = {},
      weight_keys = ['weight_DMP_h3a_rc1_e_k','weight_DMP_h3a_rc1_e_p','weight_DMP_h3a_rc1_mu_k','weight_DMP_h3a_rc1_mu_p'],
 #     weight_keys = ['weight_e', 'weight_mu', 'tweight_DMP_GH_mu_p_jaspert'],
      detsys_redo = False,
      sysfile = sysfile_use,
      #flatflux_module = flat_corr,
      verbose = False, # # Never again set to true. It dumps SO MUCH GARBAGE
      table_nbins = -1)


#the data settings
data_settings = {
      'dm31':                  0.0025,
      'theta23':                  0.74,
      'theta13':                  0.155,
      'mix_angle':                1.,
      'norm_tau':                 1.,
      'axm_qe':                   0.,
      'axm_res':                  0.,
      'norm_nu':                  2.75, # In years!
      'norm_e':                   1.,
      'domeff':                   1.,
      'nu_pi_scale':              1.0, #0.0, #0.91,  # this multiplies by 'tweight_DMP_GH_mu_p_jaspert' in the code everywehre, so it will wipe the third weight out
      'hole_ice':                 0.02,
      'atmmu_template':           'data',
      'simulation':               'baseline',
      'oscTables':                False,
      'gamma':                    0.,
      'ma_variations':            False,
      'add_detector_systematics': True,
      'norm_atmmu':               0.38,
      # 'pid_bias':                 0.,
      'hi_fwd':                   0., # MSU parameterization of the forward impact angle
      'had_escale':               1.,
      'oscMode':                  'Prob3', #'TwoNeutrino',#'Vacuum', #'TwoNeutrino',
      'norm_noise':                0.0}
#      'atmmu_f':                  0.10  }

####################  
# try re-normalizing to correct norm_Nu basically ... 
###########################

#data_hist2 = loader.loadMCasData(data_settings, statistical_fluctuations=False)
histo_num = np.arange(0,1000, 1)
#make list of statistically fluctuatied histograms 
#each scan will use a particlar histogram, a for the whole scan
#each total scan will then differ from the others only by statistical fluctuations

data_histogram_array = []

for item in histo_num:
       print item
       data_hist2 = loader.loadMCasData(data_settings,
                                                   statistical_fluctuations=True)
       data_histogram_array.append(data_hist2)



#dump list of data_histograms into pickle file.. will now be a dictionary perhaps. 
pickle.dump(data_histogram_array,open('/home/trwood/oscfit_output/hist_list_1000_prob3_2.75_h3a_h3a.pckl', 'w'))

sys.exit()


#data_histo_bkrd_PlusNu = pickle.load(open('/home/trwood/pbs_submit/FractionForwdFold/tw_scripts/Checks_Binning_Berlin/Data_Feb_2018.pckl'))
data_hist2 = loader.loadMCasData(data_settings, statistical_fluctuations=False)
data_hist = loader.loadMCasData(data_settings, statistical_fluctuations=False)
print 'Events in data_hist2', np.sum(data_hist2)
print 'Events in data_hist1', np.sum(data_hist)
#data_hist2 = loader.loadMCasData(data_settings, statistical_fluctuations=False)
#data_hist2 = deepcopy(original_data)
#print np.sum(data_hist2)
# Scaling the data to the observed events in the sample (with containment cut)
msu_observed = 49599.
data_hist2 *= msu_observed/np.sum(data_hist2)
data_hist *= msu_observed/np.sum(data_hist)
#print 'Events in data', np.sum(data_hist2)
'''

######################
# checks !
##########################
# Check that TANIA can reproduce her own data (duh!)
#data_to_data = data_histo_bkrd_PlusNu/data_hist
#print 'Mean', data_to_data.mean()
print 'Panic if its not EXACTLY one'


#################################
## Calculate the fractions.. shoudl we really do this again and again? means twice the loaders i think ... soooo
## still it is cleaner and less time then the fit .... (But a lot) .. minutes to hours. let's do it. 
#################################

#IN CASE I HAVE to calculate the fractions right meow 
'''
split_full_histo = np.zeros_like(data_hist2)
split_data = []

loader_dict = deepcopy(loader.iniDict)
split_data = []
loader_dict['user'] = 'Chi2msu_no_background_noData_baselineONLY_flat_uncontained_numu_def2'
for one_axis in true_axis_mu9:
   loader_dict['extra_cuts'] = {'energy':one_axis}
   new_loader = dataLoader.dataLoader(**loader_dict)
   this_data = new_loader.loadMCasData(data_settings)
   split_full_histo += this_data
   split_data.append(np.sum(this_data))

#split_data = np.array(split_data)
#fractions_numu = split_data/np.sum(split_data) #pickle.dump(fractions_numu, open('DRAGON_fractions_guess_a_mu.pckl', 'w'))
		       #######################
loader_dict_e = deepcopy(loader.iniDict)
split_data_e = []
loader_dict_e['user'] = 'Chi2msu_no_background_noData_baselineONLY_flat_uncontained_nue_def2'
for one_axisE in true_axis_e4:
   loader_dict_e['extra_cuts'] = {'energy':one_axisE}
   new_loader_e = dataLoader.dataLoader(**loader_dict_e)
   this_data = new_loader_e.loadMCasData(data_settings)
   split_full_histo += this_data
   split_data_e.append(np.sum(this_data))
   

split_data = np.array(split_data)

split_data_e = np.array(split_data_e)
print 'split data nue'
print split_data_e
fractions_numu = split_data/( np.sum(split_data) + np.sum(split_data_e) )
fractions_e = split_data_e/( np.sum(split_data) + np.sum(split_data_e))


print 'split data numu'
print split_data

####
## Verify that the fractions and the data sum up to the same
####

print '\n*****SUMMARY*****\n'
print 'This is the sum of split data', np.sum(split_full_histo)
#print 'Sum(abs(split-original)):', np.sum(np.abs(original_data-split_full_histo))
print 'Sum of fractions', np.sum(fractions_e) + np.sum(fractions_numu)


print '\nFractions'
print 'Nue fractions:'
print fractions_e
print 'NuMu fractions: '
print fractions_numu


start_fractions_numu = np.array(fractions_numu)
start_fractions_nue = np.array(fractions_e)

#########
##
# ATMOSPHERIC MUONS ONLY LOADER
##

#loader_dict_atmos = deepcopy(loader_dict_numu)
#loader_dict_atmos['extra_cuts'] =  {}
#loader_dict_atmos['user'] = 'Chi2msu_BKGRND_only_flat_uncontained'
#loader_pureBkrd = dataLoader.dataLoader(**loader_dict_atmos)




########
## FIT SETTINGS
########
fit_settings = deepcopy(defs.default_fit_settings)
fit_settings_fix    = {
      'simulation':     'baseline',
      'dm31':           [0.0025, False, 'NH'],
      'theta23':        [0.74, True],
      'theta13':        [0.155, True],
      'oscMode':        'TwoNeutrino',#'Prob3', #'TwoNeutrino', #'Vacuum',  # 'TwoNeutrino', # 'Vacuum',
      'oscTables':      False,         #used to be False.  need to think about the tables.  need to understand resolution to set n bins
      'norm':           [1., False],    #try once with this true and once with this false, same settings


      # These are good starting values for the realistic spectrum
      #starting values for numu
      
#value to profile scan
     # 'nu_frac7':       [dfrac_use, True],

      'nu_frac1':       [0.12329, False],
      'nu_frac2':       [0.11896, False],
      'nu_frac3':       [0.15892, False],
      'nu_frac4':       [0.09963, False],
      'nu_frac5':       [0.09477, False],
      'nu_frac6':       [0.0570, False],
      'nu_frac7':       [0.03487, False],

      'nu_frac8':       [0.08007, False],
      #  'nu_frac9':       [start_fractions_numu[8], False],  #only one fraction needs to be 'not fit' to require all to be summed to one. 
      # move this burden to nue spectrum now


      #starting fractions for nue
      'nu_frac9':	 [0.09874, False],  
      'nu_frac10':       [0.08603, False],
      'nu_frac11':       [0.03643, False],
 #     'nu_frac12':       [start_fractions_nue[3], False],
      # The last fraction is not fit, but calculated


      'norm_e':         [1., True],
      'norm_tau':       [1., True],
      'nu_nubar':       [1., True],
      'nubar_ratio':    [0., True],
      'uphor_ratio':    [0., True],
      'nu_pi_scale':    [dfrac_use, True],
      'hi_fwd':         [0., False],
      'gamma':          [0., True],
      'axm_qe':         [0., True],
      'axm_res':        [0. , False],
      'pid_bias':       [0., True],
      'hole_ice':       [0.021, False],           # Fix these to true for this test???

      #'mix_angle':      [1.0, 1.5],
      'mix_angle':      [1.0,False, 1.5],

      'minimizer':      'migrad', # 'SLSQP', #'migrad',

      'norm_nc':        [1., False],
      'domeff':         [1., False],
      'had_escale':     [1., True],
#      'atmmu_f':        [0.0, True, 'data'],
      'atmmu_f':        [0.067, False, 'data'],
   #   'norm_nu':                  2.50, # In years!

    'noise_f':        [0.0, True],
    'detector_syst':   True,
    'include_priors': True,
    'printMode':      -1}  # (-1) this is printing each step



import iminuit
fitter = oscFit.fitOscParams()


fit_priors = {'hole_ice':[0.02, 0.01],
	    'norm_nc':        [1., 0.2],
      'norm_e':[1., 0.2]}


oscFitResults_fixed =fitter(data_histograms=[data_hist],
#oscFitResults_fixed =fitter(data_histograms=[data_histo_bkrd_PlusNu],
      data_loaders=[loader_nobkrd_a,  #NuMu loaders
	 loader_nobkrd_b,
	 loader_nobkrd_c,
	 loader_nobkrd_d,
	 loader_nobkrd_e,
	 loader_nobkrd_f,
	 loader_nobkrd_g,
#	 loader_nobkrd_h,
	 loader_nobkrd_i,
	 # nue loaders
	 loader_nobkrd_j,
	 loader_nobkrd_k,
	 loader_nobkrd_l,
	 loader_nobkrd_m,
	 loader_pureBkrd],
      fit_settings=fit_settings_fix,
      ncalls               = 10000,  # For migrad. Simplex will use twice the number.
      tol 		 = 0.01,  # condition, edm < edm_max, where edm_max = 0.0001 * tol* UP  ( UP = 1.0 chi2, -.5 llh, defalut 1.0).
      store_fit_details    = True)


pickle.dump(oscFitResults_fixed,open('/gs/project/ngw-282-ac/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/analysis_scripts_h3Based/profile_scans_def2/outfiles/k_pi/def2_2nv_profilescan'+ str(dfrac_use) +'h3a_h3a.pckl', 'w'))
