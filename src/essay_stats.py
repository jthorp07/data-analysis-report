from essay_data import EssayData
from word_frequency import WordFrequencyDataManager
from statistics import fmean
from math import floor
from random import randint
import json

WORD_FREQ_MGR = WordFrequencyDataManager()

class IntegerStat:
    def __init__(self, name:str):
        self.name = name
        self.num_counts: int = 0
        self.counts: list[int] = []
        self.cumulative: int = 0
        self.min: int = -1
        self.max: int = -1
    
    def add_value(self, val: int):
        self.num_counts += 1
        self.counts.append(val)
        self.cumulative += val
        if val > self.max:
            self.max = val
        if val < self.min or self.min == -1.0:
            self.min = val

    def get_median(self):
        return self.counts[floor(float(self.num_counts) / 2.0)]
    
    def get_average(self):
        return float(self.cumulative) / float(self.num_counts)
    
    def get_std_dev(self):
        avg = self.get_average()
        sum_sq = 0.0
        for val in self.counts:
            sum_sq += (float(val) - avg) ** 2
        return (sum_sq / float(self.num_counts - 1)) ** 0.5
    
    def __str__(self):
        return f"{self.name}\n avg: {self.get_average()}\n median: {self.get_median()}\n min: {self.min}\n max: {self.max}"
        
    def to_json(self):
        return {
            f"{self.name}": {
                "avg": self.get_average(),
                "median": self.get_median(),
                "std_dev": self.get_std_dev(),
                "min": self.min,
                "max": self.max
            }
        }


class FloatStat:
    def __init__(self, name:str):
        self.name = name
        self.num_counts: int = 0
        self.counts: list[float] = []
        self.cumulative: float = 0
        self.min: float = -1
        self.max: float = -1
    
    def add_value(self, val: float):
        self.num_counts += 1
        self.counts.append(val)
        self.cumulative += val
        if val > self.max:
            self.max = val
        if val < self.min or self.min == -1.0:
            self.min = val

    def get_median(self):
        return self.counts[floor(float(self.num_counts) / 2.0)]
    
    def get_average(self):
        return float(self.cumulative) / float(self.num_counts)
    
    def get_std_dev(self):
        avg = self.get_average()
        sum_sq = 0.0
        for val in self.counts:
            sum_sq += (val - avg) ** 2
        return (sum_sq / float(self.num_counts - 1)) ** 0.5
    
    def __str__(self):
        return f"{self.name}\n avg: {self.get_average()}\n median: {self.get_median()}\n min: {self.min}\n max: {self.max}"
        
    def to_json(self):
        return {
            f"{self.name}": {
                "avg": self.get_average(),
                "median": self.get_median(),
                "std_dev": self.get_std_dev(),
                "min": self.min,
                "max": self.max
            }
        }


class EssayStats:
    def __init__(self, essay: EssayData):
        self.essay = essay
        self.word_count = sum([sentence.word_count for sentence in essay.sentences])
        self.average_sentence_length = self.word_count / len(self.essay.sentences)
        
    def count_unique_words(self) -> int:
        """
        Count the number of unique words in the essay.
        """
        unique_words = set()
        for sentence in self.essay.sentences:
            for word in sentence.words.keys():
                unique_words.add(word)
        return len(unique_words)
    
    def count_punctuation(self) -> int:
        """
        Count the number of punctuation marks in the essay.
        """
        punctuation_count = 0
        for sentence in self.essay.sentences:
            for punctuation in sentence.punctuation.keys():
                punctuation_count += sentence.punctuation[punctuation]
        return punctuation_count
    
    def word_rarity_score(self) -> float:
        score = 0.0
        for sentence in self.essay.sentences:
            for word, count in sentence.words.items():
                score += (WORD_FREQ_MGR.word_score(word) * float(count))
        return score / float(self.word_count)
    
    def punctuation_per_word_ratio(self, punctuation_count: int|None = None):
        """
        Calculate the ratio of punctuation to words in the essay.
        """
        if punctuation_count is None:
            punctuation_count = self.count_punctuation()
        return float(punctuation_count) / float(self.word_count)
    

    def lexical_diversity(self, unique_word_count: int|None = None):
        """
        Calculate the lexical diversity of the essay as the ratio of unique words to total words.
        """
        if unique_word_count is None:
            unique_word_count = self.count_unique_words()
        return float(unique_word_count) / float(self.word_count)
        
    
    def to_json(self):
        punct_count = self.count_punctuation()
        unique_word_count = self.count_unique_words()
        jsonified = {
            "ai_author": self.essay.ai_author,
            "word_count": self.word_count,
            "unique_word_count": unique_word_count,
            "punctuation_count": punct_count,
            "word_rarity_score": self.word_rarity_score(),
            "punctuation_per_word_ratio": self.punctuation_per_word_ratio(punct_count),
            "lexical_diversity": self.lexical_diversity(unique_word_count),
            "average_sentence_length": self.average_sentence_length,
            "sentence_data": [sentence.to_json() for sentence in self.essay.sentences]
        }
        return jsonified



