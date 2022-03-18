import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def plot_it(P, i, j, m, n, k, l, kop, mod, med, Modality, med2, med3):
    #World
    months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec')
    x = np.arange(len(months))
    plt.figure(figsize = (20, 20))
    mapp = P[0].astype("float")
    mapp[np.isnan(mapp)] = -1
    mapp[mapp >= 0] = 1
    plt.imshow(mapp, cmap = 'Paired', interpolation = 'nearest')
    plt.legend([(i,j)])
    currentAxis = plt.gca()
    currentAxis.add_patch(Rectangle((m, n), k, l, fill = None, alpha = 1, color = 'r', lw = 2))
    currentAxis.add_patch(Rectangle((m, n), k, l, alpha = 0.25, color = 'r'))
    plt.grid(color = 'black', ls = '--', alpha = 0.8)
    plt.show();
    
    #Stats
    if not np.isnan(med).all() == True:
        array = pd.DataFrame(np.asarray(med))
        mean = np.nanmean(array, axis = 0)
        median = np.nanmedian(array, axis = 0)
        perc25 = np.nanpercentile((np.asarray(med)), 2.5, axis = 0)
        perc975 = np.nanpercentile((np.asarray(med)), 97.5, axis = 0)
        areamod, areaflat, areapeak = Modality(np.array(median));
        
        if not np.isnan(med2).all() == True:
            array2 = pd.DataFrame(np.asarray(med2))
            mean2 = np.nanmean(array2, axis = 0)
            median2 = np.nanmedian(array2, axis = 0)
            perc25_2 = np.nanpercentile((np.asarray(med2)), 2.5, axis = 0)
            perc975_2 = np.nanpercentile((np.asarray(med2)), 97.5, axis = 0)
        
        if not np.isnan(med3).all() == True:
            median3 = pd.DataFrame(np.asarray(med3))
            maxelev = np.nanmax(median3)
            minelev = np.nanmin(median3)
            median3 = np.nanmedian(median3)
            maxelev = np.nanmax(med3)
            
            #COOL PLOT TEMPERATURE
            plt.figure()
            plt.suptitle('Temperature', fontsize=20, fontweight='bold');
            plt.plot(x, median2);
            plt.plot(x, mean2);
            plt.ylabel('Temperature [oC]');
            plt.plot(months, perc25_2, color = 'blue', alpha=0.2)
            plt.plot(months, perc975_2, color = 'blue', alpha=0.2)
            plt.fill_between(months, perc25_2, perc975_2, alpha=0.1)
            plt.legend(['Median', 'Mean', '95% Quantile'], loc = 'best');
            plt.grid(ls = '--')
        
        if areamod.sum() == 0:
            text = 'Non-modal'
        if areamod.sum() == 1:
            text = 'Unimodal'
        if areamod.sum() == 2:
            text = 'Bimodal'
        if areamod.sum() == 3:
            text = 'Trimodal'
        if areamod.sum() > 3:
            text = 'Multimodal & rest'
        peaky = f'Peaks: {areapeak}'
        
        #COOL PLOT PRECIPITATION
        plt.figure()
        plt.suptitle(text, fontsize=20, fontweight='bold');
        plt.plot(x, median);
        plt.plot(x, mean);
        plt.ylabel('Precipitation [mm]');
        plt.plot(months, perc25, color = 'blue', alpha=0.2)
        plt.plot(months, perc975, color = 'blue', alpha=0.2)
        plt.fill_between(months, perc25, perc975, alpha=0.1)
        plt.legend(['Median', 'Mean', '95% Quantile'], loc = 'best');
        plt.grid(ls = '--')
        plt.show()
    
        if areamod.any() > 0:
            print(peaky)
        if len(areaflat) > 0:
            flaty = f'Flats: {areaflat}'
            print(flaty)
    
        #Location
        plt.figure()
        mapping = np.reshape(mod, ((l, k)))
        colormap1 = plt.imshow(mapping, cmap='coolwarm')
        plt.grid()
        plt.xticks([])
        plt.yticks([])
        cbar2 = plt.colorbar(colormap1, shrink=1)
        cbar2.set_ticks([0, 1, 2, 3, 4])
        cbar2.set_ticklabels(['Non-modal', 'Unimodal', 'Bimodal', 'Trimodal', 'Multimodal & rest'])
    
        plt.figure(figsize = (25, 4))
        Koppen_map = np.reshape(kop, ((l, k)))
        mapping2 = Koppen_map.copy()
    
        mapping2[mapping2 == 'Af'] = 0
        mapping2[mapping2 == 'Am'] = 1
        mapping2[mapping2 == 'As'] = 2
        mapping2[mapping2 == 'Aw'] = 3
        mapping2[mapping2 == 'BWh'] = 4
        mapping2[mapping2 == 'BWk'] = 5
        mapping2[mapping2 == 'BSh'] = 6
        mapping2[mapping2 == 'BSk'] = 7
        mapping2[mapping2 == 'Cfa'] = 8
        mapping2[mapping2 == 'Cfb'] = 9
        mapping2[mapping2 == 'Cfc'] = 10
        mapping2[mapping2 == 'Csa'] = 11
        mapping2[mapping2 == 'Csb'] = 12
        mapping2[mapping2 == 'Csc'] = 13
        mapping2[mapping2 == 'Cwa'] = 14
        mapping2[mapping2 == 'Cwb'] = 15
        mapping2[mapping2 == 'Cwc'] = 16
        mapping2[mapping2 == 'Dfa'] = 17
        mapping2[mapping2 == 'Dfb'] = 18
        mapping2[mapping2 == 'Dfc'] = 19
        mapping2[mapping2 == 'Dfd'] = 20
        mapping2[mapping2 == 'Dsa'] = 21
        mapping2[mapping2 == 'Dsb'] = 22
        mapping2[mapping2 == 'Dsc'] = 23
        mapping2[mapping2 == 'Dsd'] = 24
        mapping2[mapping2 == 'Dwa'] = 25
        mapping2[mapping2 == 'Dwb'] = 26
        mapping2[mapping2 == 'Dwc'] = 27
        mapping2[mapping2 == 'Dwd'] = 28
        mapping2[mapping2 == 'ET'] = 29
        mapping2[mapping2 == 'EF'] = 30
        mapping2[mapping2 == 'HT'] = 31
        mapping2[mapping2 == 'HF'] = 32
        mapping2 = mapping2.astype("float")
           
        plt.imshow(mapping2)
        plt.grid()
        plt.xticks([])
        plt.yticks([])
        plt.colorbar();
        
        return mapping2