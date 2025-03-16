import re
import nltk
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords

nltk.download("stopwords")

def analyze_text(language):
    try:
        with open("words.txt", "r", encoding="utf-8") as f:
            text = f.read().strip()

        if not text:
            print("Файл порожній!")
            return

        try:
            stop_words = set(stopwords.words(language))
        except OSError:
            print(f"Мова '{language}' не підтримується! Використовуємо тільки фільтрацію пунктуації.")
            stop_words = set()

        words = re.sub(r'[^\w\s]', '', text.lower()).split()

        filtered_words = [word for word in words if word not in stop_words]

        word_counts = Counter(filtered_words)

        top_5 = word_counts.most_common(5)
        print(f"Топ-5 найпоширеніших слів: {top_5}")

        total_length = sum(len(word) for word in filtered_words)
        average = total_length / len(filtered_words) if filtered_words else 0
        print(f"Середня довжина слова: {average}")

        top_words = word_counts.most_common(10)
        words, counts = zip(*top_words) if top_words else ([], [])

        plt.figure(figsize=(10, 5))
        plt.bar(words, counts, color='skyblue')
        plt.xlabel("Слова")
        plt.ylabel("Кількість входжень")
        plt.title(f"Топ-10 найчастіших слів ({language})")
        plt.xticks(rotation=45)
        plt.show()

    except FileNotFoundError:
        print("Файл 'words.txt' не знайдено!")

language = input("Enter the language: ").strip().lower()

analyze_text(language)
