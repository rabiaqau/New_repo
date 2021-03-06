#16_nov_2019

# Parts of script

# import libararies
from ROOT import *
import AtlasStyle
import AtlasUtils
import ROOT
import math
import numpy as np
import os.path
import pickle
import os.path
import pickle
import sys
import glob
#from numbers import *
from functions import *
# all functions
def gaussD(x, p):

    return p[0] * (1.0 / ( math.sqrt(2 * math.pi) * p[2] ) ) * np.exp( - (1.0 / 2.0) * ( (x[0] - p[1])**2 / ( p[2] **2
) ) ) + p[3] * (1.0 / (math.sqrt(2 * math.pi) * p[4] ) ) * np.exp( - (1.0 / 2.0) * ( (x[0] - p[5])**2 / ( p[4] **2) ))





def trklcd(scan_type):
          
      bunches = scan_type[4]
      
      current1 =scan_type[2]
      current2= scan_type[3]
          
      n1= np.mean(current1/bunches)


      n2= np.mean(current2/bunches)

      n1n2 = n1*n2

      sigma_x = scan_type[0][0]

      sigma_y = scan_type[1][0]
          
      expected_lumi =  expected_luminosity(sigma_x,sigma_y,n1n2)
      peak_of_curve = scan_type[0][2]
      fom = peak_of_curve /expected_lumi

      return fom, sigma_x, sigma_y, expected_lumi, peak_of_curve










freq = (1./8.89244e-05) #[s-1] 
inel = 8. * 1e-24
                      
def gauss2D(x, p):
      return p[0] * ( np.exp( - (x[0]-p[1])**2/(2.*p[2]**2) ) * np.exp( - (x[1]-p[3])**2/(2.*p[4]**2)  ))

                      
def expected_luminosity( sigma_x, sigma_y, current ):
      return freq * current * 1e22 / ( sigma_x * sigma_y  * 2.0 * math.pi) / (freq / inel )


def double_gauss2D(x, p):
      return p[0] *(np.exp(-(x[0]-p[1])**2/(2.*p[2]**2)) * np.exp(-(x[1]-p[3])**2/(2.*p[4]**2))+ np.exp( - (x[0]-p[5])**2/(2.*p[6]**2) ) * np.exp( - (x[1]-p[7])**2/(2.*p[8]**2)))


# def double_gauss2D(x, p):


#       return p[0] *( 1.0 / (2 * math.pi) )* ( (1.0 / p[2]/p[4])  * np.exp(-(x[0]-p[1])**2/(2.*p[2]**2)) * np.exp(-(x[1]-p[3])**2/(2.*p[4]**2))+ (1.0 / p[6]/p[8]) * np.exp( - (x[0]-p[5])**2/(2.*p[6]**2) ) * np.exp( - (x[1]-p[7])**2/(2.*p[8]**2)))



          
#fit_pickle_trk = sorted(glob.glob("fits/integrated/fit_integrated_trk_run_348251.pickle"))
#fit_pickle_lcd = sorted(glob.glob("fits/integrated/fit_integrated_lcd_run_348251.pickle"))

fit_pickle_trk = sorted(glob.glob("fits/integrated/*trk*"))
#fit_pickle_lcd = sorted(glob.glob("fits/integrated/*lcd*"))



    # 3.main function (analyze function)
