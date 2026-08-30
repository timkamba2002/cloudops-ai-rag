import boto3

REGION = "us-east-1"
KNOWLEDGE_BASE_ID = "UCTIVBUB1H"
MODEL_ID = "amazon.nova-lite-v1:0"

# Client used for Knowledge Base retrieval
kb_client = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION
)

# Client used for LLM generation
bedrock_client = boto3.client(
    "bedrock-runtime",
    region_name=REGION
)

question = input("Ask CloudOps AI: ")

# -----------------------------
# 1. RETRIEVAL
# -----------------------------

response = kb_client.retrieve(
    knowledgeBaseId=KNOWLEDGE_BASE_ID,
    retrievalQuery={
        "text": question
    },
    retrievalConfiguration={
        "managedSearchConfiguration": {
            "numberOfResults": 3
        }
    }
)

retrieval_results = response["retrievalResults"]

import json

print("\nDEBUG - First retrieval result:")
print(json.dumps(retrieval_results[0], indent=2, default=str))

# Combine the retrieved chunks into one context block
context_parts = []
sources = []

for index, result in enumerate(retrieval_results, start=1):
    text = result["content"]["text"]

    metadata = result.get("metadata", {})
    title = metadata.get("_document_title", "Unknown source")
    score = result.get("score", 0)

    context_parts.append(
        f"[Source {index}: {title}]\n{text}"
    )

    sources.append({
        "number": index,
        "title": title,
        "score": score
    })

context = "\n\n".join(context_parts)

# -----------------------------
# 2. AUGMENTATION
# -----------------------------

prompt = f"""
Use only the provided CloudOps documentation to answer the question.

If the documentation does not contain enough information to answer,
say that you do not have enough information in the knowledge base.

Cite relevant sources using their source number and document title.

Question:
{question}

CloudOps Documentation:
{context}
"""

# -----------------------------
# 3. GENERATION
# -----------------------------

llm_response = bedrock_client.converse(
    modelId=MODEL_ID,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "text": prompt
                }
            ]
        }
    ],
    inferenceConfig={
        "maxTokens": 700,
        "temperature": 0.1
    }
)

answer = llm_response["output"]["message"]["content"][0]["text"]

print("\nCloudOps AI:\n")
print(answer)

print("\nSources:")

for source in sources:
    print(
        f"{source['number']}. "
        f"{source['title']} "
        f"(relevance score: {source['score']:.3f})"
    )