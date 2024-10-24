# Google Search
This is a Google Search langchain agent that can be used with integrations in sidekick

## Testing the summarizer locally
In order to run the server you will need to run the following command to summarize sentences

```bash
curl --location --request POST 'http://localhost:8080/summarize_text/invoke' \
--header 'Content-Type: application/json' \
--data-raw '{
"input": {
"text": "Sam Altman, the CEO of OpenAI and co-founder of Worldcoin, recently testified before Congress alongside IBM%27s chief of trust, Christina Montgomery, and NYU professor Gary Marcus.%20%0A%0AThe Senate Judiciary Privacy, Technology, and the Law Subcommittee session represented Altmans first official appearance before Congress, giving senators the opportunity to question the OpenAI CEO concerning his companys views on regulation.%0A%0ADubbed a historic session by Illinois Senator Dick Durbin, the proceedings focused on understanding the potential threats posed by generative artificial intelligence (AI) models such as ChatGPT and how lawmakers should approach regulation.%0A%0AAltmans comments , which were described by congressional members and fellow speaker Marcus as seeming sincere and genuine , appeared to take several Senate members by surprise.%0A%0AHe advocated for the establishment of a federal oversight agency with the authority to issue and revoke development licenses, stated that he believed creators should be compensated when their work is used to train an AI system and agreed that consumers who suffer harm using AI products should be entitled to sue the developer.%0A%0AAltman shrugged off questions related to the recent AI pause letter calling for a six-month moratorium on the deployment of systems more powerful than GPT-4, the AI system underpinning ChatGPT, by stating that OpenAI had spent longer than six months evaluating GPT-4 before deployment. He said the company had no plans to deplcleoy another model within the next six months.%0A%0AMarcus, a signatory of the pause letter, admitted he agreed more to the spirit of the letter than its contents, but the NYU professor urged Congress to consider global oversight as well as federal regulation %E2%80%94 a sentiment Altman agreed with.%0A%0AThroughout the hearing, the three guest speakers aligned on most topics. This included support for privacy protections, greater government oversight, third-party auditing and how soon the United States government should seek to regulate the industry (immediately).",
"summary_type": "sentences",
"number": "3",
"style": "business"
}
}'
```

and bullet points:

```bash
curl --location --request POST 'http://localhost:8080/summarize_text/invoke' \
--header 'Content-Type: application/json' \
--data-raw '{
"input": {
"text": "Sam Altman, the CEO of OpenAI and co-founder of Worldcoin, recently testified before Congress alongside IBM%27s chief of trust, Christina Montgomery, and NYU professor Gary Marcus.%20%0A%0AThe Senate Judiciary Privacy, Technology, and the Law Subcommittee session represented Altmans first official appearance before Congress, giving senators the opportunity to question the OpenAI CEO concerning his companys views on regulation.%0A%0ADubbed a historic session by Illinois Senator Dick Durbin, the proceedings focused on understanding the potential threats posed by generative artificial intelligence (AI) models such as ChatGPT and how lawmakers should approach regulation.%0A%0AAltmans comments , which were described by congressional members and fellow speaker Marcus as seeming sincere and genuine , appeared to take several Senate members by surprise.%0A%0AHe advocated for the establishment of a federal oversight agency with the authority to issue and revoke development licenses, stated that he believed creators should be compensated when their work is used to train an AI system and agreed that consumers who suffer harm using AI products should be entitled to sue the developer.%0A%0AAltman shrugged off questions related to the recent AI pause letter calling for a six-month moratorium on the deployment of systems more powerful than GPT-4, the AI system underpinning ChatGPT, by stating that OpenAI had spent longer than six months evaluating GPT-4 before deployment. He said the company had no plans to deplcleoy another model within the next six months.%0A%0AMarcus, a signatory of the pause letter, admitted he agreed more to the spirit of the letter than its contents, but the NYU professor urged Congress to consider global oversight as well as federal regulation %E2%80%94 a sentiment Altman agreed with.%0A%0AThroughout the hearing, the three guest speakers aligned on most topics. This included support for privacy protections, greater government oversight, third-party auditing and how soon the United States government should seek to regulate the industry (immediately).",
"summary_type": "bullets",
"number": "5",
"style": "business"
}
}'
```