def analyse_scan(separation, luminosity, error, path, run_number, bunches, current, Xscan,early,date):

    # separation --> separation of points(but not corrected one)
    # luminosity 
    # error
    # canvas_name 
    # run_number
    # bunches
    # current

    separation_points = len(separation) # number of points (8,9)depends on scan
    #print separation_points,"sep points"
    # TGraph(A Graph is a graphics object made of two arrays X and Y with npoints each.)
    graph = ROOT.TGraph(separation_points,separation,luminosity)

    #TGraphErrors(A TGraphErrors is a TGraph with error bars.)
    graph = ROOT.TGraphErrors(separation_points, separation, luminosity, np.zeros(separation_points), error ) 
    #TCanvas
    canvas_name = ROOT.TCanvas( 'scan_name', 'scan_name',800, 600 )

    # Canvas Title
    graph.GetXaxis().SetTitle("separation[mm]")
    graph.GetYaxis().SetTitle("mu")
    graph.GetXaxis().SetTitleSize(0.064)
    graph.GetYaxis().SetTitleSize(0.064)

    #Single gauss Fit 
    single_gauss_fit = ROOT.TF1( "single_gauss_fit", 'gaus', -0.05, 0.05 )# single gauss (3 parameters)
    #Double gauss Fit
    double_gauss_fit = ROOT.TF1("double_gauss_fit", gaussD, -0.05, 0.05, 6)#2d gauss (5 parameters)

    # fitting the graph with single gauss fit
    graph.Fit('single_gauss_fit','Q')
    # title
    graph.GetXaxis().SetTitle("separation")
    graph.GetYaxis().SetTitle("mu")


# for my fucntions

    amp1 = single_gauss_fit.GetParameter(0)
    #print amp1,"amp1"

    m1 = single_gauss_fit.GetParameter(1)
#    print m1,"m1"
    s1 = single_gauss_fit.GetParameter(2)
