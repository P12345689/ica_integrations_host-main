# autogen_news_webscraper Integration

> Authors: Ali Hassan, Max Belitsky, Dennis Weiss

This module implements an `autogen` nested group chat to scrape a news page for articles of a specific industry and provides a summary with the impact on the industry.

## API Endpoints

### POST /autogen_news_webscraper/result

Given a text in news page URL `newsUrl` and the `industry` of interest, scrapes the news page and provides a summary.

```bash
curl -X POST "http://localhost:8080/autogen_news_webscraper/result" \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
    "newsUrl": "https://www.swissinfo.ch/eng/bloomberg",
    "industry": "Pharmaceutical"
    }'
```

```json
{
    "status": "success",
    "invocationId": "cedbc740-3e66-45e8-8fe1-a1eae29f5e00",
    "response": [
        {
            "message": "We scraped the following news:\n\n\"Novartis Raises 2024 Profit Forecast on Demand For New Blockbuster Drugs\"\nSummary: While sales of Novartis AG’s prostate cancer drug Pluvicto disappointed in the latest quarter, the pharmaceutical company raised its profit forecast due to the demand for its new blockbuster drugs. This could mean an increase in Novartis' overall revenue and positive growth in the pharmaceutical industry. \nLink: [Read More](https://www.swissinfo.ch/eng/novartis-raises-2024-profit-forecast-on-demand-for-new-blockbuster-drugs/84186716)\n\n\"Roche Jumps After Weight-Loss Pill Shows Promise in Study\"\nSummary: Shares of Roche Holding AG saw a significant increase after their experimental weight loss pill showed promising results in an early stage study among obesity patients. This could potentially lead to a new successful product in the pharmaceutical market. \nLink: [Read More](https://www.swissinfo.ch/eng/roche-jumps-after-weight-loss-pill-shows-promise-in-study/84068829)\n\n\"First Malaria Shots From Biggest Vaccine Maker Deployed in Africa\"\nSummary: Ivory Coast has become the first country to deploy a malaria shot developed by Serum Institute of India Ltd., the world’s largest vaccine maker, and the University of Oxford. This could imply potential growth for the Serum Institute and an increase in demand for their products in the pharmaceutical industry.\nLink: [Read More](https://www.swissinfo.ch/eng/first-malaria-shots-from-biggest-vaccine-maker-deployed-in-africa/83815074)",
            "type": "text"
        }
    ]
}
```
