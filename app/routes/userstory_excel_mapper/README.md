# userstory_excel_mapper Integration

This integration provides functionality for generating an excel file with detailed user stories from the given requirements.

It has two steps involved - 
1. Triggers a background task and returns a URL to downlaod the xlsx file with detailed user stories. This URL can be used only after the completion of background task.
2. The background task is completed and the xlsx file is ready to be downloaded.

To ensure fair usage, user story generation is capped at 10 requirements per request. Any additional requirements have to be submitted in a new request to continue the process.

Input: - Business Objective: Implementing <Strategic Initiative> for <Persona> in the <Industry> domain, to <Business Goal> 
       - Requirement: <Text>
Final Output: An excel file with the User story details for all the reqirements
This excel can be used to bulk import the user stories to JIRA.

Optional input parameters: epicToUsAssistantId, usDetailAssistantId

This integration chains multiple assistants, 
First step is to fetch the single line user stories for the input Epics - Assistant 22113 (epicToUsAssistantId) is used for this purpose
Second step to to fetch detailed  user stories for each of the single line user stories - Assistant 8352 (usDetailAssistantId) is used for this purpose

If you want to bring in your own assistants, please make sure that the output of the assistants is in github markdown format.
This integration currently takes around 2 mins to generate 30 detailed user stories.


## Endpoint

### 1. Initiate background tasks (Asynchronous)

- **POST** `/system/us_excel_mapper/generate_excel/invoke`

  Executes the request asynchronously using BackgroundTasks. Returns a URL to download the xlsx file with detailed user stories, which can be used after some time (once the background tasks are completed).

#### Example 1 - To generate as many user stories as possible for the given inputs
To ensure fair usage, user story generation is capped at 10 requirements per request. Any additional requirements have to be submitted in a new request to continue the process.

```bash
curl --silent --location --request POST 'http://localhost:8080/system/us_excel_mapper/generate_excel/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{ "epicToUsAssistantId":"22113", "usDetailAssistantId":"8352", "inputType": "UserStory", "input": "- Business Objective: Implementing a property management app for Property Owners and Service Providers in the retail domain, to enhance property management experience \n - Requirement: \n Login \n Profile \n Search and Select Asset \n Maintenance Request \n Quotation \n Payment \n Reviews \n Registration \n Offline Functionality \n Dark mode \n Accessibility" }'
```

```json
{
  "status": "processing",
  "invocationId": "3bad9c0f-8211-4450-b047-fea3c85ffd68",
  "response": [
    {
      "message": "The generation of user stories has started. Please use the following URL after 10 minutes, and within 24 hours, to access the generated user stories: \n http://127.0.0.1:8080/public/xlsx_builder/xlsx_93f2dc47-981f-4a4b-ae03-7b97c6b55f2d.xlsx \n\n Please Note: User stories can only be generated for up to 10 requirements at a time. Any additional requirements have been excluded from this session. Kindly submit the remaining requirements in a separate request to proceed with their generation.",
      "type": "text"
    }
  ]
}
```


##### Example 2 - To generate a limited number of user stories for the given inputs

```bash
curl --silent --location --request POST 'http://localhost:8080/system/us_excel_mapper/generate_excel/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{ "epicToUsAssistantId":"22113", "usDetailAssistantId":"8352", "inputType": "UserStory", "input": "- Business Objective: Implementing an eCommerce app for end Customer in the retail domain, to enhance buying experience \n - Requirement: \n Login \n Profile \n Product" }'
```

```json
{
  "status": "processing",
  "invocationId": "69973548-1c49-476a-8b78-9b1178e66074",
  "response": [
    {
      "message": "The generation of user stories has started. Please use the following URL after 10 minutes, and within 24 hours, to access the generated user stories: \n http://127.0.0.1:8080/public/xlsx_builder/xlsx_25a53fe3-3426-4575-855a-4d14f3dd8b4d.xlsx ",
      "type": "text"
    }
  ]
}
```