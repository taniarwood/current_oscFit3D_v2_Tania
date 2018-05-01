
# coding: utf-8
import os
import numpy as np
import pickle as pckl
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='script for calculating neutrino flux forward fold bin nomrmalization profiles')
parser.add_argument('frac', help='Energy bin number (or nu_Frac numer), pls use a digit only')
parser.add_argument('low', help='Lower Bound of profile scan')
parser.add_argument('up', help='Upper Bound')
parser.add_argument('step', help='step size in scan')
#parser.add_argument('dig', help='number of digits in filename')
args = parser.parse_args()

#for use if you want this in the outputfile naming
frac_num=str(args.frac)
lowr_s  =str(args.low)
upr_s =str(args.up)
step_s = str(args.step)

lowr = float(lowr_s)
upr = float(upr_s)
stepp = float(step_s)
#digg = str(args.dig)

print lowr, 'float'




chi_value = []
profile_scan_value =[]

scan_val=0
chi_v =0
#frac_num = 7

#This needs to be an argument readin
nu_pi_range =np.arange(lowr,upr,stepp)

for item in nu_pi_range:
    new_item = '%.3f'%item
    if os.path.isfile('/gs/project/ngw-282-ac/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/analysis_scripts_h3Based/profile_scans_def2/outfiles/frac'+str(frac_num)+'/def2_2nv_profilescan'+str(new_item)+'.pckl'):
#    if os.path.isfile('/gs/project/ngw-282-ac/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/analysis_scripts_h3Based/profile_scans_def2/outfiles/k_pi/def2_2nv_profilescan_data'+str(new_item)+ '.pckl'):  
    #if os.path.isfile('/gs/project/ngw-282-ac/trwood/post_berlin_output/post_berlin_profiles_lowchi_azimov/frac1/outfiles/Asimov_allIN_review_offical_' + str(new_item) + 'Jan5_7binsNumu_5BinsNue_oneLessbin_wBurnSample10Percent_2018_2_twoNeutrino_norm_false_frac8_burn.pckl'):#azimov_dec17_Muons_vac.pckl'):  #frac1_scale_profile0.090lowchi_azimov_dec17_Muons_vac.pckl 
        # frac1_scale_profile0.090lowchi_azimov_dec17_Muons_vac.pckl ifrac1_scale_profile0.090lowchi_azimov_dec17_Muons_vac.pckl 	
	print 'hi'
    	#data = pckl.load(open('/gs/project/ngw-282-ac/trwood/post_berlin_output/post_berlin_profiles_lowchi_azimov/frac'+str(frac_num)+'/outfiles_v/frac' + str(frac_num) + '_scale_profile' + str(new_item) + 'lowchi_azimov_dec17_Muons_vac.pckl'))#azimov_dec17_Muons_vac.pckl'))
	#data = pckl.load(open('/gs/project/ngw-282-ac/trwood/post_berlin_output/post_berlin_profiles_lowchi_azimov/frac1/outfiles/Asimov_allIN_review_offical_' + str(new_item) + 'Jan5_7binsNumu_5BinsNue_oneLessbin_wBurnSample10Percent_2018_2_twoNeutrino_norm_false_frac8_burn.pckl'))
        #data = pckl.load(open('/gs/project/ngw-282-ac/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/analysis_scripts_h3Based/profile_scans_def2/outfiles/k_pi/def2_2nv_profilescan_data'+str(new_item)+ '.pckl'))
        data = pckl.load(open('/gs/project/ngw-282-ac/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/analysis_scripts_h3Based/profile_scans_def2/outfiles/frac'+str(frac_num)+'/def2_2nv_profilescan'+str(new_item)+'.pckl'))
	if data['successful_fit']:
    		scan_val= data['nu_frac'+str(frac_num)]
		#scan_val = data['nu_pi_scale']
    		chi_v = data['llh']
    
    		print scan_val, chi_v
    
    		chi_value.append( chi_v )
    		profile_scan_value.append(scan_val)
    else:
	print 'a file is missing'
	print new_item

chi_value = np.array(chi_value)
profile_scan_value=np.array(profile_scan_value)

#move chi2 values so that minimum chi2 value is at zero
chi_value = chi_value - chi_value.min()

#print chi_value


