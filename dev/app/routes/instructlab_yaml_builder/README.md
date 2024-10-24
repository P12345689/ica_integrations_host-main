# InstructLab Generator

> Author: Mihai Criveti

Generate instructlab yaml

## Testing the integration locally


```bash
curl -sX POST "http://localhost:8080/system/instructlab/generate_yaml/invoke" \
     -H "Content-Type: application/json" \
     --header "Integrations-API-Key: dev-only-token" \
     -d '{
          "skill_type": "compositional",
          "question_1": "Give few rhyming words for *cool*.",
          "answer_1": "Here are a few rhyming words for \"cool\":\n\n1. Pool\n2. Fool\n3. Tool\n4. Rule\n5. Mule",
          "question_2": "give one rhyming word for *pan*",
          "answer_2": "Here is one rhyming word for *pan*:\n\n1. Man",
          "question_3": "Give three rhyming words for *meet*",
          "answer_3": "Here are three rhyming words for *meet*:\n\n1. Street\n2. Neat\n3. Beat"
        }' | jq
```

## Integration

```
{
    "skill_type": "{input.skill_type}",
    "question_1": "{input.question_1}",
    "answer_1": "{input.answer_1}",
    "question_2": "{input.question_2}",
    "answer_2": "{input.answer_2}",
    "question_3": "{input.question_3}",
    "answer_3": "{input.answer_3}"
}

```
