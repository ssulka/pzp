from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType, BooleanType
from .base_processor import BaseProcessor
import time
import os

class Spark(BaseProcessor):
    def __init__(self, data_path, stop_words_path):
        super().__init__(data_path, stop_words_path)
        self.spark = SparkSession.builder \
            .appName("TextProcessing") \
            .master("local[*]") \
            .getOrCreate()
        # Create output folder
        self.output_folder = "output"
        os.makedirs(os.path.join(self.output_folder, "filtered"), exist_ok=True)
        # Print Spark configuration
        print("\nSpark Configuration:")
        print(f"Spark cores in use: {self.spark.sparkContext.defaultParallelism}")
        print(f"Spark master: {self.spark.conf.get('spark.master')}")

    def process(self):
        start_time = time.time()
        try:
            # Load data
            words = self.load_file(self.data_path)
            stop_words = set(self.load_file(self.stop_words_path))
            
            # Create Spark DataFrame
            words_df = self.spark.createDataFrame([(word,) for word in words], ["word"])
            stop_words_broadcast = self.spark.sparkContext.broadcast(stop_words)
            
            # Define UDF filters
            udf_len = udf(lambda word: 4 <= len(word) <= 8, BooleanType())
            stop_udf = udf(
                lambda word: word.lower() not in stop_words_broadcast.value, 
                BooleanType()
            )
            
            # Apply filters
            filtered_df = words_df \
                .filter(udf_len(col("word"))) \
                .filter(stop_udf(col("word")))
            
            # Get filtered words as list and collection all dataframe filtered words and pass to filtered words
            filtered_words = [row["word"] for row in filtered_df.collect()]
            
            # Save filtered words to file
            output_file_path = os.path.join(self.output_folder, "filtered", "spark_filtered_words.txt")
            with open(output_file_path, "w", encoding='utf-8') as f:
                f.write("\n".join(filtered_words))
            
            # Compute statistics
            stats = self.compute_statistics(filtered_words)
            execution_time = time.time() - start_time
            
            return stats, execution_time
            
        except Exception as e:
            print(f"Error in Spark processing: {str(e)}")
            return None, 0
            
        finally:
            self.spark.stop()