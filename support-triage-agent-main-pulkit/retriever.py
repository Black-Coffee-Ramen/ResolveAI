from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SupportRetriever:
    def __init__(self, corpus):
        self.corpus = corpus
        self.texts = [d["content"] for d in corpus]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.texts)

    def retrieve(self, query, company=None, top_k=5):
        query_lower = query.lower()
        query_words = set(query_lower.split())

        # TF-IDF cosine scores
        q_vec = self.vectorizer.transform([query_lower])
        cosine_scores = cosine_similarity(q_vec, self.matrix).flatten()

        scored = []
        for i, doc in enumerate(self.corpus):
            score = cosine_scores[i] * 2.0

            # Strong boost: company/source match
            if company and doc["source"].lower() == company.lower():
                score += 3.0

            # Keyword overlap bonus
            doc_text = doc["content"].lower()
            overlap = sum(1 for w in query_words if len(w) > 3 and w in doc_text)
            score += overlap * 0.4

            scored.append((score, i, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = [item[2] for item in scored if item[0] > 0]
        return results[:top_k] if results else self.corpus[:top_k]

    def format_context(self, docs):
        if not docs:
            return "No relevant documentation found."
        return "\n\n".join([
            f"[{d['source']} - {d.get('topic', '')}]\n{d['content']}"
            for d in docs
        ])