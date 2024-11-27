file_path = 'data.txt'
def load_stop_words(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return set(word.strip().lower() for word in file)
    except FileNotFoundError:
        print(f"Warning: {filename} not found. Proceeding without stop words.")
        return set()

def process_text(filename, stop_words):
    try:
        freq = {}
        with open(filename, 'r', encoding='utf-8') as file:
            counter = 0
            for line in file:
                # Split line into words and process each word
                words = line.strip().split()
                for word in words:
                    # Clean the word: remove punctuation and convert to lowercase
                    word = word.strip('.,!?()[]{}":;').lower()

                    # filtering words grater than 8 and smaller than 4
                    if len(word)>8:
                        word=""
                    if  len(word)<4:
                        word=""

                    # Skip empty strings and stop words
                    if word and word not in stop_words:
                        print(f"Processing word: {word}")
                        freq[word] = freq.get(word, 0) + 1
                        
        # Find most and least frequent words
        most_frequent = max(freq.items(), key=lambda x: x[1])
        least_frequent = min(freq.items(), key=lambda x: x[1])
        # Printing most and least frequent word
        print(f"Most frequent word: '{most_frequent[0]}', totally {most_frequent[1]} times")
        print(f"Least frequent word: '{least_frequent[0]}' totally {least_frequent[1]} times")

    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 
def main():
    # Load stop words
    stop_words = load_stop_words('stop_words.txt')
    
    # Process the main text file
    process_text(file_path, stop_words)

if __name__ == "__main__":
    main()