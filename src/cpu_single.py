import os
import time
from .base_processor import BaseProcessor  # Fixed import

class SingleCPUProcessor(BaseProcessor):
    def __init__(self, data_path, stop_words_path, output_folder):
        super().__init__(data_path, stop_words_path)
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def process(self):
        start_time = time.time()
        try:
            words = self.load_file(self.data_path)
            stop_words = set(self.load_file(self.stop_words_path))
            filtered_words = self.filter_words(words, stop_words)
            
            filtered_folder = os.path.join(self.output_folder, "filtered")
            os.makedirs(filtered_folder, exist_ok=True)
            
            output_file_path = os.path.join(filtered_folder, "filtered_single_words.txt")
            with open(output_file_path, "w", encoding='utf-8') as f:
                f.write("\n".join(filtered_words))
            
            stats = self.compute_statistics(filtered_words)
            execution_time = time.time() - start_time
            return stats, execution_time
            
        except Exception as e:
            print(f"Error in single CPU processing: {str(e)}")
            return None, 0