cd ../

echo "r1"
#Resultado1
python plot_g2_name_all_runs.py 7 2 20 b0_0.1_V_Int_On_
python plot_g2_name_all_runs.py 7 2 20 b0_3_V_Int_On_
python plot_g2_name_all_runs.py 7 2 20 b0_5_V_Int_On_

python plot_g2_name_all_runs.py 7 2 20 b0_0.1_V_Int_Off_
python plot_g2_name_all_runs.py 7 2 20 b0_3_V_Int_Off_
python plot_g2_name_all_runs.py 7 2 20 b0_5_V_Int_Off_

echo "r2"
#Resultado2

python plot_g2_name_all_runs.py 7 1 0 b0_0.1_V_Int_On_
python plot_g2_name_all_runs.py 7 1 0 b0_3_V_Int_On_
python plot_g2_name_all_runs.py 7 1 0 b0_5_V_Int_On_

python plot_g2_name_all_runs.py 7 1 0 b0_0.1_V_Int_Off_
python plot_g2_name_all_runs.py 7 1 0 b0_3_V_Int_Off_
python plot_g2_name_all_runs.py 7 1 0 b0_5_V_Int_Off_

echo "r3"
#Resultado3


python plot_g2_name_all_runs.py 7 0.02 0 b0_0.1_V_Int_On_
python plot_g2_name_all_runs.py 7 0.02 0 b0_3_V_Int_On_
python plot_g2_name_all_runs.py 7 0.02 0 b0_5_V_Int_On_

python plot_g2_name_all_runs.py 7 0.02 0 b0_0.1_V_Int_Off_
python plot_g2_name_all_runs.py 7 0.02 0 b0_3_V_Int_Off_
python plot_g2_name_all_runs.py 7 0.02 0 b0_5_V_Int_Off_











