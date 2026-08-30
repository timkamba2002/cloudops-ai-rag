import boto3

REGION = "us-east-1"
KNOWLEDGE_BASE_ID = "UCTIVBUB1H"

kb_client = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION
)

TEST_CASES = [
    {
        "question": "My Kubernetes container keeps restarting. What should I check?",
        "expected_source": "crashloopbackoff.md"
    },
    {
        "question": "My pod is stuck in Pending. What should I investigate?",
        "expected_source": "pod-pending.md"
    },
    {
        "question": "My EC2 instance has high CPU. What should I check?",
        "expected_source": "ec2-high-cpu.md"
    },
    {
        "question": "My ALB is returning 5xx errors. How should I troubleshoot it?",
        "expected_source": "alb-5xx-errors.md"
    },
    {
        "question": "What is the SEV1 incident response procedure?",
        "expected_source": "sev1-response.md"
    },
    {
        "question": "A container keeps starting and dying repeatedly. How do I troubleshoot it?",
        "expected_source": "crashloopbackoff.md"
    },
    {
        "question": "How do I reset the password on a Cisco router?",
        "expected_source": None
    },
    {
        "question": "How do I configure a PostgreSQL replication cluster?",
        "expected_source": None
    }
]


def retrieve(question):
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

    return response["retrievalResults"]


MIN_RELEVANCE_SCORE = 0.40

in_domain_total = 0
in_domain_passed = 0

out_of_domain_total = 0
out_of_domain_rejected = 0


print("\nCloudOps AI Retrieval Evaluation")
print("=" * 60)

for number, test in enumerate(TEST_CASES, start=1):

    results = retrieve(test["question"])

    top_result = results[0]

    metadata = top_result.get("metadata", {})
    retrieved_source = metadata.get("_document_title", "Unknown")
    score = top_result.get("score", 0)

    expected_source = test["expected_source"]

    # Out-of-domain test
    if expected_source is None:
        out_of_domain_total += 1

        if score < MIN_RELEVANCE_SCORE:
            out_of_domain_rejected += 1
            status = "PASS"
        else:
            status = "FAIL"

    # In-domain test
    else:
        in_domain_total += 1

        if retrieved_source == expected_source:
            in_domain_passed += 1
            status = "PASS"
        else:
            status = "FAIL"

    print(f"\nTest {number}: {status}")
    print(f"Question: {test['question']}")
    print(f"Expected: {expected_source}")
    print(f"Retrieved: {retrieved_source}")
    print(f"Top score: {score:.3f}")


print("\n" + "=" * 60)

print(
    f"In-domain retrieval accuracy: "
    f"{in_domain_passed}/{in_domain_total}"
)

print(
    f"Out-of-domain rejection: "
    f"{out_of_domain_rejected}/{out_of_domain_total}"
)