#    print s1,"s1"

    # getting value for the double gauss fit before we have only constant term

    amp1 = amp1 * s1 * math.sqrt(2*math.pi)
    #print amp1,"amp1"
    double_gauss_fit.SetParameter(0,0.5*amp1)#amplitude          

    double_gauss_fit.SetParameter(3,0.5*amp1)#amplitude2
    double_gauss_fit.SetParameter(4,2*s1)#sigma2
    

    double_gauss_fit.SetParameter(1,m1)#mean1 (349592)
    double_gauss_fit.SetParameter(2,s1)#sigma1 

    double_gauss_fit.SetParameter(5,m1)#mean(349592)
  
   
    if  run_number == 349592:# only early run
        double_gauss_fit.SetParameter(4, 0.021)#sigma2 (349592)
        double_gauss_fit.SetParameter(1,0.00053)#mean1 (349592)            
        double_gauss_fit.SetParameter(5,0.0019)#mean(349592)            


    if  run_number == 349841:# only early run
        if early and Xscan:

            double_gauss_fit.SetParameter(0,amp1 * 0.60)#amplitude
            double_gauss_fit.SetParameter(3,0.40 * amp1)#amplitude2                               
        if early and not Xscan:

            double_gauss_fit.SetParameter(0,amp1 * 0.60)#amplitude
            double_gauss_fit.SetParameter(3,0.40 * amp1)#amplitude2                               
            double_gauss_fit.SetParameter(4,s1 * 1.5)#sigma2

    
    if  run_number == 355389:# only early run
        if early and Xscan:

            double_gauss_fit.SetParameter(0,amp1 * 0.80)#amplitude
            double_gauss_fit.SetParameter(3,0.20 * amp1)#amplitude2                               



    if  run_number == 363910:# only early run
        if early and not Xscan:

            double_gauss_fit.SetParameter(0,amp1 * 0.90)#amplitude
            double_gauss_fit.SetParameter(3,0.10 * amp1)#amplitude2                               

    if  run_number == 351223:# only early run
        if not early and not Xscan:

            double_gauss_fit.SetParameter(0,amp1 * 0.60)#amplitude
            double_gauss_fit.SetParameter(3,0.40 * amp1)#amplitude2                               

    if  run_number == 352448:# only early run
        if early and Xscan:

            double_gauss_fit.SetParameter(0,amp1 * 0.80)#amplitude
            double_gauss_fit.SetParameter(3,0.20 * amp1)#amplitude2                               

    if  run_number == 355331:# only early run
        if early and not Xscan:

            double_gauss_fit.SetParameter(0,amp1 * 0.80)#amplitude
            double_gauss_fit.SetParameter(3,0.20 * amp1)#amplitude2                               


    if  run_number == 352107:# only early run
        if early and not Xscan:

            double_gauss_fit.SetParameter(0,amp1 * 0.90)#amplitude
            double_gauss_fit.SetParameter(3,0.10 * amp1)#amplitude2                               
    
    if  run_number == 355416:# only early run
        if not Xscan and early:
            double_gauss_fit.SetParameter(0,amp1 * 0.70)#amplitude
            double_gauss_fit.SetParameter(3,0.30 * amp1)#amplitude2                               
            double_gauss_fit.SetParameter(4,s1 * 1.8)#sigma2

    if  run_number == 363129:# only early run
        double_gauss_fit.SetParameter(0,amp1 * 0.70)#amplitude
        double_gauss_fit.SetParameter(3,0.30 * amp1)#amplitude2                               
        double_gauss_fit.SetParameter(4,s1 * 1.8)#sigma2
        
    if  run_number == 350160:# only early run
        if early and Xscan:
            double_gauss_fit.SetParameter(4,s1 * 1.5)#sigma2

    
    if  run_number == 357821:# only early run
        double_gauss_fit.SetParameter(4,s1 * 1.8)#sigma2


    if  run_number == 360402:# only early run
        double_gauss_fit.SetParameter(0,amp1 * 0.70)#amplitude
        double_gauss_fit.SetParameter(3,0.30 * amp1)#amplitude2                               
        double_gauss_fit.SetParameter(4,s1 * 1.8)#sigma2


    
    if  run_number == 354124:# only early run
        double_gauss_fit.SetParameter(0,amp1 * 0.70)#amplitude
        double_gauss_fit.SetParameter(3,0.30 * amp1)#amplitude2                               
        double_gauss_fit.SetParameter(4,s1 * 1.5)#sigma2


    if  run_number == 350310:# only early run
        double_gauss_fit.SetParameter(0,amp1 * 0.70)#amplitude
        double_gauss_fit.SetParameter(3,0.30 * amp1)#amplitude2                               
        double_gauss_fit.SetParameter(4,s1 * 1.5)#sigma2
    if  run_number == 359124:

        if not Xscan and early:
            double_gauss_fit.SetParameter(0,amp1 * 0.90)#amplitude
            double_gauss_fit.SetParameter(3,0.10 * amp1)#amplitude2                          
    if  run_number == 359058:

        if  Xscan and early:
            double_gauss_fit.SetParameter(0,amp1 * 0.90)#amplitude
            double_gauss_fit.SetParameter(3,0.10 * amp1)#amplitude2                          

        
    if  run_number == 362661:

        if not Xscan and early:
            double_gauss_fit.SetParameter(0,amp1 * 0.60)#amplitude
            double_gauss_fit.SetParameter(3,0.40 * amp1)#amplitude2                               

    if  run_number == 362445:
        if  Xscan and not early:    
            double_gauss_fit.SetParameter(0,amp1 * 0.80)#amplitude1        
            double_gauss_fit.SetParameter(3,0.20 * amp1)#amplitude2                               
            double_gauss_fit.SetParameter(4,s1 * 1.5)#sigma2
    if  run_number == 349481:
 
            double_gauss_fit.SetParameter(0,amp1 * 0.60)#amplitude1        
            double_gauss_fit.SetParameter(3,0.40 * amp1)#amplitude2                               

    if  run_number == 350013:
        if  Xscan and early:    
            double_gauss_fit.SetParameter(0,amp1 * 0.70)#amplitude1        
            double_gauss_fit.SetParameter(3,0.30 * amp1)#amplitude2                               

    if  run_number == 349693:
        if  Xscan and early:    
            double_gauss_fit.SetParameter(0,amp1 * 0.70)#amplitude1        
            double_gauss_fit.SetParameter(3,0.30 * amp1)#amplitude2                               
    
    if  run_number == 350440:
        if  not Xscan and early:    
            double_gauss_fit.SetParameter(0,amp1 * 0.70)#amplitude1        
            double_gauss_fit.SetParameter(3,0.30 * amp1)#amplitude2                               
    
    if  run_number == 350880:
        if  not Xscan and early:    
            double_gauss_fit.SetParameter(0,amp1 * 0.60)#amplitude1        
            double_gauss_fit.SetParameter(3,0.40 * amp1)#amplitude2                               
    
    if  run_number == 355468:
        if  not Xscan and early:    
            double_gauss_fit.SetParameter(0,amp1 * 0.90)#amplitude1        
            double_gauss_fit.SetParameter(3,0.10 * amp1)#amplitude2                               

    
    if  run_number == 357620:
        if  not Xscan and not early:    
            double_gauss_fit.SetParameter(0,amp1 * 0.90)#amplitude1        
            double_gauss_fit.SetParameter(3,0.10 * amp1)#amplitude2                               
    
    if  run_number == 358031:
        if  not Xscan and early:    
            double_gauss_fit.SetParameter(0,amp1 * 0.60)#amplitude1        
            double_gauss_fit.SetParameter(3,0.40 * amp1)#amplitude2                               
            double_gauss_fit.SetParameter(4,s1 * 1.5)#sigma2

    if  run_number == 358615:
        if  not Xscan and not early:    
            double_gauss_fit.SetParameter(0,amp1 * 0.60)#amplitude1        
            double_gauss_fit.SetParameter(3,0.40 * amp1)#amplitude2                               

    
    if  run_number == 359735:
        if  not Xscan and not early:    
            double_gauss_fit.SetParameter(0,amp1 * 0.60)#amplitude1        
            double_gauss_fit.SetParameter(3,0.40 * amp1)#amplitude2                               
    
    if  run_number == 359541:
        if Xscan and  early:    
            double_gauss_fit.SetParameter(0,amp1 * 0.60)#amplitude1        
            double_gauss_fit.SetParameter(3,0.40 * amp1)#amplitude2
            double_gauss_fit.SetParameter(3,0.40 * amp1)#amplitude2                               
    if  run_number == 364098:
        if  not Xscan and not early:    
            double_gauss_fit.SetParameter(0,amp1 * 0.60)#amplitude1        
            double_gauss_fit.SetParameter(3,0.40 * amp1)#amplitude2                               
    

    # fit double gauss                                                        
 
    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.SetHeader("Double Gauss Fit")
    legend.AddEntry(graph,"data","P")
    legend.AddEntry(double_gauss_fit,"fit","L")
 

    graph.Fit('double_gauss_fit','Q')#fitting of double gaussain

    


    ###########
    double_gauss_fit.ReleaseParameter(3)
    double_gauss_fit.ReleaseParameter(4)
    
    

    # chi2 from fit before correction
    chi2_double_gauss_fit = double_gauss_fit.GetChisquare()

    NDF_double_gauss_fit =  double_gauss_fit.GetNDF()
                      

    Prob_double_gauss_fit = double_gauss_fit.GetProb()
    
    chi_NDF_double_gauss_fit= chi2_double_gauss_fit/NDF_double_gauss_fit#ratio chi/NDF 
    round_chi_double_gauss_fit = round(chi2_double_gauss_fit,2)#round off the value    
    round_chi_NDF_double_gauss_fit = round(chi_NDF_double_gauss_fit,2)# 
    


