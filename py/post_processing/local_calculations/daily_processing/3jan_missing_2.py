from post_processing.local_calculations.get_g2 import * 
from post_processing.local_calculations.get_cs import * 


import traceback
import sys

"""
get_g2_from_all_available_rho_ss(25,25, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,90, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,155, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-25, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-90, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,205, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 2.0, 20.0, "direct", 0 ) 
"""



get_g2_from_all_available_rho_ss(25,25, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 0.02, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,90, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 0.02, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,155, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 0.02, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-25, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 0.02, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-90, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 0.02, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,205, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 0.02, 0.0, "direct", 0 ) 




get_g2_from_all_available_rho_ss(25,25, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 1.0, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,90, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 1.0, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,155, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 1.0, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-25, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 1.0, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-90, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 1.0, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,205, 6, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 1.0, 0.0, "direct", 0 ) 



get_g2_from_all_available_rho_ss(25,25, 6, 1, 0.1, 0 , "b0_0.1_V_Int_Off_fixed", False, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,90, 6, 1, 0.1, 0 , "b0_0.1_V_Int_Off_fixed", False, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,155, 6, 1, 0.1, 0 , "b0_0.1_V_Int_Off_fixed", False, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-25, 6, 1, 0.1, 0 , "b0_0.1_V_Int_Off_fixed", False, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-90, 6, 1, 0.1, 0 , "b0_0.1_V_Int_Off_fixed", False, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,205, 6, 1, 0.1, 0 , "b0_0.1_V_Int_Off_fixed", False, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,25, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,90, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,155, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-25, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-90, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,205, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,25, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 0.02, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,90, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 0.02, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,155, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 0.02, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-25, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 0.02, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-90, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 0.02, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,205, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 0.02, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,25, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 1.0, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,90, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 1.0, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,155, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 1.0, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-25, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 1.0, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-90, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 1.0, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,205, 7, 1, 0.1, 0 , "b0_0.1_V_Int_On_fixed", True, 1.0, 0.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,25, 7, 1, 0.1, 0 , "b0_0.1_V_Int_Off_fixed", False, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,90, 7, 1, 0.1, 0 , "b0_0.1_V_Int_Off_fixed", False, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,155, 7, 1, 0.1, 0 , "b0_0.1_V_Int_Off_fixed", False, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-25, 7, 1, 0.1, 0 , "b0_0.1_V_Int_Off_fixed", False, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,-90, 7, 1, 0.1, 0 , "b0_0.1_V_Int_Off_fixed", False, 2.0, 20.0, "direct", 0 ) 
get_g2_from_all_available_rho_ss(25,205, 7, 1, 0.1, 0 , "b0_0.1_V_Int_Off_fixed", False, 2.0, 20.0, "direct", 0 ) 
