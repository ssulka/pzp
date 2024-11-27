def load_stop_words(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return set(word.strip().lower() for word in file)
    except FileNotFoundError:
        print(f"Warning: {filename} not found. Proceeding without stop words.")
        return set()

def process_text(filename, stop_words):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                # Split line into words and process each word
                words = line.strip().split()
                for word in words:
                    # Clean the word: remove punctuation and convert to lowercase
                    word = word.strip('.,!?()[]{}":;').lower()
                    
                    #filtering words grater than 8 and smaller than 4
                    if len(word)>8:
                        word=""
                    if  len(word)<4:
                        word=""

                    # Skip empty strings and stop words
                    if word and word not in stop_words:
                        print(f"Processing word: {word}")

                        
                        
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
    process_text('data.txt', stop_words)

if __name__ == "__main__":
    main()