#    mean_double_gauss =  double_gauss_fit.Mean(-5,5) ,"mean of double gauss"
 
    graph.SetLineColor( 38 )
    graph.SetMarkerColor( 4 )
    graph.SetMarkerStyle( 20 )
    graph.SetMarkerSize( 1.1 )
  
    # colors                            
    canvas_name.SetFillColor(18)
    canvas_name.SetGrid()
    canvas_name.SetGridx()
    canvas_name.SetGridy()


    legend.SetTextSize(0.03)
    legend.Draw()

    graph.Draw("AP")

    # ****** without corrected separation *****    

    # chi2 value
    # luminsoity from fit (each point)
  
    chi2_uncorrected = np.array([])
    lumi_fit = gaussD([separation], double_gauss_fit.GetParameters())


    # looping on all separation points
    # to get lumionsity of each separation points
    # lastly calculate the chi2
#     subtraction_lumi = np.array([])# array for subration_lumi

#     for sep in range(separation_points):  # looping 
#           print sep,"sep"
#           print luminosity[sep],"luminsoity given"
#           print lumi_fit[sep],"leminosity from fit"
#           subtraction_luminosity = (luminosity[sep]- lumi_fit[sep])
#           subtraction_lumi= np.append(subtraction_lumi,subtraction_luminosity)
#           chi2 = ((luminosity[sep]- lumi_fit[sep])/error[sep])**2# chi2 formula
#           chi2_uncorrected = np.append(chi2_uncorrected,chi2)
        
    
# #canvas
#     test = ROOT.TGraphErrors(len(separation), separation,subtraction_lumi,np.zeros(separation_points), error)
    
    c = ROOT.TCanvas('sub_lumi', 'sub_lumi')
    c.Divide(1,2) # 1 row, 2 columns
    c.cd(1)
    graph.GetXaxis().SetTitle("separation[mm]")
    graph.GetYaxis().SetTitle("mu")
    graph.GetXaxis().SetTitleSize(0.064)
    graph.GetYaxis().SetTitleSize(0.064)


    graph.Draw("AP")

    legend = ROOT.TLegend(0.75, 0.6, 0.9, 0.86)
   # legend.SetHeader("Double Gauss Fit")# for lagend header                    
    legend.AddEntry(graph,"data","P")# points                                      
    legend.AddEntry(double_gauss_fit," Fit","L")# 
    legend.AddEntry(0,'#chi^{2}='+str(round_chi_double_gauss_fit), '')# chi2
    legend.AddEntry(0,'#chi^{2}/ndf='+str(round_chi_NDF_double_gauss_fit), '')# chi
    legend.SetTextSize(0.055)

    label= ROOT.TLatex()
    label.SetTextSize(0.058)
    label.DrawLatexNDC(0.75,0.90,"#bf{Double Gauss Fit}")# horizontal, vertical
    label.SetTextColor(4)

    legend.Draw()


    c.cd(2)
    # test.Draw("AP")

    # test.SetLineColor( 38 )
    # test.SetMarkerColor( 4 )
    # test.SetMarkerStyle( 20 )
    # test.SetMarkerSize( 1.3 )


    # test.GetXaxis().SetTitle("Separation[mm]");
    # test.GetYaxis().SetTitle("lumi[data]-lumi[fit]");
    # test.GetXaxis().SetTitleSize(0.064)
    # test.GetYaxis().SetTitleSize(0.064)
    # #test.SetTitleY(0.1)
    # # line                                                                                                                                     
    # line = TLine(-0.037,0,0.037,0.0)
    # line.SetLineColor(2)
    # line.SetLineWidth(1)
    # line.Draw()

    # path
    # fileName = path + str(run_number) +"_"+str(scan)+"_"
    # if Xscan== True:
    #     fileName += "x_scan_comp.png"
    # else:
    #     fileName += "y_scan_comp.png"
    # c.Print(fileName)
    
    # sigma
    def sigma_fit():

        peak = double_gauss_fit.GetMaximum()

        intlimit = 0.1        
        integral = double_gauss_fit.Integral(-intlimit,intlimit)
     
        sigma = (1 / math.sqrt (2 * math.pi)) * integral /peak 
             
        return sigma, peak
    sigma_fit = sigma_fit()
    sigma = sigma_fit[0]
    peak =  sigma_fit[1]
    
    
    # path
    graph.Draw("AP")
    # fileName = path + str(run_number) +"_"+str(scan)+"_"
    # if Xscan == True:
    #     fileName = fileName +"x_scan.png"
    # else:
    #     fileName = fileName+ "y_scan.png"
        
    # canvas_name.Print(fileName)

    return sigma, chi_NDF_double_gauss_fit, peak, chi2_double_gauss_fit



