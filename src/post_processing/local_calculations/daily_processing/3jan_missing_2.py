from post_processing.local_calculations.get_g2 import * 
from post_processing.local_calculations.get_cs import * 


import traceback
import sys

"""
get_g2_from_all_available_rho_ss(25,25, N, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed_", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,90, N, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed_", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,155, N, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed_", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-25, N, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed_", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-90, N, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed_", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,205, N, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed_", True, 2.0, 20.0, "direct", 0 ) 
"""


for N in range(4,8):
    get_g2_from_all_available_rho_ss(25,25, N, 1, 3, 0 , "b0_3_V_Int_On_fixed_", True, 0.02, 0.0, "direct", 0 ) 
    get_g2_from_all_available_rho_ss(25,90, N, 1, 3, 0 , "b0_3_V_Int_On_fixed_", True, 0.02, 0.0, "direct", 0 ) 
    get_g2_from_all_available_rho_ss(25,155, N, 1, 3, 0 , "b0_3_V_Int_On_fixed_", True, 0.02, 0.0, "direct", 0 ) 
    get_g2_from_all_available_rho_ss(25,-25, N, 1, 3, 0 , "b0_3_V_Int_On_fixed_", True, 0.02, 0.0, "direct", 0 ) 
    get_g2_from_all_available_rho_ss(25,-90, N, 1, 3, 0 , "b0_3_V_Int_On_fixed_", True, 0.02, 0.0, "direct", 0 ) 
    get_g2_from_all_available_rho_ss(25,205, N, 1, 3, 0 , "b0_3_V_Int_On_fixed_", True, 0.02, 0.0, "direct", 0 ) 


    get_g2_from_all_available_rho_ss(25,25, N, 1, 5, 0 , "b0_5_V_Int_On_fixed_", True, 0.02, 0.0, "direct", 0 )
    get_g2_from_all_available_rho_ss(25,90, N, 1, 5, 0 , "b0_5_V_Int_On_fixed_", True, 0.02, 0.0, "direct", 0 )
    get_g2_from_all_available_rho_ss(25,155, N, 1, 5, 0 , "b0_5_V_Int_On_fixed_", True, 0.02, 0.0, "direct", 0 )
    get_g2_from_all_available_rho_ss(25,-25, N, 1, 5, 0 , "b0_5_V_Int_On_fixed_", True, 0.02, 0.0, "direct", 0 )
    get_g2_from_all_available_rho_ss(25,-90, N, 1, 5, 0 , "b0_5_V_Int_On_fixed_", True, 0.02, 0.0, "direct", 0 )
    get_g2_from_all_available_rho_ss(25,205, N, 1, 5, 0 , "b0_5_V_Int_On_fixed_", True, 0.02, 0.0, "direct", 0 )



