from csv import reader
from essay_data import EssayData, Words
from essay_stats import EssayStats, EssayBatchStats, BatchManager
from time import time
from inference import compare_batches
import json

PATH = "../essay_data.csv"
BATCH_SIZE = 1000

PUNCTUATION = [
    "\"", "'", ",", ".", "!", "?", "/", "-", ":", ";", "(", ")", "[", "]", "{", "}", "<", ">", "@", "#", "$", "%", "^", "&", "*",
    "_", "+", "=", "~", "`", "|", "\\", "«", "»", "“", "”", "‘", "’", "•", "…"
]

def read_essays(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        csv_reader = reader(file)
        next(csv_reader)
        ai_start = 0
        ai_end = 0
        human_start = 0
        human_end = 0
        essay_count = 0
        ai_dump: list[EssayStats] = []
        ai_batches = BatchManager(True)
        human_dump: list[EssayStats] = []
        human_batches = BatchManager(False)
        for row in csv_reader:
            try:
                ai_author = row[1] == "1.0"
                parsed_essay = parse_essay(row[0], ai_author)
                essay_stats = EssayStats(parsed_essay)
                essay_count += 1
                if ai_author:
                    ai_end += 1
                    ai_dump.append(essay_stats)
                    ai_batches.add_essay(essay_stats)
                else:
                    human_end += 1
                    human_dump.append(essay_stats)
                    human_batches.add_essay(essay_stats)
            except Exception as e:
                print(f"Error parsing row {essay_count}: {e.with_traceback(None)}")
                essay_count += 1
                continue
            
            if len(ai_dump) >= BATCH_SIZE:
                dump_data = [{"ai_author": ai_author, "essay": current.to_json()} for current in ai_dump]
                with open(f"data/ai/essay_{ai_start}_{ai_end}.json", "w", encoding="utf-8") as essay_dump_file:
                    json.dump(dump_data, essay_dump_file, ensure_ascii=False, indent=2)
                ai_start = ai_end + 1
                ai_dump = []
            if len(human_dump) >= BATCH_SIZE:
                dump_data = [{"ai_author": ai_author, "essay": current.to_json()} for current in human_dump]
                with open(f"data/human/essay_{human_start}_{human_end}.json", "w", encoding="utf-8") as essay_dump_file:
                    json.dump(dump_data, essay_dump_file, ensure_ascii=False, indent=2)
                human_start = human_end + 1
                human_dump = []
        ai_batches.write_files()
        human_batches.write_files()
        compare_batches(ai_batches, human_batches)
        print(f"Processed {essay_count} essays")
                


def parse_essay(essay: str, ai_author: bool) -> EssayData:
    sentences = essay.split(".")
    essay_data = EssayData(ai_author)
    skipped = 0
    for sentence in sentences:
        essay_sentence = Words()
        words = sentence.split()
        for word in words:
            word = word.lower()
            if word in PUNCTUATION:
                essay_sentence.add_punctuation(word)
            elif word.isalpha():
                # Word is a word
                essay_sentence.add_word(word)
            elif word.isnumeric():
                # Word is a number
                essay_sentence.add_word(word)
            else:
                # Unidentified case
                for punc in PUNCTUATION:
                    if punc in word:
                        essay_sentence.add_punctuation(punc)
                        word = word.replace(punc, "")
                essay_sentence.add_word(word)
        if essay_sentence.word_count > 0:
            essay_sentence.add_punctuation(".")
            if skipped > 0:
                for _ in range(skipped):
                    essay_sentence.add_punctuation(".")
            essay_data.sentences.append(essay_sentence)
            skipped = 0
        else:
            skipped += 1
    return essay_data

start_time = time()
read_essays(PATH)
end_time = time()
print(f"Execution time: {end_time - start_time} seconds")
