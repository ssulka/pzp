import threading
import os
import math
import time
from queue import Queue
from .base_processor import BaseProcessor

class MultiCPUProcessor(BaseProcessor):
    def __init__(self, data_path, stop_words_path):
        super().__init__(data_path, stop_words_path)
        self.num_threads = os.cpu_count()
        self.result_queue = Queue()
        # Create output folder
        self.output_folder = "output"
        os.makedirs(os.path.join(self.output_folder, "filtered"), exist_ok=True)

    def process_chunk(self, chunk, stop_words):
        filtered_words = self.filter_words(chunk, stop_words)
        self.result_queue.put(filtered_words)

    def process(self):
        start_total = time.time()
        
        # Load data
        words = self.load_file(self.data_path)
        stop_words = set(self.load_file(self.stop_words_path))
        
        # Parallel processing
        start_process = time.time()
        chunk_size = max(1000, math.ceil(len(words) / self.num_threads))
        chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
        
        # Create and start threads
        threads = []
        for chunk in chunks:
            thread = threading.Thread(
                target=self.process_chunk,
                args=(chunk, stop_words)
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
            
        process_time = time.time() - start_process
        print(f"Process time: {process_time:.4f} seconds")
        
        # Aggregate results or it gives together chunks
        start_aggregate = time.time()
        filtered_words = []
        while not self.result_queue.empty():
            # Will take filtered words from queue and pass it to filtered words
            chunk_results = self.result_queue.get()
            filtered_words.extend(chunk_results)

        # Save filtered words to file
        output_file_path = os.path.join(self.output_folder, "filtered", "multithread_filtered_words.txt")
        with open(output_file_path, "w", encoding='utf-8') as f:
            f.write("\n".join(filtered_words))
        print(f"Filtered words have been saved to: {output_file_path}")
            
        stats = self.compute_statistics(filtered_words)
        total_time = time.time() - start_total
        
        return stats, total_time