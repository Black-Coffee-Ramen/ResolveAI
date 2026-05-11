import pandas as pd
from scraper import build_corpus
from retriever import SupportRetriever
from agent import triage_ticket
from utils import precheck


def main():
    print("Building corpus...")
    corpus = build_corpus()
    print(f"Corpus size: {len(corpus)} documents")

    print("Building retriever...")
    retriever = SupportRetriever(corpus)

    # Load CSV
    df = pd.read_csv("support_tickets.csv")
    results = []

    for i, (_, row) in enumerate(df.iterrows()):
        print(f"\nProcessing ticket {i+1}/{len(df)}...")

        issue = str(row.get("issue", "") or row.get("Issue", "")).strip()
        subject = str(row.get("subject", "") or row.get("Subject", "")).strip()
        company = str(row.get("company", "") or row.get("Company", "")).strip()

        # Handle "None" string
        if company.lower() in ("none", "nan", ""):
            company = ""

        print(f"  Company: {company}")
        print(f"  Subject: {subject[:60]}")
        print(f"  Issue:   {issue[:80]}")

        # Build retrieval query
        query = f"{company} {subject} {issue}"

        # Retrieve relevant docs
        docs = retriever.retrieve(query, company=company if company else None, top_k=5)
        print(f"  Docs retrieved: {len(docs)}")
        context = retriever.format_context(docs)

        # Safety precheck first — context param removed
        pre = precheck(issue)
        if pre:
            result = pre
            print(f"  → Precheck triggered: {result['product_area']}")
        else:
            result = triage_ticket(issue, subject, company, context)
            print(f"  → Status: {result.get('status')} | Area: {result.get('product_area')}")

        results.append({
            "issue": issue,
            "subject": subject,
            "company": company,
            "status": result.get("status", "escalated"),
            "product_area": result.get("product_area", "general"),
            "request_type": result.get("request_type", "product_issue"),
            "response": result.get("response", ""),
            "justification": result.get("justification", ""),
        })

    output_df = pd.DataFrame(results)
    output_df.to_csv("output.csv", index=False)
    print(f"\n✅ Done → output.csv ({len(results)} rows)")


if __name__ == "__main__":
    main()
