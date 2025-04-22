from csv import writer, reader

RAW_PATH = "../word_frequency.txt"
DATA_PATH = "data/word_frequency.csv"

word_rarity_cache: dict[str,float] = {}
MAX_CACHE_SIZE = 10000
WORD_RARITY_DIGIT_MULTIPLIERS: dict[str, float] ={
    "11": 1.0,
    "10": 1.0,
    "9": 1.0,
    "8": 1.5,
    "7": 2.0,
    "6": 3.0,
    "5": 4.0,
}

def prepare_frequency_data():
    raw_lines: list[str] = []
    with open(RAW_PATH, "r", encoding="utf-8") as file:
        raw_lines = file.readlines()

    cleaned_lines: list[tuple[str, str, str]] = [("Word", "Rank", "Digits")]
    num_lines = len(raw_lines)
    for i in range(num_lines):
        word, frequency = raw_lines[i].strip().split()
        cleaned_lines.append((word, str(i + 1), str(len(frequency))))

    with open(DATA_PATH, "w" , encoding="utf-8", newline="") as file:
        csv_writer = writer(file)
        csv_writer.writerows(cleaned_lines)




def word_rarity_score(word:str):
    if word in word_rarity_cache:
        return word_rarity_cache[word]
    highest_rank = 0
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        csv_reader = reader(file)
        next(csv_reader)
        for row in csv_reader:
            highest_rank = int(row[1])
            if row[0] == word:
                if len(word_rarity_cache) > MAX_CACHE_SIZE:
                    evict_cache()
                word_rarity_cache[word] = float(row[1]) * WORD_RARITY_DIGIT_MULTIPLIERS.get(row[2], 1.0)
                return word_rarity_cache[word]
    return highest_rank * 5.0


def evict_cache():
    highest_score = 0.0
    highest_word = ""

    for word, score in word_rarity_cache.items():
        if score > highest_score:
            highest_score = score
            highest_word = word
    
    word_rarity_cache.pop(highest_word)


def load_word_frequency_data():
    print("Loading word frequency data")
    data: dict[str,float] = {}
    data.setdefault(-1.0)
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        csv_reader = reader(file)
        next(csv_reader)
        for row in csv_reader:
            data[row[0]] = float(row[1]) * WORD_RARITY_DIGIT_MULTIPLIERS.get(row[2])
    print("Word frequency data loaded")
    return data

class WordFrequencyDataManager:
    def __init__(self):
        self.data: dict[str,float] = load_word_frequency_data()
        self.count = float(len(self.data.keys()))
    def word_score(self, word:str):
        res = self.data.get(word, -5.0)
        if res < 0:
            return self.count * 5.0
        else:
            return res