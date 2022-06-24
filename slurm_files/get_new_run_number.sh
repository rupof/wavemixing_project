#!/usr/bin/bash                                                                                                                          
 
#Given the full path without number and extension, this script returns the new number for the simulation
 #
 
full_path_without_results=$1
path=${full_path_without_results%/*}
filename=${full_path_without_results##*/}
 
extension="$2"
results_path="../results/"
 
 #echo $full_path_without_results
 
if [ -f "$results_path${full_path_without_results}0.$extension" ]; then
# if above path exists
        full_path_without_results_without_extension=${full_path_without_results} # ${var%.${extension}}
        current_largest_simulation_full_name="$(ls $results_path${full_path_without_results_without_extension}*.$extension | sort -r --version-sort | head -1)"
        #echo $current_largest_simulation_full_name
        current_largest_simulation_number=$(echo ${current_largest_simulation_full_name%.*} | grep -Eo '[0-9]+$')
        #echo $current_largest_simulation_number
        new_simulation_number=$(($current_largest_simulation_number+1))
        #new_simulation_full_name=$new_simulation_number$extension
        #mv $name_of_file $new_simulation_full_name
fi
echo $new_simulation_number                    
