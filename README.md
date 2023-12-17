# SNACS_IM_LU

run the script with

python main.py -r [run,wiki,enron,time,spread,both,bar] -p [wiki,enron] -n [int] -k [int]

k seed size for single run if None provided runs script from seed 1 to 50 standard

n number of parallel workers in case multiple seed sizes can be run

r whether to run the algorithms on (run for both wiki and enron) just wiki, just enron, or make a plot of the time, spread or both, or a bar plot

p in case of plotting whether to plot enron or wiki data

this returns a text file of the selected dataset to run for the selected algorithms
the selected algorithms have to be adjusted in the main.py file under the set_algorithms function.