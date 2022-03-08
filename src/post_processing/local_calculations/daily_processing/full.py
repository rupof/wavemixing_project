from post_processing.local_calculations.get_g2 import * 
from post_processing.local_calculations.get_cs import * 


import traceback
import sys



c1 = [2.0,20.0]
c2 = [0.02, 0.0]
c3 = [1.0, 0.0]
c4 = [4.0, 40.0]

#c_list = [c1,c2,c3]
c_list = [c4]
#N_list = [i for i in range(1,8)]
N_list = [6,7]
#b0_list = [0.1, 3, 5]
b0_list = [0.1]
ang2_list = [25, 90, 155, -25, -90, 205]

useb0 = 1
kd = None
rho_ss_parameter = "direct"




ang1 = 25
interaction = True
tmax=0
print("c_list:", c_list)
for N in N_list:
    for b0 in b0_list:
        description = f"b0_{b0}_V_Int_On_fixed_"
        for c_i in c_list:
            Omega, Delta = float(c_i[0]), float(c_i[1])
            print("------------- \n", c_i)
            try:
                get_cs_from_all_available_rho_ss(ang1, N, useb0, b0, kd, description, interaction, Omega, Delta, rho_ss_parameter, tmax );
                #continue
                #break
                a=1
            except Exception:
                print(traceback.format_exc())
                print(f"Error for:N{N} and b0:{b0} and {c_i}" )

            for ang2 in ang2_list:
                try:
                    get_g2_from_all_available_rho_ss(ang1,ang2, N, useb0, b0, kd, description, interaction, Omega, Delta, rho_ss_parameter, tmax )
                    a = 1
                except Exception:
                    print(f"Error for:N{N}, b0:{b0} and angle {ang2}" )

