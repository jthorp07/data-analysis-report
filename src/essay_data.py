
class Words:
    def __init__(self):
        self.word_count = 0
        self.unique_word_count = 0
        self.words: dict[str,int] = {}
        self.punctuation: dict[str,int] = {}
    
    def add_word(self, word:str):
        if self.words.get(word) == None:
            self.words[word] = 1
            self.unique_word_count += 1
        else:
            self.words[word] = self.words[word] + 1
        self.word_count += 1
    
    def add_punctuation(self, punctuation:str):
        if self.punctuation.get(punctuation) == None:
            self.punctuation[punctuation] = 1
        self.punctuation[punctuation] = self.punctuation[punctuation] + 1

    def __str__(self):
        return f"Words( word count: {self.word_count}, unique_word_count: {self.unique_word_count}, data: {self.words}, punctuation: {self.punctuation} )"
    
    def to_json(self):
        return {
            "word_count": self.word_count,
            "unique_word_count": self.unique_word_count,
            "words": self.words,
            "punctuation": self.punctuation
        }

class EssayData:
    def __init__(self, ai_author: bool):
        self.ai_author: bool = ai_author
        self.sentences: list[Words] = []

    def __str__(self):
        return f"EssayData( word count: {self.words.word_count}, unique_word_count: {self.words.unique_word_count}, sentence_count: {len(self.sentences)}, sentences: {self.sentences}, words: {self.words} )"

    def to_json(self):
        return {
            "ai_author": self.ai_author,
            "sentence_data": [sentence.to_json() for sentence in self.sentences]
        }