def analyse( input_data ):
      
    sep_x =  input_data['sep_x']
    sep_y =  input_data['sep_y']
    exp_lumi_x = input_data['exp_lumi_y']
    exp_lumi_y = input_data['exp_lumi_y']

    err_x = input_data['err_x']
    err_y = input_data['err_y']
    curr_0 = input_data['curr'][0]
    curr_1 = input_data['curr'][1]
    date =  input_data['date']
    bunches = input_data['bunches']
    early = input_data['early']
    run_number = input_data['run']

                      
    result_1 = analyse_scan(sep_x, exp_lumi_x ,err_x ,"Emittance_scan/", run_number, bunches, curr_0, True, early,date )


    result_2 =  analyse_scan(sep_y, exp_lumi_y ,err_y ,"Emittance_scan/", run_number, bunches, curr_1, False , early, date )
    return( result_1, result_2,curr_0,curr_1,bunches, run_number )






#### arrays section

track =np.array([])
lucid = np.array([])

# array for FOM of track and luci
early_1d_dgauss_fom_tc = np.array([])
late_1d_dgauss_fom_tc = np.array([])

early_1d_dgauss_peak_tc = np.array([])
late_1d_dgauss_peak_tc = np.array([])



early_2d_sgauss_fom_tc = np.array([])
late_2d_sgauss_fom_tc = np.array([])


