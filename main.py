import time
import os
import shutil
from src.cpu_single import SingleCPUProcessor
from src.cpu_multithread import MultiCPUProcessor
from src.spark_processor import Spark  # Updated import
from src.visualize import visualize_times, visualize_bar_chart

# This is for creating and removing folder 
def clean_output_folder(folder_path):
    if os.path.exists(folder_path):
        print(f"Cleaning up existing output folder: {folder_path}")
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)
    os.makedirs(os.path.join(folder_path, "filtered"))
    print("Created fresh output folder")

def run_all_versions(data_file, stop_words_file):
    # Define the output folder and clean it
    output_folder = "output"
    clean_output_folder(output_folder)

    # Single-threaded CPU algorithm
    print("\nRunning single-threaded CPU algorithm")
    single_processor = SingleCPUProcessor(data_file, stop_words_file, output_folder)
    single_stats, single_time = single_processor.process()
    print(f"Single-threaded CPU processing time: {single_time:.4f} seconds")
    print("Statistics:")
    print(f"- Total words after filtration: {single_stats['total_words']}")
    print(f"- Most frequent word: '{single_stats['most_frequent']}' ({single_stats['most_frequent_count']} occurrences)")
    print(f"- Least frequent word: '{single_stats['least_frequent']}' ({single_stats['least_frequent_count']} occurrences)")

    # Multi-threaded CPU algorithm
    print("\nRunning multi-threaded CPU algorithm")
    multi_processor = MultiCPUProcessor(data_file, stop_words_file)
    multi_stats, multi_time = multi_processor.process()
    print(f"Multi-threaded CPU processing time: {multi_time:.4f} seconds")
    print("Statistics:")
    print(f"- Total words after filtration: {multi_stats['total_words']}")
    print(f"- Most frequent word: '{multi_stats['most_frequent']}' ({multi_stats['most_frequent_count']} occurrences)")
    print(f"- Least frequent word: '{multi_stats['least_frequent']}' ({multi_stats['least_frequent_count']} occurrences)")

    # Spark algorithm
    print("\nRunning Spark algorithm")
    spark_processor = Spark(data_file, stop_words_file) 
    spark_stats, spark_time = spark_processor.process()
    print(f"Spark processing time: {spark_time:.4f} seconds")

    print("Statistics:")
    print(f"- Total words after filtration: {spark_stats['total_words']}")
    print(f"- Most frequent word: '{spark_stats['most_frequent']}' ({spark_stats['most_frequent_count']} occurrences)")
    print(f"- Least frequent word: '{spark_stats['least_frequent']}' ({spark_stats['least_frequent_count']} occurrences)")

    # Collect results for visualization
    times = {
        "Single-threaded CPU": single_time,
        "Multi-threaded CPU": multi_time,
        "Spark": spark_time
    }

    # Create visualizations
    visualize_times(times)
    visualize_bar_chart(times)

def main():
    # Define file paths
    data_file = "data/data.txt"
    stop_words_file = "data/stop_words.txt"

    # Check if files exist
    if not os.path.exists(data_file):
        print(f"Error: Data file '{data_file}' does not exist.")
        return
    if not os.path.exists(stop_words_file):
        print(f"Error: Stop words file '{stop_words_file}' does not exist.")
        return

    # Run all processing versions
    run_all_versions(data_file, stop_words_file)

if __name__ == "__main__":
    main()