#repurosed code from Joshua Hignight
#note we want to find the value at y=num NOT x=num, so we give x as y-values and y as x-values
# so here we want the value of the scanned paramter at chi_2 is zero and where chi2 = 1
	#so want value at chi2 (y) = 1 
#Note, this really only works for the special case you have a parabola like shape so only use for that reason

#print 'QUESTION to self > so if i take both interesctions i just divde by twoto get error bar on each side. this assumes
#the errors are semetric ... hmmmm they may not be. I should find a way to print the zero also and allow for non-symmetirc
#error bars on my final result'

#point_LHS = 0.0
#point_RHS = 0.0
#point_center = 0.0

def find_intersection(x,y,num_to_find):#(frac, chi, num_to_find):

	#find the min for splitting array
	print np.argmin(y)
	point_center = np.argmin(y)
	split = np.argmin(y)
	


	#I changed to using np.interp.  It is a linear interpolation, which is fine given enough points in profile
	#Must be given in increasing value of x, so sort incase number is negative (if not will return same ordering)
	#note we want to find the value at y=num NOT x=num, so we give x as y-values and y as x-values
	#This means sort y
	order_LHS = np.argsort(y[0:split+1])
	order_RHS = np.argsort(y[split::])

#Find values at y=2
	point_LHS=np.interp(num_to_find,y[0:split+1][order_LHS], x[0:split+1][order_LHS])
	point_RHS=np.interp(num_to_find,y[split::][order_RHS], x[split::][order_RHS])
	
	print x[0:split+1]

	print point_LHS, point_RHS 
	return point_LHS, point_RHS

# = 1.0   #chi squared of 1, ie 1sigma error
left, right =find_intersection(profile_scan_value, chi_value,1.0)
#find_intersection(profile_scan_value, chi_value,0.0)

#print nu_pi_range[0]
#print len(nu_pi_range)

plt.figure(figsize=(8., 5))
plt.scatter(profile_scan_value, chi_value, marker='o', color = 'black',label = 'frac ' + str(frac_num) )
plt.title(r'Profile Scan, Segmented Unfolding EnergyBin ' +str(frac_num), fontsize = 20)
#plt.title(r'$\pi$ /K profile scan', fontsize = 20)

plt.ylabel(r'$\Delta \chi^{2}$',fontsize = 18)
plt.xlabel('Fraction of total sample (max = 1)')
#plt.xlabel(r'$\pi$ /K profile scan value (1.0 = nominal)',fontsize = 18)

plt.xlim([nu_pi_range[0],nu_pi_range[-1]])
plt.ylim([0,3])

plt.plot([0,2], [1,1], 'k', marker='o')

plt.rc('grid', linestyle='--', color='indianred')
plt.grid(True)
plt.legend()
plots_dir  = '/gs/project/ngw-282-ac/trwood/jasper_home/JP_fraction_original_jan26_test_lessbins/analysis_scripts_h3Based/profile_scans_def2/outfiles/'
#plt.plot(nu_pi_range[idx], f[idx], 'ro')
#plt.savefig(plots_dir + 'profile_scan_nupiscale_data_def2_h3a.png')
plt.savefig(plots_dir + '/frac'+ str(frac_num) + '/Frac'+str(frac_num)+'_2nv_def2_data.png')

#plt.savefig('/Users/trwood/oscfit_at_home/workign_lowchi/FracAzimovLowChi2'+str(frac_num)+'mark.png')


plt.figure(figsize=(8., 5))
plt.scatter(profile_scan_value, chi_value, marker='o', color = 'black',label = 'frac ' + str(frac_num) )
plt.title(r'Profile Scan, Segmented Unfolding EnergyBin ' +str(frac_num), fontsize = 20)
#plt.title(r'$\pi$ /K profile scan', fontsize = 20)

plt.ylabel(r'$\Delta \chi^{2}$',fontsize = 18)
plt.xlabel('Fraction of total sample (max = 1)')
#plt.xlabel(r'$\pi$ /K profile scan value (1.0 = nominal)',fontsize = 18)

plt.xlim([nu_pi_range[0],nu_pi_range[-1]])
plt.ylim([0,3])

#plt.plot([0,2], [1,1], 'k', marker='o')

plt.rc('grid', linestyle='--', color='indianred')
plt.grid(True)
plt.legend()