early_2d_dgauss_fom_tc = np.array([])
late_2d_dgauss_fom_tc = np.array([])



### runs
early_run_number = np.array([])
late_run_number = np.array([])

# array for the lucid

early_fom_lcd= np.array([])

late_fom_lcd= np.array([])





##### peak arrays

early_x_scan= np.array([])
early_y_scan = np.array([])


late_x_scan= np.array([])
late_y_scan = np.array([])




# selection of pickle file

# Track 
if fit_pickle_trk:


      for filename in fit_pickle_trk:
            with open(filename,'rb') as fit_pickle_trk:
                  scans = pickle.load(fit_pickle_trk)
                  print scans.key()
                  Tight_mod= scans['TightModLumi']

                  for i_scan in range(len(Tight_mod)):
                        output = Tight_mod[i_scan]

                        
                        if output['early']==True:
                              fom_early=  trklcd(analyse(output))[0]


                              early_1d_dgauss_fom_tc = np.append(early_1d_dgauss_fom_tc,fom_early)

                              run_number_early = analyse(output)[5]

                              early_run_number = np.append(early_run_number,run_number_early)
                        if output['early']==False:

                              fom_late = trklcd(analyse(output))[0]

                              late_1d_dgauss_fom_tc = np.append(late_1d_dgauss_fom_tc,fom_late)

                              run_number_late =  analyse(output)[5]

                              late_run_number = np.append(late_run_number, run_number_late)
                              #print trklcd(analyse(output))[3],"expected lumi"
                              #print trklcd(analyse(output))[4],"peak of curve"
                        #track = np.append(track,output)

print len(early_run_number),"early run"
print len(late_run_number),"late"
print len(early_1d_dgauss_fom_tc),"early"
print len(late_1d_dgauss_fom_tc),"late"

print early_run_number,"early run"
print late_run_number,"late"
print early_1d_dgauss_fom_tc,"early"
print late_1d_dgauss_fom_tc,"late"



no_early_1d_dgauss_fom_tc =len(early_1d_dgauss_fom_tc)
plot_graph("fom/early_1d_dgauss_fomVsRun_tc.png", "early_1d_dgauss_fom_tc", no_early_1d_dgauss_fom_tc, early_run_number ,early_1d_dgauss_fom_tc,"run","early_fom1d")


no_late_1d_dgauss_fom_tc =len(late_1d_dgauss_fom_tc)
plot_graph("fom/late_1d_dgauss_fomVsRun_tc.png", "late_1d_dgauss_fom_tc", no_late_1d_dgauss_fom_tc, late_run_number ,late_1d_dgauss_fom_tc,"run","late_fom1d")




# # Lucid
# if fit_pickle_lcd:
#       for filename in fit_pickle_lcd:
#             with open(filename,'rb') as fit_pickle_lcd:
#                   scans = pickle.load(fit_pickle_lcd)

#                   for i_scan in range(len(scans)):

#                         output_lcd = scans[i_scan]
#                         lucid = np.append(lucid, output_lcd)




# # loading of both track and lucid files


