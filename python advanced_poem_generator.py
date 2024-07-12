import random
import re
from collections import defaultdict
import nltk
from textblob import TextBlob
import pyphen
import pronouncing
import string

# Download NLTK data (if not already downloaded)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

class EnhancedWordBank:
    def __init__(self):
        self.words = defaultdict(list)
        self.load_words()
        self.themes = {
            'nature': ['forest', 'river', 'mountain', 'sky', 'ocean', 'star', 'flower', 'tree', 'wind', 'rain'],
            'emotion': ['love', 'fear', 'joy', 'sorrow', 'anger', 'hope', 'desire', 'peace', 'anxiety', 'bliss'],
            'time': ['moment', 'eternity', 'past', 'future', 'dawn', 'dusk', 'season', 'year', 'century', 'instant'],
            'abstract': ['dream', 'idea', 'thought', 'memory', 'soul', 'spirit', 'destiny', 'fate', 'truth', 'lies']
        }

    def load_words(self):
        # Expanded word lists with more diverse and evocative words
        self.words['nouns'] = ['whisper', 'shadow', 'light', 'darkness', 'heart', 'mind', 'soul', 'dream', 'nightmare', 'echo', 'silence', 'thunder', 'lightning', 'storm', 'calm', 'chaos', 'order', 'mystery', 'secret', 'revelation', 'abyss', 'celestial', 'ephemeral', 'eternity', 'infinity', 'labyrinth', 'nebula', 'paradox', 'quantum', 'zeitgeist']
        self.words['verbs'] = ['whispers', 'dances', 'flows', 'shines', 'grows', 'fades', 'rises', 'falls', 'embraces', 'echoes', 'shatters', 'mends', 'transforms', 'yearns', 'ignites', 'freezes', 'melts', 'cascades', 'erupts', 'dissolves', 'oscillates', 'transcends', 'metamorphoses', 'radiates', 'undulates', 'evaporates', 'crystallizes', 'implodes', 'resonates', 'spirals']
        self.words['adjectives'] = ['silent', 'luminous', 'dark', 'ethereal', 'cosmic', 'eternal', 'ephemeral', 'infinite', 'microscopic', 'iridescent', 'somber', 'ecstatic', 'serene', 'turbulent', 'gossamer', 'velvet', 'crystalline', 'molten', 'frozen', 'incandescent', 'enigmatic', 'surreal', 'kaleidoscopic', 'nebulous', 'quantum', 'prismatic', 'phantasmagorical', 'ineffable', 'chimerical', 'labyrinthine']
        self.words['adverbs'] = ['softly', 'violently', 'tenderly', 'feverishly', 'languidly', 'passionately', 'silently', 'thunderously', 'delicately', 'furiously', 'gently', 'savagely', 'sweetly', 'bitterly', 'luminously', 'darkly', 'swiftly', 'glacially', 'fiercely', 'serenely', 'ethereally', 'enigmatically', 'paradoxically', 'infinitely', 'quantum-ly', 'transcendentally', 'ephemerally', 'celestially', 'chaotically', 'harmoniously']

    def get_word(self, type, theme=None):
        if theme and theme in self.themes:
            themed_words = [word for word in self.words[type] if word in self.themes[theme] or any(theme_word in word for theme_word in self.themes[theme])]
            if themed_words:
                return random.choice(themed_words)
        return random.choice(self.words[type])

    def get_rhyme(self, word):
        rhymes = pronouncing.rhymes(word)
        return random.choice(rhymes) if rhymes else word

    def get_synonym(self, word):
        synonyms = set()
        for syn in nltk.corpus.wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
        return random.choice(list(synonyms)) if synonyms else word