## Testing the search remotely
In order to run the server you will need to run the following command

```bash
curl --location --request POST 'https://langserve.1eqk2rork3yg.eu-gb.codeengine.appdomain.cloud/summarize_text/invoke' \
--header 'Content-Type: application/json' \
--data-raw '{
"input": {
"text": "Sam Altman, the CEO of OpenAI and co-founder of Worldcoin, recently testified before Congress alongside IBM%27s chief of trust, Christina Montgomery, and NYU professor Gary Marcus.%20%0A%0AThe Senate Judiciary Privacy, Technology, and the Law Subcommittee session represented Altmans first official appearance before Congress, giving senators the opportunity to question the OpenAI CEO concerning his companys views on regulation.%0A%0ADubbed a historic session by Illinois Senator Dick Durbin, the proceedings focused on understanding the potential threats posed by generative artificial intelligence (AI) models such as ChatGPT and how lawmakers should approach regulation.%0A%0AAltmans comments , which were described by congressional members and fellow speaker Marcus as seeming sincere and genuine , appeared to take several Senate members by surprise.%0A%0AHe advocated for the establishment of a federal oversight agency with the authority to issue and revoke development licenses, stated that he believed creators should be compensated when their work is used to train an AI system and agreed that consumers who suffer harm using AI products should be entitled to sue the developer.%0A%0AAltman shrugged off questions related to the recent AI pause letter calling for a six-month moratorium on the deployment of systems more powerful than GPT-4, the AI system underpinning ChatGPT, by stating that OpenAI had spent longer than six months evaluating GPT-4 before deployment. He said the company had no plans to deplcleoy another model within the next six months.%0A%0AMarcus, a signatory of the pause letter, admitted he agreed more to the spirit of the letter than its contents, but the NYU professor urged Congress to consider global oversight as well as federal regulation %E2%80%94 a sentiment Altman agreed with.%0A%0AThroughout the hearing, the three guest speakers aligned on most topics. This included support for privacy protections, greater government oversight, third-party auditing and how soon the United States government should seek to regulate the industry (immediately).",
"summary_type": "sentences",
"number": "5",
"style": "business"
}
}'
```

or

```bash
curl --location --request POST 'https://langserve.1eqk2rork3yg.eu-gb.codeengine.appdomain.cloud/summarize_text/invoke' \
--header 'Content-Type: application/json' \
--data-raw '{
"input": {
"text": "Sam Altman, the CEO of OpenAI and co-founder of Worldcoin, recently testified before Congress alongside IBM%27s chief of trust, Christina Montgomery, and NYU professor Gary Marcus.%20%0A%0AThe Senate Judiciary Privacy, Technology, and the Law Subcommittee session represented Altmans first official appearance before Congress, giving senators the opportunity to question the OpenAI CEO concerning his companys views on regulation.%0A%0ADubbed a historic session by Illinois Senator Dick Durbin, the proceedings focused on understanding the potential threats posed by generative artificial intelligence (AI) models such as ChatGPT and how lawmakers should approach regulation.%0A%0AAltmans comments , which were described by congressional members and fellow speaker Marcus as seeming sincere and genuine , appeared to take several Senate members by surprise.%0A%0AHe advocated for the establishment of a federal oversight agency with the authority to issue and revoke development licenses, stated that he believed creators should be compensated when their work is used to train an AI system and agreed that consumers who suffer harm using AI products should be entitled to sue the developer.%0A%0AAltman shrugged off questions related to the recent AI pause letter calling for a six-month moratorium on the deployment of systems more powerful than GPT-4, the AI system underpinning ChatGPT, by stating that OpenAI had spent longer than six months evaluating GPT-4 before deployment. He said the company had no plans to deplcleoy another model within the next six months.%0A%0AMarcus, a signatory of the pause letter, admitted he agreed more to the spirit of the letter than its contents, but the NYU professor urged Congress to consider global oversight as well as federal regulation %E2%80%94 a sentiment Altman agreed with.%0A%0AThroughout the hearing, the three guest speakers aligned on most topics. This included support for privacy protections, greater government oversight, third-party auditing and how soon the United States government should seek to regulate the industry (immediately).",
"summary_type": "bullets",
"number": "5",
"style": "business"
}
}'
```
