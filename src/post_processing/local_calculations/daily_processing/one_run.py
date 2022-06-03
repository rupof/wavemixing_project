from post_processing.local_calculations.get_g2 import * 
from post_processing.local_calculations.get_cs import * 
import sys

ang1 = float(sys.argv[1]) ##this is a useless parameter
print(f"ang1 = {ang1}")
ang2 = float(sys.argv[2]) ##This is a useless parameter
print(f"ang2 = {ang2}")
N = int(sys.argv[3])
print(f"N = {N}")
useb0 = bool(int(sys.argv[4]))
print(f"useb0 = {useb0}")


if useb0 == True:
    b0 = float(sys.argv[5])
    kd = None
    exc_radius = None
    description = str(sys.argv[6])
    print(f"b0 = {b0}, description = {description}")
    # ang1 ang2 N useb0 b0 description interaction Omega Delta
else:
    b0 = None
    kd = float(sys.argv[5])
    exc_radius = float(sys.argv[6])
    description = str(sys.argv[7])
    # ang1 ang2 N useb0 kd exc_radius description
    print("kd main", kd) 
interaction = bool(int(sys.argv[7]))
print(f"interaction = {interaction}")
Omega = float(sys.argv[8])
print(f"Omega = {Omega}")
Delta = float(sys.argv[9])
print(f"Delta = {Delta}")
rho_ss_parameter = str(sys.argv[10])
print(f"rho_ss_parameter = {rho_ss_parameter}")
tmax = float(sys.argv[11])
print(f"tmax = {tmax}")
start_index=int(sys.argv[12])

get_g2_from_all_available_rho_ss(ang1,ang2, N, useb0, b0, kd, description, interaction, Omega, Delta, rho_ss_parameter, tmax, start_index)