# saveObject = (track,lucid)



# with open("test.pickle", "wb") as f:
#       pickle.dump(saveObject,f)


# with open ("test.pickle","rb") as f:
#       testout = pickle.load(f)


# trackLucid function
 
            
# tracking data
#       

#             # early scan result

#                   # sigma or width of x and y scan

#                   sigma_x = trklcd(analyse(i))[1]
#                   sigma_y = trklcd(analyse(i))[2]
 


                  
#                   # peak of x and y scan
#                   # centering_correction_y = np.exp( - ( mean[0] / math.sqrt(2) / sigma_y  )**2 )
#                   # print centering_correction_y,"centering correction y"
                  
#                   # peak 
                  

#                   early_1d_dgauss_peak_tc = np.append(early_1d_dgauss_peak_tc,analyse(i)[0][2])

# #                  peak_x_1d_double_gauss = analyse(i)[0][2] / centering_correction_y
# #                  print peak_x_1d_double_gauss,"peak after correction"

                  
#                 #  peak_y_1d_double_gauss = analyse(i)[1][2] * centering_correction_x
#                 #  print peak_y_1d_double_gauss,"after centering correction for y"
#                   # fom of 1d double gauss function 
#                   
#                   print early_1d_dgauss_fom_tc
#                   # fom early




#  #                 print early_1d_dgauss_fom_tc /centering_correction_y,"fom after centgaring correction"
#  #                 print early_1d_dgauss_fom_tc * centering_correction_y,"fom after centgaring correction"
                  
#                   #if <0.95:
# #                  print trklcd(analyse(i))[0],"fom of 1d double gasus function "
# #                  print peak_x_1d_double_gauss,"peak of x scan 1d double gauss"
# #                  print analyse(i)[4]
#                   # print analyse(i)[5],"run number"
#             if i['early']== False:#early x and y scan
#                   # late run
# #                  print analyse(i)[0][4],"mean of fucntion late"
#                   late_run_number = np.append(late_run_number,analyse(i)[5])
#                   late_1d_dgauss_fom_tc = np.append(late_1d_dgauss_fom_tc,trklcd(analyse(i))[0])
#                   print late_1d_dgauss_fom_tc,"late"
#                   late_1d_dgauss_peak_tc =  np.append(late_1d_dgauss_peak_tc,analyse(i)[0][2])







#             peak = analyse(i)[0][2] # peak for 2d fit
#             width_x = analyse(i)[0][0]# peak for 2d fit
#             width_y = analyse(i)[1][0]#peak for 2d fit

#             # 2d fit single gaussian fit
                     
#             sep_x_2d= np.append(i['sep_x'], np.zeros(len(i['sep_y'])))# 2d

#             sep_y_2d= np.append( np.zeros(len(i['sep_x'])), i['sep_y'])#2d

#             exp_lumi_2d =np.append(i['exp_lumi_x'],i['exp_lumi_y'])#2d

#             graph_2d= ROOT.TGraph2D(len(sep_x_2d),sep_x_2d , sep_y_2d , exp_lumi_2d)# 2d fit


#             gauss2d = ROOT.TF2("gauss2d", gauss2D, -3, 3, -3, 3, 5)#2d gauss (5 parameters)


#             gauss2d.SetParameter(0,peak)# amplitude,# 2d fit      

#             gauss2d.SetParameter(1,0)# mean1,# 2d fit                                                             
#             gauss2d.SetParameter(2,width_x)# sigma1,# 2d fit                                                  
#             gauss2d.SetParameter(3,0)# mean2,# 2d fit                                                             
#             gauss2d.SetParameter(4,width_y)# sigma2,# 2d fit                                                  

#             graph_2d.Fit('gauss2d','Q')# fitting 2d fit


#             #### 2d double gaussian function


#             double_graph_2d= ROOT.TGraph2D(len(sep_x_2d),sep_x_2d , sep_y_2d , exp_lumi_2d)# 2d fit
#             double_gauss2d = ROOT.TF2("double_gauss2d", double_gauss2D, -3, 3, -3, 3, 9)#


