import os

def build_corpus():
    corpus = []
    kb_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "knowledge_base")
    
    if not os.path.exists(kb_path):
        return corpus

    for filename in os.listdir(kb_path):
        if filename.endswith(".md"):
            with open(os.path.join(kb_path, filename), "r", encoding="utf-8") as f:
                content = f.read()
                corpus.append({
                    "source": filename.replace(".md", ""),
                    "topic": filename.replace(".md", "").replace("_", " ").title(),
                    "content": content
                })
    return corpus