class EssayBatchStats:
    def __init__(self, ai_author: bool):

        self.ai_author = ai_author
        self.essay_count = 0
        self.word_counts = IntegerStat("word_counts")
        self.unique_word_counts = IntegerStat("unique_word_counts")
        self.punc_counts = IntegerStat("punctuation_counts")
        self.rarity_scores = FloatStat("rarity_scores")
        self.sentence_lengths = FloatStat("average_sentence_lengths")
        self.ppw_ratios = FloatStat("punctuation_per_word_ratios")
        self.lexical_diversities = FloatStat("lexical_diversities")

    def add_essay(self, essay: EssayStats):
        self.essay_count += 1
        self.word_counts.add_value(essay.word_count)
        self.unique_word_counts.add_value(essay.count_unique_words())
        self.punc_counts.add_value(essay.count_punctuation())
        self.rarity_scores.add_value(essay.word_rarity_score())
        self.sentence_lengths.add_value(essay.average_sentence_length)
        self.ppw_ratios.add_value(essay.punctuation_per_word_ratio())
        self.lexical_diversities.add_value(essay.lexical_diversity())


    def get_random_sample(self, sample_size: int):
        if sample_size > self.essay_count * 5:
            return self
        else:
            sample_indices: list[int] = []
            sample_batch = EssayBatchStats(self.ai_author)
            while len(sample_indices) < sample_size:
                index = randint(0, self.essay_count - 1)
                if index in sample_indices:
                    continue
                sample_indices.append(index)
            for index in sample_indices:
                sample_batch.word_counts.add_value(self.word_counts.counts[index])
                sample_batch.unique_word_counts.add_value(self.unique_word_counts.counts[index])
                sample_batch.punc_counts.add_value(self.punc_counts.counts[index])
                sample_batch.rarity_scores.add_value(self.rarity_scores.counts[index])
                sample_batch.sentence_lengths.add_value(self.sentence_lengths.counts[index])
                sample_batch.ppw_ratios.add_value(self.ppw_ratios.counts[index])
                sample_batch.lexical_diversities.add_value(self.lexical_diversities.counts[index])
        return sample_batch

    def __str__(self):
        return f"Essays: {self.essay_count}\n{self.word_counts}\n{self.unique_word_counts}\n{self.punc_counts}\n{self.rarity_scores}\n{self.sentence_lengths}"
    
    def to_json(self):
        
        return {
            "essay_count": self.essay_count,
            **self.word_counts.to_json(),
            **self.unique_word_counts.to_json(),
            **self.punc_counts.to_json(),
            **self.rarity_scores.to_json(),
            **self.sentence_lengths.to_json(),
            **self.ppw_ratios.to_json(),
            **self.lexical_diversities.to_json()
        }


class BatchManager:
    def __init__(self, ai_author: bool):
        self.ai_author = ai_author
        self.batches: dict[str, EssayBatchStats] = {
            "0-50": EssayBatchStats(ai_author),
            "51-100": EssayBatchStats(ai_author),
            "101-200": EssayBatchStats(ai_author),
            "201-500": EssayBatchStats(ai_author),
            "501-1000": EssayBatchStats(ai_author),
            "1001-plus": EssayBatchStats(ai_author)
        }

    def add_essay(self, essay: EssayStats):
        if essay.word_count <= 50:
            self.batches["0-50"].add_essay(essay)
        elif essay.word_count <= 100:
            self.batches["51-100"].add_essay(essay)
        elif essay.word_count <= 200:
            self.batches["101-200"].add_essay(essay)
        elif essay.word_count <= 500:
            self.batches["201-500"].add_essay(essay)
        elif essay.word_count <= 1000:
            self.batches["501-1000"].add_essay(essay)
        else:
            self.batches["1001-plus"].add_essay(essay)

    def write_files(self):
        author = "ai" if self.ai_author else "human"
        for key, batch in self.batches.items():
            path = f"data/batches/{author}_{key}.json"
            with open(path, "w", encoding="utf-8") as batch_file:
                json.dump(batch.to_json(), batch_file, ensure_ascii=False, indent=2)
    
    def get_batches(self) -> list[tuple[str, EssayBatchStats]]:
        return [
            ("0-50", self.batches["0-50"]),
            ("51-100", self.batches["51-100"]),
            ("101-200", self.batches["101-200"]),
            ("201-500", self.batches["201-500"]),
            ("501-1000", self.batches["501-1000"]),
            ("1001-plus", self.batches["1001-plus"]),
        ]
        