#             double_gauss2d.SetParameter(0,peak)# amplitude,# 2d fit      

#             double_gauss2d.SetParameter(1,-0.0712)# mean1,# 2d fit                                                             
#             double_gauss2d.SetParameter(2,width_x)# sigma1,# 2d fit                                                  
#             double_gauss2d.SetParameter(3,-0.00141)# mean2,# 2d fit                                                             
#             double_gauss2d.SetParameter(4,width_y)# sigma2,# 2d fit                                                  
#             double_gauss2d.SetParameter(5,-0.00320)# mean

#             double_gauss2d.SetParameter(6,width_x)

#             double_gauss2d.SetParameter(7,0.000564)# mean

#             double_gauss2d.SetParameter(8,width_y)


#             double_graph_2d.Fit('double_gauss2d','Q')# fitting 2d fit
            
            
       
#             # # fom early
#             if i['early']== True:#early x and y scan


#                   NDF_2d= double_gauss2d.GetNDF()

                        
#                   fom_2d= double_gauss2d.GetParameter(0)/trklcd(analyse(i))[3]
#                   # if fom_2d < 0.90 :
#                   #       print trklcd(analyse(i))[3],"expectetion lumi"
#                   #       print fom_2d,"fom2d"
#                   #       print double_gauss2d.GetMaximum(),"double gausssian 2d"
#                   #       print NDF_2d,"NDF "
#                   #       print analyse(i)[5],"early run number"
                  
#                   # Early
#                   _2d_dgauss_fom_tc = np.append(early_2d_dgauss_fom_tc,fom_2d)


#             # fom late
#             if i['early']== False:# late x and y
#                   fom_2d= double_gauss2d.GetParameter(0)/trklcd(analyse(i))[3]
#                   late_2d_dgauss_fom_tc = np.append(late_2d_dgauss_fom_tc,fom_2d)
#                   # if fom_2d < 0.90 :
#                   #       print "late scan"
#                   #       print trklcd(analyse(i))[3],"expectetion lumi"
#                   #       print fom_2d,"fom2d"
#                   #       print double_gauss2d.GetMaximum(),"double gausssian 2d"
#                   #       print NDF_2d,"NDF "
#                   #       print analyse(i)[5],"early run number"

# # lucid data
#       for i in testout[1]:
           
#             if i['early']== True:

#                   early_lucid =trklcd(analyse(i))
#                   early_fom_lcd = np.append(early_fom_lcd,early_lucid[0])

              
#             if i['early']== False:
#                         late_lucid =trklcd(analyse(i))
#                         late_fom_lcd= np.append(late_fom_lcd, late_lucid[0])
              


# # graph plotting section
# # fom
# ROOT.TGaxis.SetMaxDigits(6)



# # mu Vs FOM


# no_early_1d_dgauss_fom_tc =len(early_1d_dgauss_fom_tc)
# plot_graph("fomvsmu/early_1d_dgauss_fomVsmu_tightmode_tc.png", "early_1d_dgauss_fom_tc", no_early_1d_dgauss_fom_tc, early_1d_dgauss_peak_tc ,early_1d_dgauss_fom_tc,"peak","fom")

# multigraph("fomvsmu/fomVsmu_earlylate.png", len(early_1d_dgauss_fom_tc), len(late_1d_dgauss_fom_tc), early_1d_dgauss_peak_tc, early_2d_dgauss_fom_tc, late_1d_dgauss_peak_tc, late_2d_dgauss_fom_tc )







# multigraph("fom/early_fom1d2d_doublegauss.png", len(early_2d_dgauss_fom_tc), len(early_1d_dgauss_fom_tc), early_run_number, early_2d_dgauss_fom_tc,early_run_number,early_1d_dgauss_fom_tc)

# multigraph("fom/late_fom1d2d_doublegauss.png", len(late_2d_dgauss_fom_tc), len(late_1d_dgauss_fom_tc), late_run_number, late_2d_dgauss_fom_tc,late_run_number,late_1d_dgauss_fom_tc)






            
            








