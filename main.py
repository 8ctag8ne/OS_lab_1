import stats 
import file_helper as fh
import two_pointers_technique as tp
import majority_graph as maj
import logarithmic_histogram as log_hist
input_list = fh.get_sizes("file_size_sys.csv")
# maj.save_visualizations(input_list)
# print(tp.get_answer(input_list, 0.9))
stats.analyze_file_sizes(input_list)