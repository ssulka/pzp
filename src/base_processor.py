from collections import Counter

class BaseProcessor:
    def __init__(self, data_path, stop_words_path):
        self.data_path = data_path
        self.stop_words_path = stop_words_path

    def load_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return [word.strip().lower() for word in f.read().split()]

    def filter_by_length(self, words):
        return [word for word in words if 4 <= len(word) <= 8]
    # filtering words with legth
    def filter_words(self, words, stop_words):
        # First filter by length
        length_filtered = self.filter_by_length(words)
        # Then filter stop words
        return [word for word in length_filtered if word and word not in stop_words]

    def compute_statistics(self, filtered_words):
        if not filtered_words:
            return {
                "total_words": 0,
                "most_frequent": None,
                "most_frequent_count": 0,
                "least_frequent": None,
                "least_frequent_count": 0
            }
        
        # Count word frequencies
        word_counts = Counter(filtered_words)
        
        # Find most and least frequent words
        # return the first word with most vyskytom
        most_common = word_counts.most_common(1)[0]
        # return the first word with least vyskytom
        least_common = word_counts.most_common()[-1]

        return {
            "total_words": len(filtered_words),
            "most_frequent": most_common[0],
            "most_frequent_count": most_common[1],
            "least_frequent": least_common[0],
            "least_frequent_count": least_common[1]
        }