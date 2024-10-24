# cv_builder Integration

This integration provides functionality for CV Builder integration.

## API Endpoints

### POST /system/cv_builder/enhance_profile/invoke

Helps users to enhance specific section of their CV profile, this enpoint will get your current CV and use a LLM to suggest a better description for your profile, skillset or any other profile section.

Section options are: overview, key_skills, key_courses, experience, education, languages, assignments
you can also use 'full' as section and the LLM will tailor your CV based on the intent i.e intent='tailor my profile for a banking industry postition'

```bash
curl -X POST "http://localhost:8080/cv_builder/enhance_profile/invoke" \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{"user_id": "999999999", "section":"overview", "intent":"I would like to show my leadership skills and my desired to take risks"}'
```

```json
{
  "status": "success",
  "invocationId": "f3589037-8ade-4049-b9ad-2f2eecda83bc",
  "response": [
    {
      "message": "Here's the proposal to your request for enhance your overview:

Here's an enhanced version of the profile section that incorporates the user's intent to showcase leadership skills and a willingness to take risks and embrace changes:

Results-driven technology professional with a strong background in Computer Science and approximately 8 years of experience in software development and analyzing requirements documentation. Proven leader with a track record of driving innovative solutions, leveraging extensive knowledge of the SAP system, including hands-on understanding of ABAP development and HCM functional knowledge. Adept at harnessing the power of emerging technologies, including robot process automation, Cloud technologies, and cognitive services like Watson Assistant, text to speech, API connections, and SLACK applications. Possesses excellent analytical, problem-solving, and written/verbal communication skills, complemented by a high degree of organizational, teamwork, and time management abilities. A change agent with a passion for taking calculated risks, driving digital transformation, and leading cross-functional teams to achieve exceptional results in fast-paced and dynamic environments.\"

I made the following changes to enhance the section:

* Added \"Results-driven technology professional\" to emphasize the user's ability to deliver results.
* Introduced \"Proven leader\" to explicitly highlight leadership skills.
* Emphasized the user's ability to \"drive innovative solutions\" to showcase their willingness to take risks and embrace changes.
* Used phrases like \"harnessing the power of emerging technologies\" and \"change agent\" to convey a sense of adaptability and forward thinking.
* Maintained the same format and structure as the original section to ensure consistency.

This revised section aims to showcase the user's leadership skills, ability to take risks, and willingness to embrace changes, while still highlighting their technical expertise and soft skills.

For reference, the current profile description in your cv is:

Current Profile Information.

Is there anything else you'd like me to help on your CV?",
      "type": "text"
    }
  ]
}
```

### POST /experience/cv_builder/update_overview/invoke

Invokes the cv_builder update function to reflect the proposed changes in the actual CV.

```bash
curl --silent --location --request PUT 'http://localhost:8080/cv_builder/update_overview/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{"user_id": "999999999", "section":"overview","enhanced_section":"Proposed Version from previous interaction"}' | jq
```

```json
{
  "status": "success",
  "invocationId": "a3264395-b542-4127-ad47-772685b1da8a",
  "response": [
    {
      "message": "Your profile has been successfully updated with the following information

Results-driven technology professional with a strong background in Computer Science and approximately 8 years of experience in software development and analyzing requirements documentation. Proven leader with a track record of driving innovative solutions, leveraging extensive knowledge of the SAP system, including hands-on understanding of ABAP development and HCM functional knowledge. Adept at harnessing the power of emerging technologies, including robot process automation, Cloud technologies, and cognitive services like Watson Assistant, text to speech, API connections, and SLACK applications. Possesses excellent analytical, problem-solving, and written/verbal communication skills, complemented by a high degree of organizational, teamwork, and time management abilities. A change agent with a passion for taking calculated risks, driving digital transformation, and leading cross-functional teams to achieve exceptional results in fast-paced and dynamic environments.

Is there anything else you'd like me to help on your CV?",
      "type": "text"
    }
  ]
}
```