class EnhancedPoemGenerator:
    def __init__(self):
        self.word_bank = EnhancedWordBank()
        self.pyphen_dic = pyphen.Pyphen(lang='en')

    def syllable_count(self, word):
        return len(self.pyphen_dic.inserted(word).split('-'))

    def generate_line(self, template, theme=None):
        def replace_placeholder(match):
            word_type = match.group(1)
            word = self.word_bank.get_word(word_type, theme)
            if random.random() < 0.2:  # 20% chance to use a synonym
                word = self.word_bank.get_synonym(word)
            return word
        
        line = re.sub(r'\{(\w+)\}', replace_placeholder, template)
        return line.capitalize()

    def generate_metaphor(self, theme=None):
        return f"{self.word_bank.get_word('nouns', theme)} is {self.word_bank.get_word('adjectives', theme)} {self.word_bank.get_word('nouns', theme)}"

    def generate_simile(self, theme=None):
        return f"{self.word_bank.get_word('nouns', theme)} is like {self.word_bank.get_word('adjectives', theme)} {self.word_bank.get_word('nouns', theme)}"

    def generate_poem(self, style='free_verse', theme=None):
        if style == 'sonnet':
            return self.generate_sonnet(theme)
        elif style == 'haiku':
            return self.generate_haiku(theme)
        elif style == 'abstract':
            return self.generate_abstract(theme)
        elif style == 'villanelle':
            return self.generate_villanelle(theme)
        else:
            return self.generate_free_verse(theme)

    def generate_sonnet(self, theme=None):
        lines = []
        rhyme_scheme = 'ABABCDCDEFEFGG'
        rhymes = {}
        
        templates = [
            "The {adjectives} {nouns} {verbs} {adverbs}",
            "{adverbs}, {nouns} {verbs} through {nouns}",
            "In {adjectives} {nouns}, {nouns} {verbs}",
            "With {adjectives} {nouns}, {adverbs} {verbs}",
            "From {nouns} to {nouns}, {nouns} {verbs}",
            "As {adjectives} as {nouns}, {nouns} {verbs}"
        ]
        
        for rhyme in rhyme_scheme:
            template = random.choice(templates)
            line = self.generate_line(template, theme)
            
            if rhyme not in rhymes:
                rhymes[rhyme] = self.word_bank.get_rhyme(line.split()[-1])
                lines.append(line)
            else:
                while not line.endswith(rhymes[rhyme]):
                    line = self.generate_line(template, theme)
                lines.append(line)
        
        return '\n'.join(lines)

    def generate_haiku(self, theme=None):
        lines = []
        syllable_structure = [5, 7, 5]

        for syllables in syllable_structure:
            line = ""
            while sum(self.syllable_count(word) for word in line.split()) != syllables:
                template = random.choice([
                    "The {adjectives} {nouns}",
                    "{verbs} {adverbs} through {nouns}",
                    "{nouns} {verbs} {adverbs}",
                    "{adjectives} {nouns} {verbs}",
                    "{nouns} of {adjectives} {nouns}"
                ])
                line = self.generate_line(template, theme)
            lines.append(line)

        return '\n'.join(lines)

    def generate_free_verse(self, theme=None):
        lines = []
        for _ in range(random.randint(6, 12)):
            choice = random.random()
            if choice < 0.2:
                lines.append(self.generate_metaphor(theme))
            elif choice < 0.4:
                lines.append(self.generate_simile(theme))
            else:
                template = random.choice([
                    "The {adjectives} {nouns} {verbs}",
                    "{adverbs}, {nouns} {verbs}",
                    "In {adjectives} {nouns}, {nouns} {verbs}",
                    "{nouns} of {nouns} {verbs} {adverbs}",
                    "{adjectives} {nouns} {verbs} like {nouns}",
                    "From {nouns} to {nouns}, {adjectives} {nouns}",
                    "{verbs} the {adjectives} {nouns} of {nouns}",
                    "With {adjectives} {nouns}, {nouns} {verbs} {adverbs}"
                ])
                lines.append(self.generate_line(template, theme))
        return '\n'.join(lines)

    def generate_abstract(self, theme=None):
        fragments = []
        for _ in range(7):
            choice = random.random()
            if choice < 0.3:
                fragments.append(f"{self.word_bank.get_word('adjectives', theme)} {self.word_bank.get_word('nouns', theme)}")
            elif choice < 0.6:
                fragments.append(f"{self.word_bank.get_word('nouns', theme)} {self.word_bank.get_word('verbs', theme)}")
            else:
                fragments.append(f"{self.word_bank.get_word('adverbs', theme)} {self.word_bank.get_word('verbs', theme)}")
        return ' '.join(fragments).capitalize()

    def generate_villanelle(self, theme=None):
        # A1 and A2 are repeated lines, B is the rhyme for the middle lines
        A1 = self.generate_line("The {adjectives} {nouns} {verbs} {adverbs}", theme)
        A2 = self.generate_line("{adverbs}, {nouns} {verbs} through {nouns}", theme)
        B_rhyme = self.word_bank.get_rhyme(A1.split()[-1])
        
        lines = [A1]
        for i in range(5):
            lines.append(self.generate_line(f"{{adjectives}} {{nouns}} {{verbs}} {B_rhyme}", theme))
            lines.append(A1 if i % 2 == 0 else A2)
        lines.extend([A1, A2])
        
        return '\n'.join(lines)

    def add_poetic_devices(self, poem):
        lines = poem.split('\n')
        enhanced_lines = []
        for line in lines:
            if random.random() < 0.2:  # 20% chance to add alliteration
                words = line.split()
                if len(words) > 2:
                    start_sound = words[0][0].lower()
                    words[1] = self.word_bank.get_word(self.get_word_type(words[1]))
                    while words[1][0].lower() != start_sound:
                        words[1] = self.word_bank.get_word(self.get_word_type(words[1]))
                    line = ' '.join(words)
            if random.random() < 0.1:  # 10% chance to add assonance
                vowels = 'aeiou'
                words = line.split()
                if len(words) > 2:
                    vowel_sound = random.choice(vowels)
                    for i in range(1, len(words)):
                        if vowel_sound not in words[i].lower():
                            words[i] = self.word_bank.get_word(self.get_word_type(words[i]))
                            while vowel_sound not in words[i].lower():
                                words[i] = self.word_bank.get_word(self.get_word_type(words[i]))
                    line = ' '.join(words)
            enhanced_lines.append(line)
        return '\n'.join(enhanced_lines)

    def get_word_type(self, word):
        pos = nltk.pos_tag([word])[0][1]
        if pos.startswith('N'):
            return 'nouns'
        elif pos.startswith('V'):
            return 'verbs'
        elif pos.startswith('J'):
            return 'adjectives'
        elif pos.startswith('R'):
            return 'adverbs'
        else:
            return random.choice(['nouns', 'verbs', 'adjectives', 'adverbs'])

# Generate poems
generator = EnhancedPoemGenerator()

print("Sonnet (Nature theme):")
print(generator.add_poetic_devices(generator.generate_poem('sonnet', 'nature')))
print("\nHaiku (Emotion theme):")
print(generator.add_poetic_devices(generator.generate_poem('haiku', 'emotion')))
print("\nFree Verse (Time theme):")
print(generator.add_poetic_devices(generator.generate_poem('free_verse', 'time')))
print("\nAbstract (Abstract theme):")
print(generator.add_poetic_devices(generator.generate_poem('abstract', 'abstract')))
print("\nVillanelle (Nature theme):")
print(generator.add_poetic_devices(generator.generate_poem('villanelle', 'nature')))