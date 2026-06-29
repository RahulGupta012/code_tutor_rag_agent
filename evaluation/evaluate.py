import time

from app.retriever.retriever import retrieve
from evaluation.test_queries import TEST_QUERIES


print("=" * 80)
print("RAG Retrieval Evaluation")
print("=" * 80)

total_time = 0
total_score = 0
web_count = 0

THRESHOLD = 0.5


for idx, query in enumerate(TEST_QUERIES, start=1):

    start = time.perf_counter()

    retrieval = retrieve(query)

    elapsed = time.perf_counter() - start

    chunks = retrieval["chunks"]
    score = retrieval["best_score"]

    total_time += elapsed
    total_score += score

    if score < THRESHOLD:
        web_count += 1

    print("\n" + "=" * 80)

    print(f"{idx}. {query}")

    print(f"Dense Score : {score:.3f}")

    print(f"Retrieval Time : {elapsed:.3f} sec")

    print(
        "Web Search :",
        "YES" if score < THRESHOLD else "NO"
    )

    print("\nTop Retrieved Chunks:\n")

    for i, chunk in enumerate(chunks, start=1):

        title = chunk["content"].split("\n")[0]

        print(f"{i}. {title}")

print("\n")
print("=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"Queries Tested      : {len(TEST_QUERIES)}")
print(f"Average Dense Score : {total_score/len(TEST_QUERIES):.3f}")
print(f"Average Retrieval   : {total_time/len(TEST_QUERIES):.3f} sec")
print(f"Web Search Trigger  : {web_count}/{len(TEST_QUERIES)}")