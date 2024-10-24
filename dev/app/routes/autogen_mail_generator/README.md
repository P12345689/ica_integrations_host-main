# autogen_mail_generator Integration

> Author: Dennis Weiss, Max Belitsky, Alexandre Carlhammar, Stan Furrer

This module provides an integration that can generate and send a newsletter email and its attached audio version based on input content to a specified recipient's address, using a multi-agent setup.

## API Endpoints

### POST /autogen_mail_generator/result

Given a text for generating a newsletter email and its attached audio version.

```bash
curl -X POST "http://localhost:8080/autogen_mail_generator/result" \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
      "text": "Former House Speaker Nancy Pelosi privately told President Joe Biden in a recent conversation that polling shows that the president cannot defeat      Donald Trump and that Biden could destroy Democrats chances of winning the House in November if he continues seeking a second term, according to four sources briefed on the call. The president responded by pushing back, telling Pelosi he has seen polls that indicate he can win, one source said. Another one of the sources described Biden as getting defensive about the polls. At one point, Pelosi asked Mike Donilon, Biden’s longtime adviser, to get on the line to talk over the data. This phone call would mark the second known conversation between the California lawmaker and Biden since the president’s disastrous debate on June 27. While the exact date of the conversation was not clear, one source described it as being within the last week. Pelosi and Biden also spoke in early July.None of the sources indicated whether Pelosi told Biden in this conversation that she believes the president should drop out of the 2024 race. Pelosi has spent the weeks following the debate listening to concerns from her colleagues. Pelosi made waves when she said in an interview last week: “It’s up to the president to decide if he is going to run. We’re all encouraging him to make that decision because time is running short.When asked for comment, White House spokesperson Andrew Bates did not respond to the details of CNN’s reporting on the recent Pelosi-Biden call. “President Biden is the nominee of the party. He plans to win and looks forward to working with congressional Democrats to pass his 100 days agenda to help working families,” Bates said.A Pelosi spokesperson told CNN that the former House speaker has been in California since Friday and she has not spoken to Biden since.",
      "recipientEmailAddress": "newsletter.members@example.com"
    }'
```


```json
{
    "status": "success",
    "invocationId": "4c2f8e56-4578-49ea-919b-f5fda0ddf1ba",
    "response": [
        {
            "message": "This is the email sent to the email address newsletter.members@example.com:\n\nNone",
            "type": "text"
        }
    ]
}
```