#plt.plot(nu_pi_range[idx], f[idx], 'ro')
plt.savefig(plots_dir + '/frac'+ str(frac_num) + '/Frac'+str(frac_num)+'_2nv_def2_data_minus.png')

#plt.savefig(plots_dir + 'profile_scan_nupiscale_data_def2_h3a_short.png')
#plt.savefig('/gs/project/ngw-282-ac/trwood/post_berlin_output/post_berlin_profiles_lowchi_azimov/plots_v/frac' + str(frac_num) + '/scatterFracAzimovLowChi2'+str(frac_num)+'mark_BURN10_2Neutrinoshortr.png')
#plt.savefig('/Users/trwood/oscfit_at_home/workign_lowchi/ScatterFracAzimovLowChi2'+str(frac_num)+'mark.png')

chi_value = chi_value - 1

plt.figure(figsize=(8., 5))
plt.scatter(profile_scan_value, chi_value, linewidth=4, color = 'black',label = 'frac ' + str(frac_num) )
plt.title(r'Profile Scan, Segmented Unfolding EnergyBin ' +str(frac_num), fontsize = 20)
#plt.title(r'$\pi$ /K profile scan', fontsize = 20)

plt.ylabel(r'$\Delta \chi^{2}$',fontsize = 18)
#plt.xlabel(r'$\pi$ /K profile scan value (1.0 = nominal)',fontsize = 18)

plt.xlim([nu_pi_range[0],nu_pi_range[-1]])
plt.ylim([-1,3])
plt.plot([0,2], [0,0], '--k')
#plt.plot([0,2], [1,1], '--k')
plt.rc('grid', linestyle='-', color='indianred')
plt.grid(True)
plt.grid(b=True, which='minor', color='indigo', linestyle='--')

plt.legend()

#plt.plot(nu_pi_range[idx], f[idx], 'ro')
#plt.savefig('/gs/project/ngw-282-ac/trwood/post_berlin_output/post_berlin_profiles_lowchi_azimov/plots_v/frac' +str(frac_num) + '/zerosFrac'+str(frac_num)+'mark_burn10_2Neutrino_shortr.png')
#plt.savefig(plots_dir + 'profile_scan_nupiscale_data_def2_h3a_v.png')
plt.savefig(plots_dir + '/frac'+ str(frac_num) + '/Frac'+str(frac_num)+'_2nv_def2_data_minusv.png')

plt.figure(figsize=(8., 5))
plt.scatter(profile_scan_value, chi_value, linewidth=4, color = 'black',label = 'frac ' + str(frac_num) )
plt.title(r'Profile Scan, Segmented Unfolding EnergyBin ' +str(frac_num), fontsize = 20)
#plt.title(r'$\pi$ /K profile scan', fontsize = 20)

plt.ylabel(r'$\Delta \chi^{2}$',fontsize = 18)
plt.xlabel('Fraction of total sample (max = 1)')
#plt.xlabel(r'$\pi$ /K profile scan value (1.0 = nominal)',fontsize = 18)

plt.xlim([nu_pi_range[0],nu_pi_range[-1]])
plt.ylim([0,8])
plt.plot([0,2], [0,0], 'o')
#plt.plot([0,2], [1,1], '--k')
plt.rc('grid', linestyle='-', color='indianred')
plt.grid(True)
plt.grid(b=True, which='minor', color='indigo', linestyle='--')

plt.legend()

#plt.plot(nu_pi_range[idx], f[idx], 'ro')
#plt.savefig('/gs/project/ngw-282-ac/trwood/post_berlin_output/post_berlin_profiles_lowchi_azimov/plots_v/frac' +str(frac_num) + '/lzerosFrac'+str(frac_num)+'mark_BURN10_2neutrino_shortr.png')
#plt.savefig(plots_dir + 'profile_scan_nupiscale_data_def2_h3a_voption.png')
plt.savefig(plots_dir + '/frac'+ str(frac_num) + '/Frac'+str(frac_num)+'_2nv_def2_data_minusvoption.png')


#point_LHS = 0.0
#point_RHS = 0.0
#point_center = 0.0
#print 
#print (point_RHS -point_center)
#print (point_center - point_RHS)
print 'relative error'
print (((right- 0.03)/2.0)/0.03)*100
#print (  (    (point_RHS -point_center) + (point_center - point_RHS) )/2)/point_center
print 'printing left', left
print 'printing right', right
print (right + left)/2.0
