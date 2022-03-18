from tkinter import filedialog, Tk
root = Tk()
root.withdraw()
cwd = filedialog.askdirectory(title='Scripts')
import os, sys
# cwd = 'C:/Users/DTouloumidis/Downloads/Koppen'
sys.path.append(cwd)
from rain_modality import Modality
from koppen import Koppen_classification
from plot_map import plot_it
from export_shapefile import export_tif, tiff_to_shp
import rasterio
import pandas as pd
import numpy as np
from tqdm import tqdm

want_z = input('Do you want to use elevation for Koppen? [y/N]: ', )

if want_z == 'y' or want_z == 'Y' or want_z == 'yes' or want_z == 'Yes' or want_z == 'YES ':
    want_z = 1
elif want_z == 'n' or want_z == 'NO' or want_z == 'no' or want_z == 'No' or want_z == 'NO ':
    want_z = 0
elif len(want_z) == 0:
    want_z = 0


prec_path = filedialog.askdirectory(title='Precipitation Images')
temp_path = filedialog.askdirectory(title='Temperature Images')

if want_z:
    elev_path = filedialog.askopenfilename(title='Elevation Image')
    # elev_path = r'C:\Users\DTouloumidis\Downloads\Koppen\Elev\wc2.1_10m_elev.tif'

# prec_path = 'C:/Users/DTouloumidis/Downloads/Koppen/Prec'
# temp_path = 'C:/Users/DTouloumidis/Downloads/Koppen/Temp'

prec_imgs, temp_imgs, elev_img = [], [], []
for file in os.listdir(prec_path):
    if file.endswith(".tif"):
        prec_imgs.append(os.path.join(prec_path, file))

for file in os.listdir(temp_path):
    if file.endswith(".tif"):
        temp_imgs.append(os.path.join(temp_path, file))

precs = []
for i in prec_imgs:
    precs.append(rasterio.open(i).read())

temps = []
for i in temp_imgs:
    temps.append(rasterio.open(i).read())

if want_z:
    elev = []
    elev.append(rasterio.open(elev_path).read())

with rasterio.open(prec_imgs[0]) as src:
    profile = src.profile

rows, cols = rasterio.open(prec_imgs[0]).shape

# Get rid of Nan values
P = np.reshape(precs, (12, rows, cols))
P = P.astype("float")
P[P < 0] = np.nan

T = np.reshape(temps, (12, rows, cols))
T = T.astype("float")
T[T < -3e+38] = np.nan

if want_z:
    elev = np.reshape(elev, (1, rows, cols))
    elev = elev.astype("float")
    elev[elev == -32768] = np.nan

m = 1195      #GREECE
n = 285       #GREECE

l = 45
k = 45

# m = 0           #X
# n = 0           #Y

# l = rows        #Lenght (Χ)
# k = cols        #Width  (Υ)

mod, flats, peak, med, med2, med3, text, kop = ([] for i in range(8))

for i in tqdm(range(int(n), int(n) + l)):
     for j in range(int(m), int(m) + k):
            P_ = (P[0][i][j], P[1][i][j], P[2][i][j], P[3][i][j], P[4][i][j], P[5][i][j], P[6][i][j], P[7][i][j], P[8][i][j], P[9][i][j], P[10][i][j], P[11][i][j])
            T_ = (T[0][i][j], T[1][i][j], T[2][i][j], T[3][i][j], T[4][i][j], T[5][i][j], T[6][i][j], T[7][i][j], T[8][i][j], T[9][i][j], T[10][i][j], T[11][i][j])
            if want_z:
                z = elev[0][i][j]
            else:
                z = 0
            med.append(P_)
            med2.append(T_)
            med3.append(z)
            if P[0][i][j] >= 0:
                mod.append(sum(Modality(P_)[0]))
                flats.append(Modality(P_)[1])
                peak.append(Modality(P_)[2])
            else:
                mod.append(np.nan)
                flats.append(np.nan)
                peak.append(np.nan)
            if T[0][i][j] >= -300:
                if n <= rows/2:
                    kop.append(Koppen_classification(P_, T_, lat = 1, z = z))
                elif n > rows/2:
                    kop.append(Koppen_classification(P_, T_, lat = -1, z = z))
            else:
                kop.append(np.nan)

koppen_map = plot_it(P, i, j, m, n, k, l, kop, mod, med, Modality, med2, med3)

out = filedialog.askdirectory(title='Export folder')
export_tif(profile, koppen_map, out)
exp = '{}/Koppen.tif'.format(out)
tiff_to_shp(exp, out)
