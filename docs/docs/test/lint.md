# Linting code (static analysis)

## Sorting imports with isort

```
Fixing /home/cmihai/production/ica_integrations_host/app/routes/googlesearch/googlesearch_router.py
Fixing /home/cmihai/production/ica_integrations_host/app/routes/duckduckgo/duckduckgo_router.py
Fixing /home/cmihai/production/ica_integrations_host/app/routes/instagram/instagram_router.py
Fixing /home/cmihai/production/ica_integrations_host/app/routes/mermaid/mermaid_router.py
Fixing /home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py
Fixing /home/cmihai/production/ica_integrations_host/app/routes/geministt/geministt_router.py
Fixing /home/cmihai/production/ica_integrations_host/app/routes/wikipedia/wikipedia_router.py
Fixing /home/cmihai/production/ica_integrations_host/app/routes/time/time_router.py
Fixing /home/cmihai/production/ica_integrations_host/app/routes/summarizer/summarizer_router.py
Fixing /home/cmihai/production/ica_integrations_host/app/routes/jokes/jokes_router.py
Skipped 3 files


```

## Linting with flake8

```
app/routes/docbuilder/__init__.py:20:1: F401 '.docbuilder_router.add_custom_routes' imported but unused
app/routes/docbuilder/docbuilder_router.py:15:1: F401 'fastapi.staticfiles.StaticFiles' imported but unused
app/routes/docbuilder/docbuilder_router.py:20:1: F811 redefinition of unused 're' from line 10
app/routes/docbuilder/docbuilder_router.py:20:1: E402 module level import not at top of file
app/routes/docbuilder/docbuilder_router.py:52:9: F841 local variable 'request_type' is assigned to but never used
app/routes/duckduckgo/__init__.py:2:1: F401 '.duckduckgo_router.add_custom_routes' imported but unused
app/routes/duckduckgo/duckduckgo_router.py:3:1: F401 'sys' imported but unused
app/routes/duckduckgo/duckduckgo_router.py:4:1: F401 'pathlib.Path' imported but unused
app/routes/duckduckgo/duckduckgo_router.py:15:12: F541 f-string is missing placeholders
app/routes/duckduckgo/duckduckgo_router.py:54:9: F841 local variable 'e' is assigned to but never used
app/routes/duckduckgo/duckduckgo_router.py:57:32: F541 f-string is missing placeholders
app/routes/geministt/__init__.py:2:1: F401 '.geministt_router.add_custom_routes' imported but unused
app/routes/geministt/geministt_router.py:2:1: F401 'sys' imported but unused
app/routes/geministt/geministt_router.py:3:1: F401 'pathlib.Path' imported but unused
app/routes/geministt/geministt_router.py:6:1: F401 'langchain.chains.LLMChain' imported but unused
app/routes/geministt/geministt_router.py:7:1: F401 'langchain.prompts.ChatPromptTemplate' imported but unused
app/routes/geministt/geministt_router.py:9:1: F401 'langchain_consultingassistants.ChatConsultingAssistants' imported but unused
app/routes/googlesearch/__init__.py:2:1: F401 '.googlesearch_router.add_custom_routes' imported but unused
app/routes/googlesearch/googlesearch_router.py:3:1: F401 'sys' imported but unused
app/routes/googlesearch/googlesearch_router.py:4:1: F401 'pathlib.Path' imported but unused
app/routes/googlesearch/googlesearch_router.py:15:12: F541 f-string is missing placeholders
app/routes/googlesearch/googlesearch_router.py:54:9: F841 local variable 'e' is assigned to but never used
app/routes/googlesearch/googlesearch_router.py:57:32: F541 f-string is missing placeholders
app/routes/gpt4vision/__init__.py:2:1: F401 '.gpt4vision_router.add_custom_routes' imported but unused
app/routes/gpt4vision/gpt4vision_router.py:3:1: F401 'sys' imported but unused
app/routes/gpt4vision/gpt4vision_router.py:4:1: F401 'pathlib.Path' imported but unused
app/routes/gpt4vision/gpt4vision_router.py:8:1: F401 'langchain.chains.LLMChain' imported but unused
app/routes/gpt4vision/gpt4vision_router.py:9:1: F401 'langchain.prompts.PromptTemplate' imported but unused
app/routes/gpt4vision/gpt4vision_router.py:10:1: F401 'langchain_community.utilities.GoogleSearchAPIWrapper' imported but unused
app/routes/gpt4vision/gpt4vision_router.py:67:9: F841 local variable 'e' is assigned to but never used
app/routes/health/__init__.py:2:1: F401 '.health_router.add_custom_routes' imported but unused
app/routes/health/health_router.py:2:1: F401 'json' imported but unused
app/routes/instagram/__init__.py:2:1: F401 '.instagram_router.add_custom_routes' imported but unused
app/routes/instagram/instagram_router.py:3:1: F401 'sys' imported but unused
app/routes/instagram/instagram_router.py:4:1: F401 'pathlib.Path' imported but unused
app/routes/instagram/instagram_router.py:51:32: F541 f-string is missing placeholders
app/routes/jokes/__init__.py:2:1: F401 '.jokes_router.add_custom_routes' imported but unused
app/routes/jokes/jokes_router.py:2:1: F401 'sys' imported but unused
app/routes/jokes/jokes_router.py:3:1: F401 'pathlib.Path' imported but unused
app/routes/mermaid/__init__.py:2:1: F401 '.mermaid_router.add_custom_routes' imported but unused
app/routes/mermaid/mermaid_router.py:3:1: F401 'os' imported but unused
app/routes/mermaid/mermaid_router.py:5:1: F401 'sys' imported but unused
app/routes/mermaid/mermaid_router.py:6:1: F401 'pathlib.Path' imported but unused
app/routes/mermaid/mermaid_router.py:8:1: F401 'requests' imported but unused
app/routes/mermaid/mermaid_router.py:12:1: F401 'langchain_community.utilities.GoogleSearchAPIWrapper' imported but unused
app/routes/mermaid/mermaid_router.py:27:5: F841 local variable 'e' is assigned to but never used
app/routes/mermaid/mermaid_router.py:75:9: F841 local variable 'e' is assigned to but never used
app/routes/mermaid/mermaid_router.py:130:9: F841 local variable 'e' is assigned to but never used
app/routes/mermaid/mermaid_router.py:181:9: F841 local variable 'e' is assigned to but never used
app/routes/qareact/__init__.py:2:1: F401 '.qareact_router.add_custom_routes' imported but unused
app/routes/qareact/qareact_router.py:2:1: F401 'sys' imported but unused
app/routes/qareact/qareact_router.py:3:1: F401 'pathlib.Path' imported but unused
app/routes/qareact/qareact_router.py:7:1: F401 'langchain.chains.LLMChain' imported but unused
app/routes/qareact/qareact_router.py:85:13: F841 local variable 'error_message' is assigned to but never used
app/routes/qareact/qareact_router.py:87:22: F541 f-string is missing placeholders
app/routes/summarizer/__init__.py:2:1: F401 '.summarizer_router.add_custom_routes' imported but unused
app/routes/summarizer/summarizer_router.py:3:1: F401 'sys' imported but unused
app/routes/summarizer/summarizer_router.py:4:1: F401 'pathlib.Path' imported but unused
app/routes/summarizer/summarizer_router.py:36:9: F841 local variable 'e' is assigned to but never used
app/routes/summarizer/summarizer_router.py:38:32: F541 f-string is missing placeholders
app/routes/test/__init__.py:19:1: F401 '.test_router.add_custom_routes' imported but unused
app/routes/test/test_router.py:14:1: E302 expected 2 blank lines, found 1
app/routes/test_llm/__init__.py:20:1: F401 '.test_llm_router.add_custom_routes' imported but unused
app/routes/time/__init__.py:2:1: F401 '.time_router.add_custom_routes' imported but unused
app/routes/time/time_router.py:14:12: F541 f-string is missing placeholders
app/routes/time/time_router.py:55:9: F841 local variable 'e' is assigned to but never used
app/routes/time/time_router.py:57:32: F541 f-string is missing placeholders
app/routes/time/time_router.py:80:9: F841 local variable 'e' is assigned to but never used
app/routes/webex_summarizer/__init__.py:20:1: F401 '.webex_summarizer_router.add_custom_routes' imported but unused
app/routes/webex_summarizer/webex_summarizer_router.py:7:1: F401 'json' imported but unused
app/routes/webex_summarizer/webex_summarizer_router.py:12:1: F401 'libica.ICAClient' imported but unused
app/routes/webex_summarizer/webex_summarizer_router.py:37:19: F821 undefined name 'HTTPException'
app/routes/wikipedia/__init__.py:19:1: F401 '.wikipedia_router.add_custom_routes' imported but unused
app/routes/wikipedia/wikipedia.py:8:1: F401 'os' imported but unused
app/routes/wikipedia/wikipedia.py:9:1: F401 'sys' imported but unused
app/routes/wikipedia/wikipedia.py:11:1: F401 'typing.List' imported but unused
app/routes/wikipedia/wikipedia_router.py:12:1: F401 'libica.ICAClient' imported but unused
app/server.py:3:1: F401 'sys' imported but unused
app/staging_routes/datagenerator/__init__.py:20:1: F401 '.datagenerator_router.add_custom_routes' imported but unused
app/staging_routes/datagenerator/datagenerator_router.py:17:1: F401 'libica.ICAClient' imported but unused


```

## Linting with pylint

```
************* Module app.server
app/server.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app/server.py:3:0: W0611: Unused import sys (unused-import)

------------------------------------------------------------------
Your code has been rated at 9.20/10 (previous run: 9.20/10, +0.00)



```

## Linting with mypy

```


```

## Linting with bandit

```
Run started:2024-05-02 10:39:01.927434

Test results:
>> Issue: [B404:blacklist] Consider possible security implications associated with the subprocess module.
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.7.8/blacklists/blacklist_imports.html#b404-import-subprocess
   Location: app/routes/docbuilder/docbuilder_router.py:11:0
10	import re
11	import subprocess
12	from uuid import uuid4

--------------------------------------------------
>> Issue: [B607:start_process_with_partial_path] Starting a process with a partial executable path
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.7.8/plugins/b607_start_process_with_partial_path.html
   Location: app/routes/docbuilder/docbuilder_router.py:134:8
133	        # Generate .docx
134	        subprocess.run(["pandoc", markdown_file_path, "-o", docx_file_path])
135

--------------------------------------------------
>> Issue: [B603:subprocess_without_shell_equals_true] subprocess call - check for execution of untrusted input.
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.7.8/plugins/b603_subprocess_without_shell_equals_true.html
   Location: app/routes/docbuilder/docbuilder_router.py:134:8
133	        # Generate .docx
134	        subprocess.run(["pandoc", markdown_file_path, "-o", docx_file_path])
135

--------------------------------------------------
>> Issue: [B607:start_process_with_partial_path] Starting a process with a partial executable path
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.7.8/plugins/b607_start_process_with_partial_path.html
   Location: app/routes/docbuilder/docbuilder_router.py:137:8
136	        # Generate .pptx (assuming the input is suitable for slides)
137	        subprocess.run(
138	            [
139	                "pandoc",
140	                "-s",
141	                markdown_file_path,
142	                "--reference-doc",
143	                template_name,
144	                "-o",
145	                pptx_file_path,
146	                "--slide-level=2",
147	            ]
148	        )
149

--------------------------------------------------
>> Issue: [B603:subprocess_without_shell_equals_true] subprocess call - check for execution of untrusted input.
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.7.8/plugins/b603_subprocess_without_shell_equals_true.html
   Location: app/routes/docbuilder/docbuilder_router.py:137:8
136	        # Generate .pptx (assuming the input is suitable for slides)
137	        subprocess.run(
138	            [
139	                "pandoc",
140	                "-s",
141	                markdown_file_path,
142	                "--reference-doc",
143	                template_name,
144	                "-o",
145	                pptx_file_path,
146	                "--slide-level=2",
147	            ]
148	        )
149

--------------------------------------------------
>> Issue: [B113:request_without_timeout] Requests call without timeout
   Severity: Medium   Confidence: Low
   CWE: CWE-400 (https://cwe.mitre.org/data/definitions/400.html)
   More Info: https://bandit.readthedocs.io/en/1.7.8/plugins/b113_request_without_timeout.html
   Location: app/routes/geministt/test.py:13:15
12	    # Fetch audio content from URL
13	    response = requests.get(url)
14	    audio_content = base64.b64encode(response.content).decode("utf-8")

--------------------------------------------------
>> Issue: [B113:request_without_timeout] Requests call without timeout
   Severity: Medium   Confidence: Low
   CWE: CWE-400 (https://cwe.mitre.org/data/definitions/400.html)
   More Info: https://bandit.readthedocs.io/en/1.7.8/plugins/b113_request_without_timeout.html
   Location: app/routes/gpt4vision/gpt4vision_router.py:44:15
43	    # call gpt4 vision azure
44	    response = requests.post(url, headers=headers, json=data)
45

--------------------------------------------------
>> Issue: [B113:request_without_timeout] Requests call without timeout
   Severity: Medium   Confidence: Low
   CWE: CWE-400 (https://cwe.mitre.org/data/definitions/400.html)
   More Info: https://bandit.readthedocs.io/en/1.7.8/plugins/b113_request_without_timeout.html
   Location: app/routes/webex_summarizer/webex.py:40:15
39
40	    response = requests.get(url, headers=headers)
41	    if response.status_code == 200:

--------------------------------------------------
>> Issue: [B113:request_without_timeout] Requests call without timeout
   Severity: Medium   Confidence: Low
   CWE: CWE-400 (https://cwe.mitre.org/data/definitions/400.html)
   More Info: https://bandit.readthedocs.io/en/1.7.8/plugins/b113_request_without_timeout.html
   Location: app/routes/webex_summarizer/webex.py:46:34
45	            download_link = transcripts[-1]["txtDownloadLink"]
46	            transcript_response = requests.get(download_link, headers=headers)
47	            if transcript_response.status_code == 200:

--------------------------------------------------

Code scanned:
	Total lines of code: 1206
	Total lines skipped (#nosec): 0
	Total potential issues skipped due to specifically being disabled (e.g., #nosec BXXX): 0

Run metrics:
	Total issues (by severity):
		Undefined: 0
		Low: 5
		Medium: 4
		High: 0
	Total issues (by confidence):
		Undefined: 0
		Low: 4
		Medium: 0
		High: 5
Files skipped (0):


```

## Linting with pydocstyle

```
app/server.py:1 at module level:
        D100: Missing docstring in public module
app/__init__.py:1 at module level:
        D104: Missing docstring in public package
app/routes/googlesearch/__init__.py:1 at module level:
        D104: Missing docstring in public package
app/routes/googlesearch/googlesearch_router.py:1 at module level:
        D100: Missing docstring in public module
app/routes/googlesearch/googlesearch_router.py:14 in public function `format_prompt`:
        D103: Missing docstring in public function
app/routes/googlesearch/googlesearch_router.py:26 in public function `add_custom_routes`:
        D103: Missing docstring in public function
app/routes/test_llm/__init__.py:2 at module level:
        D205: 1 blank line required between summary line and description (found 0)
app/routes/test_llm/__init__.py:2 at module level:
        D400: First line should end with a period (not 's')
app/routes/duckduckgo/__init__.py:1 at module level:
        D104: Missing docstring in public package
app/routes/duckduckgo/duckduckgo_router.py:1 at module level:
        D100: Missing docstring in public module
app/routes/duckduckgo/duckduckgo_router.py:14 in public function `format_prompt`:
        D103: Missing docstring in public function
app/routes/duckduckgo/duckduckgo_router.py:26 in public function `add_custom_routes`:
        D103: Missing docstring in public function
app/routes/instagram/__init__.py:1 at module level:
        D104: Missing docstring in public package
app/routes/instagram/instagram_router.py:1 at module level:
        D100: Missing docstring in public module
app/routes/instagram/instagram_router.py:13 in public function `add_custom_routes`:
        D103: Missing docstring in public function
app/routes/test/__init__.py:2 at module level:
        D200: One-line docstring should fit on one line with quotes (found 3)
app/routes/mermaid/__init__.py:1 at module level:
        D104: Missing docstring in public package
app/routes/mermaid/mermaid_router.py:1 at module level:
        D100: Missing docstring in public module
app/routes/mermaid/mermaid_router.py:17 in public function `format_prompt`:
        D103: Missing docstring in public function
app/routes/mermaid/mermaid_router.py:22 in public function `get_text_between_markers`:
        D103: Missing docstring in public function
app/routes/mermaid/mermaid_router.py:31 in public function `mm`:
        D103: Missing docstring in public function
app/routes/mermaid/mermaid_router.py:44 in public function `add_custom_routes`:
        D103: Missing docstring in public function
app/routes/qareact/__init__.py:1 at module level:
        D104: Missing docstring in public package
app/routes/qareact/qareact_router.py:1 at module level:
        D100: Missing docstring in public module
app/routes/qareact/qareact_router.py:15 in public function `add_custom_routes`:
        D103: Missing docstring in public function
app/routes/health/health_router.py:1 at module level:
        D100: Missing docstring in public module
app/routes/health/health_router.py:7 in public function `add_custom_routes`:
        D103: Missing docstring in public function
app/routes/health/__init__.py:1 at module level:
        D104: Missing docstring in public package
app/routes/gpt4vision/gpt4vision_router.py:1 at module level:
        D100: Missing docstring in public module
app/routes/gpt4vision/gpt4vision_router.py:13 in public function `call_gpt4_vision_api`:
        D103: Missing docstring in public function
app/routes/gpt4vision/gpt4vision_router.py:50 in public function `add_custom_routes`:
        D103: Missing docstring in public function
app/routes/gpt4vision/__init__.py:1 at module level:
        D104: Missing docstring in public package
app/routes/webex_summarizer/webex.py:2 at module level:
        D205: 1 blank line required between summary line and description (found 0)
app/routes/webex_summarizer/webex.py:2 at module level:
        D400: First line should end with a period (not 'i')
app/routes/webex_summarizer/webex.py:18 in public function `approximate_token_count`:
        D103: Missing docstring in public function
app/routes/webex_summarizer/webex.py:75 in public function `main`:
        D103: Missing docstring in public function
app/routes/webex_summarizer/__init__.py:2 at module level:
        D205: 1 blank line required between summary line and description (found 0)
app/routes/webex_summarizer/__init__.py:2 at module level:
        D400: First line should end with a period (not 's')
app/routes/webex_summarizer/webex_summarizer_router.py:2 at module level:
        D205: 1 blank line required between summary line and description (found 0)
app/routes/webex_summarizer/webex_summarizer_router.py:2 at module level:
        D400: First line should end with a period (not 'i')
app/routes/webex_summarizer/webex_summarizer_router.py:20 in public class `WebexSummarizationRequest`:
        D101: Missing docstring in public class
app/routes/webex_summarizer/webex_summarizer_router.py:27 in public function `add_custom_routes`:
        D103: Missing docstring in public function
app/routes/geministt/test.py:1 at module level:
        D100: Missing docstring in public module
app/routes/geministt/test.py:8 in public function `transcribe_audio_from_url`:
        D103: Missing docstring in public function
app/routes/geministt/geministt_router.py:1 at module level:
        D100: Missing docstring in public module
app/routes/geministt/geministt_router.py:12 in public function `add_custom_routes`:
        D103: Missing docstring in public function
app/routes/geministt/__init__.py:1 at module level:
        D104: Missing docstring in public package
app/routes/wikipedia/config.py:1 at module level:
        D100: Missing docstring in public module
app/routes/wikipedia/config.py:6 in public class `Settings`:
        D101: Missing docstring in public class
app/routes/wikipedia/config.py:18 in public nested class `Config`:
        D106: Missing docstring in public nested class
app/routes/wikipedia/__init__.py:2 at module level:
        D200: One-line docstring should fit on one line with quotes (found 3)
app/routes/wikipedia/__init__.py:2 at module level:
        D400: First line should end with a period (not 'n')
app/routes/wikipedia/wikipedia_router.py:2 at module level:
        D205: 1 blank line required between summary line and description (found 0)
app/routes/wikipedia/wikipedia_router.py:2 at module level:
        D400: First line should end with a period (not 'i')
app/routes/wikipedia/wikipedia_router.py:20 in public function `add_custom_routes`:
        D103: Missing docstring in public function
app/routes/wikipedia/wikipedia.py:2 at module level:
        D205: 1 blank line required between summary line and description (found 0)
app/routes/wikipedia/wikipedia.py:2 at module level:
        D400: First line should end with a period (not 'i')
app/routes/wikipedia/wikipedia.py:26 in public class `ResultsType`:
        D101: Missing docstring in public class
app/routes/wikipedia/wikipedia.py:31 in public class `WikipediaSearchInput`:
        D101: Missing docstring in public class
app/routes/wikipedia/wikipedia.py:41 in public class `ResponseItem`:
        D101: Missing docstring in public class
app/routes/wikipedia/wikipedia.py:47 in public function `search_wikipedia`:
        D205: 1 blank line required between summary line and description (found 0)
app/routes/wikipedia/wikipedia.py:47 in public function `search_wikipedia`:
        D400: First line should end with a period (not 's')
app/routes/wikipedia/wikipedia.py:120 in public function `format_response`:
        D401: First line should be in imperative mood (perhaps 'Format', not 'Formats')
app/routes/time/__init__.py:1 at module level:
        D104: Missing docstring in public package
app/routes/time/time_router.py:1 at module level:
        D100: Missing docstring in public module
app/routes/time/time_router.py:13 in public function `format_prompt`:
        D103: Missing docstring in public function
app/routes/time/time_router.py:25 in public function `add_custom_routes`:
        D103: Missing docstring in public function
app/routes/time/tools/__init__.py:1 at module level:
        D104: Missing docstring in public package
app/routes/time/tools/system_time_tool.py:1 at module level:
        D100: Missing docstring in public module
app/routes/time/tools/system_time_tool.py:10 in public function `get_system_time`:
        D400: First line should end with a period (not 't')
app/routes/time/tools/system_time_tool.py:10 in public function `get_system_time`:
        D401: First line should be in imperative mood (perhaps 'Return', not 'Returns')
app/routes/docbuilder/docbuilder_router.py:2 at module level:
        D205: 1 blank line required between summary line and description (found 0)
app/routes/docbuilder/docbuilder_router.py:2 at module level:
        D400: First line should end with a period (not 'i')
app/routes/docbuilder/docbuilder_router.py:24 in public function `clean_markdown_edge_quotes`:
        D401: First line should be in imperative mood (perhaps 'Remove', not 'Removes')
app/routes/docbuilder/docbuilder_router.py:48 in public function `add_custom_routes`:
        D103: Missing docstring in public function
app/routes/docbuilder/__init__.py:2 at module level:
        D205: 1 blank line required between summary line and description (found 0)
app/routes/docbuilder/__init__.py:2 at module level:
        D400: First line should end with a period (not 'e')
app/routes/summarizer/__init__.py:1 at module level:
        D104: Missing docstring in public package
app/routes/summarizer/summarizer_router.py:1 at module level:
        D100: Missing docstring in public module
app/routes/summarizer/summarizer_router.py:13 in public function `add_custom_routes`:
        D103: Missing docstring in public function
app/routes/jokes/__init__.py:1 at module level:
        D104: Missing docstring in public package
app/routes/jokes/jokes_router.py:1 at module level:
        D100: Missing docstring in public module
app/routes/jokes/jokes_router.py:12 in public function `add_custom_routes`:
        D103: Missing docstring in public function
app/staging_routes/datagenerator/datagenerator_router.py:2 at module level:
        D205: 1 blank line required between summary line and description (found 0)
app/staging_routes/datagenerator/datagenerator_router.py:2 at module level:
        D400: First line should end with a period (not 'i')
app/staging_routes/datagenerator/datagenerator_router.py:24 in public function `add_custom_routes`:
        D103: Missing docstring in public function
app/staging_routes/datagenerator/__init__.py:2 at module level:
        D205: 1 blank line required between summary line and description (found 0)
app/staging_routes/datagenerator/__init__.py:2 at module level:
        D400: First line should end with a period (not 'e')


```

## Linting with pycodestyle

```
app/routes/instagram/instagram_router.py:22:201: E501 line too long (333 > 200 characters)
app/routes/test/test_router.py:14:1: E302 expected 2 blank lines, found 1
app/routes/webex_summarizer/webex.py:14:201: E501 line too long (271 > 200 characters)
app/routes/docbuilder/docbuilder_router.py:20:1: E402 module level import not at top of file
1       E302 expected 2 blank lines, found 1
1       E402 module level import not at top of file
2       E501 line too long (333 > 200 characters)


```

## Linting with pre-commit hooks

```
check for added large files..............................................Passed
check python ast.........................................................Passed
check BOM - deprecated: use fix-byte-order-marker........................Passed
check builtin type constructor use.......................................Passed
check for case conflicts.................................................Passed
check docstring is first.................................................Passed
check that executables have shebangs.....................................Failed
- hook id: check-executables-have-shebangs
- exit code: 1

app/routes/webex_summarizer/webex.py: marked executable but has no (or invalid) shebang!
  If it isn't supposed to be executable, try: `chmod -x app/routes/webex_summarizer/webex.py`
  If on Windows, you may also need to: `git add --chmod=-x app/routes/webex_summarizer/webex.py`
  If it is supposed to be executable, double-check its shebang.
test.sh: marked executable but has no (or invalid) shebang!
  If it isn't supposed to be executable, try: `chmod -x test.sh`
  If on Windows, you may also need to: `git add --chmod=-x test.sh`
  If it is supposed to be executable, double-check its shebang.

check json...............................................................Passed
check that scripts with shebangs are executable..........................Passed
check for merge conflicts................................................Passed
check for broken symlinks................................................Passed
check toml...............................................................Passed
check vcs permalinks.....................................................Passed
check xml................................................................Passed
check yaml...............................................................Passed
debug statements (python)................................................Passed
detect destroyed symlinks................................................Passed
detect aws credentials...................................................Passed
detect private key.......................................................Passed
fix end of files.........................................................Failed
- hook id: end-of-file-fixer
- exit code: 1
- files were modified by this hook

Fixing docs/docs/app/routes/test/index.md
Fixing docs/docs/app/routes/mermaid/index.md
Fixing docs/docs/app/routes/time/time_router.md
Fixing docs/docs/app/routes/docbuilder/docbuilder_router.md
Fixing docs/docs/app/routes/googlesearch/googlesearch_router.md
Fixing docs/docs/app/routes/webex_summarizer/webex.md
Fixing docs/docs/app/routes/duckduckgo/index.md
Fixing docs/docs/app/routes/qareact/qareact_router.md
Fixing docs/docs/app/routes/googlesearch/index.md
Fixing docs/docs/app/routes/wikipedia/wikipedia.md
Fixing docs/docs/app/routes/instagram/index.md
Fixing docs/docs/app/staging_routes/datagenerator/index.md
Fixing docs/docs/app/routes/wikipedia/index.md
Fixing docs/docs/app/routes/webex_summarizer/webex_summarizer_router.md
Fixing docs/docs/app/routes/jokes/index.md
Fixing docs/docs/app/routes/instagram/instagram_router.md
Fixing docs/docs/app/routes/webex_summarizer/index.md
Fixing docs/docs/app/routes/geministt/test.md
Fixing docs/docs/app/routes/mermaid/mermaid_router.md
Fixing docs/docs/app/routes/jokes/jokes_router.md
Fixing docs/docs/app/routes/summarizer/index.md
Fixing docs/docs/app/routes/gpt4vision/gpt4vision_router.md
Fixing docs/docs/app/routes/test_llm/test_llm_router.md
Fixing docs/docs/app/routes/qareact/index.md
Fixing docs/docs/app/routes/wikipedia/config.md
Fixing docs/docs/app/routes/gpt4vision/index.md
Fixing docs/docs/app/routes/time/tools/index.md
Fixing docs/docs/app/routes/health/index.md
Fixing docs/docs/app/routes/wikipedia/wikipedia_router.md
Fixing docs/docs/app/routes/geministt/index.md
Fixing docs/docs/app/index.md
Fixing docs/docs/app/routes/time/index.md
Fixing docs/docs/app/routes/time/tools/system_time_tool.md
Fixing docs/docs/app/routes/test_llm/index.md
Fixing docs/docs/app/routes/docbuilder/index.md
Fixing docs/docs/app/routes/duckduckgo/duckduckgo_router.md
Fixing docs/docs/app/routes/health/health_router.md
Fixing docs/docs/app/routes/geministt/geministt_router.md
Fixing docs/docs/app/staging_routes/datagenerator/datagenerator_router.md
Fixing docs/docs/app/routes/test/test_router.md
Fixing docs/docs/app/routes/summarizer/summarizer_router.md

file contents sorter.................................(no files to check)Skipped
fix utf-8 byte order marker..............................................Passed
fix python encoding pragma...............................................Passed
forbid new submodules................................(no files to check)Skipped
forbid submodules....................................(no files to check)Skipped
mixed line ending........................................................Passed
python tests naming..................................(no files to check)Skipped
don't commit to branch...................................................Failed
- hook id: no-commit-to-branch
- exit code: 1
fix requirements.txt.....................................................Passed
sort simple yaml files...............................(no files to check)Skipped
trim trailing whitespace.................................................Passed


```

## Linting with ruff

```
app/routes/docbuilder/__init__.py:20:32: F401 `.docbuilder_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/routes/docbuilder/docbuilder_router.py:15:33: F401 [*] `fastapi.staticfiles.StaticFiles` imported but unused
app/routes/docbuilder/docbuilder_router.py:20:1: E402 Module level import not at top of file
app/routes/docbuilder/docbuilder_router.py:20:8: F811 [*] Redefinition of unused `re` from line 10
app/routes/docbuilder/docbuilder_router.py:52:9: F841 Local variable `request_type` is assigned to but never used
app/routes/duckduckgo/__init__.py:2:32: F401 `.duckduckgo_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/routes/duckduckgo/duckduckgo_router.py:3:8: F401 [*] `sys` imported but unused
app/routes/duckduckgo/duckduckgo_router.py:4:21: F401 [*] `pathlib.Path` imported but unused
app/routes/duckduckgo/duckduckgo_router.py:15:12: F541 [*] f-string without any placeholders
app/routes/duckduckgo/duckduckgo_router.py:54:29: F841 [*] Local variable `e` is assigned to but never used
app/routes/duckduckgo/duckduckgo_router.py:57:32: F541 [*] f-string without any placeholders
app/routes/geministt/__init__.py:2:31: F401 `.geministt_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/routes/geministt/geministt_router.py:2:8: F401 [*] `sys` imported but unused
app/routes/geministt/geministt_router.py:3:21: F401 [*] `pathlib.Path` imported but unused
app/routes/geministt/geministt_router.py:6:30: F401 [*] `langchain.chains.LLMChain` imported but unused
app/routes/geministt/geministt_router.py:7:31: F401 [*] `langchain.prompts.ChatPromptTemplate` imported but unused
app/routes/geministt/geministt_router.py:9:44: F401 [*] `langchain_consultingassistants.ChatConsultingAssistants` imported but unused
app/routes/googlesearch/__init__.py:2:34: F401 `.googlesearch_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/routes/googlesearch/googlesearch_router.py:3:8: F401 [*] `sys` imported but unused
app/routes/googlesearch/googlesearch_router.py:4:21: F401 [*] `pathlib.Path` imported but unused
app/routes/googlesearch/googlesearch_router.py:15:12: F541 [*] f-string without any placeholders
app/routes/googlesearch/googlesearch_router.py:54:29: F841 [*] Local variable `e` is assigned to but never used
app/routes/googlesearch/googlesearch_router.py:57:32: F541 [*] f-string without any placeholders
app/routes/gpt4vision/__init__.py:2:32: F401 `.gpt4vision_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/routes/gpt4vision/gpt4vision_router.py:3:8: F401 [*] `sys` imported but unused
app/routes/gpt4vision/gpt4vision_router.py:4:21: F401 [*] `pathlib.Path` imported but unused
app/routes/gpt4vision/gpt4vision_router.py:8:30: F401 [*] `langchain.chains.LLMChain` imported but unused
app/routes/gpt4vision/gpt4vision_router.py:9:31: F401 [*] `langchain.prompts.PromptTemplate` imported but unused
app/routes/gpt4vision/gpt4vision_router.py:10:43: F401 [*] `langchain_community.utilities.GoogleSearchAPIWrapper` imported but unused
app/routes/gpt4vision/gpt4vision_router.py:67:29: F841 [*] Local variable `e` is assigned to but never used
app/routes/health/__init__.py:2:28: F401 `.health_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/routes/health/health_router.py:2:8: F401 [*] `json` imported but unused
app/routes/instagram/__init__.py:2:31: F401 `.instagram_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/routes/instagram/instagram_router.py:3:8: F401 [*] `sys` imported but unused
app/routes/instagram/instagram_router.py:4:21: F401 [*] `pathlib.Path` imported but unused
app/routes/instagram/instagram_router.py:51:32: F541 [*] f-string without any placeholders
app/routes/jokes/__init__.py:2:27: F401 `.jokes_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/routes/jokes/jokes_router.py:2:8: F401 [*] `sys` imported but unused
app/routes/jokes/jokes_router.py:3:21: F401 [*] `pathlib.Path` imported but unused
app/routes/mermaid/__init__.py:2:29: F401 `.mermaid_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/routes/mermaid/mermaid_router.py:3:8: F401 [*] `os` imported but unused
app/routes/mermaid/mermaid_router.py:5:8: F401 [*] `sys` imported but unused
app/routes/mermaid/mermaid_router.py:6:21: F401 [*] `pathlib.Path` imported but unused
app/routes/mermaid/mermaid_router.py:8:8: F401 [*] `requests` imported but unused
app/routes/mermaid/mermaid_router.py:12:43: F401 [*] `langchain_community.utilities.GoogleSearchAPIWrapper` imported but unused
app/routes/mermaid/mermaid_router.py:27:25: F841 [*] Local variable `e` is assigned to but never used
app/routes/mermaid/mermaid_router.py:75:29: F841 [*] Local variable `e` is assigned to but never used
app/routes/mermaid/mermaid_router.py:130:29: F841 [*] Local variable `e` is assigned to but never used
app/routes/mermaid/mermaid_router.py:181:29: F841 [*] Local variable `e` is assigned to but never used
app/routes/qareact/__init__.py:2:29: F401 `.qareact_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/routes/qareact/qareact_router.py:2:8: F401 [*] `sys` imported but unused
app/routes/qareact/qareact_router.py:3:21: F401 [*] `pathlib.Path` imported but unused
app/routes/qareact/qareact_router.py:7:30: F401 [*] `langchain.chains.LLMChain` imported but unused
app/routes/qareact/qareact_router.py:85:13: F841 Local variable `error_message` is assigned to but never used
app/routes/qareact/qareact_router.py:87:22: F541 [*] f-string without any placeholders
app/routes/summarizer/__init__.py:2:32: F401 `.summarizer_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/routes/summarizer/summarizer_router.py:3:8: F401 [*] `sys` imported but unused
app/routes/summarizer/summarizer_router.py:4:21: F401 [*] `pathlib.Path` imported but unused
app/routes/summarizer/summarizer_router.py:36:29: F841 [*] Local variable `e` is assigned to but never used
app/routes/summarizer/summarizer_router.py:38:32: F541 [*] f-string without any placeholders
app/routes/test_llm/__init__.py:20:30: F401 `.test_llm_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/routes/time/__init__.py:2:26: F401 `.time_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/routes/time/time_router.py:14:12: F541 [*] f-string without any placeholders
app/routes/time/time_router.py:55:29: F841 [*] Local variable `e` is assigned to but never used
app/routes/time/time_router.py:57:32: F541 [*] f-string without any placeholders
app/routes/time/time_router.py:80:29: F841 [*] Local variable `e` is assigned to but never used
app/routes/webex_summarizer/__init__.py:20:38: F401 `.webex_summarizer_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/routes/webex_summarizer/webex_summarizer_router.py:7:8: F401 [*] `json` imported but unused
app/routes/webex_summarizer/webex_summarizer_router.py:12:20: F401 [*] `libica.ICAClient` imported but unused
app/routes/webex_summarizer/webex_summarizer_router.py:37:19: F821 Undefined name `HTTPException`
app/routes/wikipedia/__init__.py:19:31: F401 `.wikipedia_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/routes/wikipedia/wikipedia.py:8:8: F401 [*] `os` imported but unused
app/routes/wikipedia/wikipedia.py:9:8: F401 [*] `sys` imported but unused
app/routes/wikipedia/wikipedia.py:11:31: F401 [*] `typing.List` imported but unused
app/routes/wikipedia/wikipedia_router.py:12:20: F401 [*] `libica.ICAClient` imported but unused
app/server.py:3:8: F401 [*] `sys` imported but unused
app/staging_routes/datagenerator/__init__.py:20:35: F401 `.datagenerator_router.add_custom_routes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
app/staging_routes/datagenerator/datagenerator_router.py:17:20: F401 [*] `libica.ICAClient` imported but unused
Found 78 errors.
[*] 58 fixable with the `--fix` option (2 hidden fixes can be enabled with the `--unsafe-fixes` option).
10 files reformatted, 30 files left unchanged


```

## Linting with pyright

```
/home/cmihai/production/ica_integrations_host/app/server.py
  /home/cmihai/production/ica_integrations_host/app/server.py:8:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/server.py:9:6 - error: Import "fastapi.middleware.cors" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/server.py:10:6 - error: Import "fastapi.staticfiles" could not be resolved (reportMissingImports)
/home/cmihai/production/ica_integrations_host/app/routes/docbuilder/docbuilder_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/docbuilder/docbuilder_router.py:14:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/docbuilder/docbuilder_router.py:15:6 - error: Import "fastapi.staticfiles" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/docbuilder/docbuilder_router.py:114:59 - error: Argument of type "str | None" cannot be assigned to parameter "input_text" of type "str" in function "clean_markdown_edge_quotes"
    Type "str | None" is incompatible with type "str"
      "None" is incompatible with "str" (reportArgumentType)
/home/cmihai/production/ica_integrations_host/app/routes/duckduckgo/duckduckgo_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/duckduckgo/duckduckgo_router.py:6:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/duckduckgo/duckduckgo_router.py:7:6 - error: Import "langchain.chains" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/duckduckgo/duckduckgo_router.py:8:6 - error: Import "langchain.prompts" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/duckduckgo/duckduckgo_router.py:9:6 - error: Import "langchain_community.tools" could not be resolved (reportMissingImports)
/home/cmihai/production/ica_integrations_host/app/routes/geministt/geministt_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/geministt/geministt_router.py:5:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/geministt/geministt_router.py:6:6 - error: Import "langchain.chains" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/geministt/geministt_router.py:7:6 - error: Import "langchain.prompts" could not be resolved (reportMissingImports)
/home/cmihai/production/ica_integrations_host/app/routes/geministt/test.py
  /home/cmihai/production/ica_integrations_host/app/routes/geministt/test.py:5:26 - error: "speech" is unknown import symbol (reportAttributeAccessIssue)
/home/cmihai/production/ica_integrations_host/app/routes/googlesearch/googlesearch_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/googlesearch/googlesearch_router.py:6:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/googlesearch/googlesearch_router.py:7:6 - error: Import "langchain.chains" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/googlesearch/googlesearch_router.py:8:6 - error: Import "langchain.prompts" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/googlesearch/googlesearch_router.py:9:6 - error: Import "langchain_community.utilities" could not be resolved (reportMissingImports)
/home/cmihai/production/ica_integrations_host/app/routes/gpt4vision/gpt4vision_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/gpt4vision/gpt4vision_router.py:7:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/gpt4vision/gpt4vision_router.py:8:6 - error: Import "langchain.chains" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/gpt4vision/gpt4vision_router.py:9:6 - error: Import "langchain.prompts" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/gpt4vision/gpt4vision_router.py:10:6 - error: Import "langchain_community.utilities" could not be resolved (reportMissingImports)
/home/cmihai/production/ica_integrations_host/app/routes/health/health_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/health/health_router.py:4:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
/home/cmihai/production/ica_integrations_host/app/routes/instagram/instagram_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/instagram/instagram_router.py:6:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/instagram/instagram_router.py:7:6 - error: Import "langchain.chains" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/instagram/instagram_router.py:8:6 - error: Import "langchain.prompts" could not be resolved (reportMissingImports)
/home/cmihai/production/ica_integrations_host/app/routes/jokes/jokes_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/jokes/jokes_router.py:5:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/jokes/jokes_router.py:6:6 - error: Import "langchain.chains" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/jokes/jokes_router.py:7:6 - error: Import "langchain.prompts" could not be resolved (reportMissingImports)
/home/cmihai/production/ica_integrations_host/app/routes/mermaid/mermaid_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/mermaid/mermaid_router.py:9:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/mermaid/mermaid_router.py:10:6 - error: Import "langchain.chains" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/mermaid/mermaid_router.py:11:6 - error: Import "langchain.prompts" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/mermaid/mermaid_router.py:12:6 - error: Import "langchain_community.utilities" could not be resolved (reportMissingImports)
/home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py:5:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py:6:6 - error: Import "langchain.agents" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py:7:6 - error: Import "langchain.chains" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py:8:6 - error: Import "langchain.prompts" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py:9:6 - error: Import "langchain.tools" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py:10:6 - error: Import "langchain_community.utilities" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py:87:19 - error: "raw_result" is possibly unbound (reportPossiblyUnboundVariable)
/home/cmihai/production/ica_integrations_host/app/routes/summarizer/summarizer_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/summarizer/summarizer_router.py:6:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/summarizer/summarizer_router.py:7:6 - error: Import "langchain.chains" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/summarizer/summarizer_router.py:8:6 - error: Import "langchain.prompts" could not be resolved (reportMissingImports)
/home/cmihai/production/ica_integrations_host/app/routes/test/test_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/test/test_router.py:10:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
/home/cmihai/production/ica_integrations_host/app/routes/test_llm/test_llm_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/test_llm/test_llm_router.py:11:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
/home/cmihai/production/ica_integrations_host/app/routes/time/time_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/time/time_router.py:4:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/time/time_router.py:5:6 - error: Import "langchain.chains" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/time/time_router.py:6:6 - error: Import "langchain.prompts" could not be resolved (reportMissingImports)
/home/cmihai/production/ica_integrations_host/app/routes/time/tools/system_time_tool.py
  /home/cmihai/production/ica_integrations_host/app/routes/time/tools/system_time_tool.py:4:6 - error: Import "langchain.agents" could not be resolved (reportMissingImports)
/home/cmihai/production/ica_integrations_host/app/routes/webex_summarizer/webex_summarizer_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/webex_summarizer/webex_summarizer_router.py:11:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/routes/webex_summarizer/webex_summarizer_router.py:37:19 - error: "HTTPException" is not defined (reportUndefinedVariable)
/home/cmihai/production/ica_integrations_host/app/routes/wikipedia/wikipedia_router.py
  /home/cmihai/production/ica_integrations_host/app/routes/wikipedia/wikipedia_router.py:11:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
/home/cmihai/production/ica_integrations_host/app/staging_routes/datagenerator/datagenerator_router.py
  /home/cmihai/production/ica_integrations_host/app/staging_routes/datagenerator/datagenerator_router.py:15:8 - error: Import "pandas" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/staging_routes/datagenerator/datagenerator_router.py:16:6 - error: Import "fastapi" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/staging_routes/datagenerator/datagenerator_router.py:18:6 - error: Import "sdv.lite" could not be resolved (reportMissingImports)
  /home/cmihai/production/ica_integrations_host/app/staging_routes/datagenerator/datagenerator_router.py:19:6 - error: Import "sdv.metadata" could not be resolved (reportMissingImports)
56 errors, 0 warnings, 0 informations


```

## Outdated packages / installed packages:

```

pdm outdated:
╭──────────────────────────┬───────────┬─────────┬─────────╮
│ Package                  │ Installed │ Pinned  │ Latest  │
├──────────────────────────┼───────────┼─────────┼─────────┤
│ aiohttp                  │           │ 3.9.5   │ 3.9.5   │
│ aiosignal                │           │ 1.3.1   │ 1.3.1   │
│ cachetools               │           │ 5.3.3   │ 5.3.3   │
│ cffi                     │           │ 1.16.0  │ 1.16.0  │
│ colorlog                 │ 4.8.0     │         │ 6.8.2   │
│ curl-cffi                │           │ 0.6.3   │ 0.6.3   │
│ duckduckgo-search        │           │ 5.3.0   │ 5.3.0   │
│ fastapi                  │           │ 0.110.2 │ 0.110.3 │
│ frozenlist               │           │ 1.4.1   │ 1.4.1   │
│ google-api-core          │           │ 2.19.0  │ 2.19.0  │
│ google-api-python-client │           │ 2.127.0 │ 2.127.0 │
│ google-auth              │           │ 2.29.0  │ 2.29.0  │
│ google-auth-httplib2     │           │ 0.2.0   │ 0.2.0   │
│ googleapis-common-protos │           │ 1.63.0  │ 1.63.0  │
│ greenlet                 │           │ 3.0.3   │ 3.0.3   │
│ gunicorn                 │           │ 22.0.0  │ 22.0.0  │
│ httplib2                 │           │ 0.22.0  │ 0.22.0  │
│ langchain                │           │ 0.1.16  │ 0.1.17  │
│ langchain-community      │           │ 0.0.34  │ 0.0.36  │
│ langchain-text-splitters │           │ 0.0.1   │ 0.0.1   │
│ libica                   │ 0.7.0     │         │ 2.4.0   │
│ mando                    │ 0.6.4     │         │ 0.7.1   │
│ multidict                │           │ 6.0.5   │ 6.0.5   │
│ networkx                 │ 3.1       │         │ 3.3     │
│ numpy                    │           │ 1.26.4  │ 1.26.4  │
│ packaging                │ 23.2      │ 23.2    │ 24.0    │
│ proto-plus               │           │ 1.23.0  │ 1.23.0  │
│ protobuf                 │           │ 4.25.3  │ 5.26.1  │
│ pyasn1                   │           │ 0.6.0   │ 0.6.0   │
│ pyasn1-modules           │           │ 0.4.0   │ 0.4.0   │
│ pycparser                │           │ 2.22    │ 2.22    │
│ radon                    │ 5.1.0     │         │ 6.0.1   │
│ rsa                      │           │ 4.9     │ 4.9     │
│ sqlalchemy               │           │ 2.0.29  │ 2.0.29  │
│ sse-starlette            │           │ 1.8.2   │ 2.1.0   │
│ starlette                │           │ 0.37.2  │ 0.37.2  │
│ typeguard                │ 2.13.3    │         │ 4.2.1   │
│ typer                    │ 0.9.4     │         │ 0.12.3  │
│ uritemplate              │           │ 4.1.1   │ 4.1.1   │
│ uvicorn                  │           │ 0.29.0  │ 0.29.0  │
│ yarl                     │           │ 1.9.4   │ 1.9.4   │
╰──────────────────────────┴───────────┴─────────┴─────────╯
pdm list --include default
╭────────────────────┬──────────┬──────────╮
│ name               │ version  │ location │
├────────────────────┼──────────┼──────────┤
│ annotated-types    │ 0.6.0    │          │
│ anyio              │ 4.3.0    │          │
│ certifi            │ 2024.2.2 │          │
│ charset-normalizer │ 3.3.2    │          │
│ h11                │ 0.14.0   │          │
│ httpcore           │ 1.0.5    │          │
│ httpx              │ 0.27.0   │          │
│ idna               │ 3.7      │          │
│ jsonpatch          │ 1.33     │          │
│ jsonpointer        │ 2.4      │          │
│ langchain-core     │ 0.1.48   │          │
│ langsmith          │ 0.1.52   │          │
│ orjson             │ 3.10.2   │          │
│ packaging          │ 23.2     │          │
│ pydantic           │ 2.7.1    │          │
│ pydantic_core      │ 2.18.2   │          │
│ python-dotenv      │ 1.0.1    │          │
│ PyYAML             │ 6.0.1    │          │
│ requests           │ 2.31.0   │          │
│ sniffio            │ 1.3.1    │          │
│ tenacity           │ 8.2.3    │          │
│ typing_extensions  │ 4.11.0   │          │
│ urllib3            │ 2.2.1    │          │
╰────────────────────┴──────────┴──────────╯
httpx 0.27.0 [ required: ==0.27.0 ]
├── anyio 4.3.0 [ required: Any ]
│   ├── idna 3.7 [ required: >=2.8 ]
│   └── sniffio 1.3.1 [ required: >=1.1 ]
├── certifi 2024.2.2 [ required: Any ]
├── httpcore 1.0.5 [ required: ==1.* ]
│   ├── certifi 2024.2.2 [ required: Any ]
│   └── h11 0.14.0 [ required: <0.15,>=0.13 ]
├── idna 3.7 [ required: Any ]
└── sniffio 1.3.1 [ required: Any ]
langchain-core 0.1.48 [ required: ==0.1.45 ]
├── jsonpatch 1.33 [ required: <2.0,>=1.33 ]
│   └── jsonpointer 2.4 [ required: >=1.9 ]
├── langsmith 0.1.52 [ required: <0.2.0,>=0.1.0 ]
│   ├── orjson 3.10.2 [ required: <4.0.0,>=3.9.14 ]
│   ├── pydantic 2.7.1 [ required: <3,>=1 ]
│   │   ├── annotated-types 0.6.0 [ required: >=0.4.0 ]
│   │   ├── pydantic-core 2.18.2 [ required: ==2.18.2 ]
│   │   │   └── typing-extensions 4.11.0 [ required: !=4.7.0,>=4.6.0 ]
│   │   └── typing-extensions 4.11.0 [ required: >=4.6.1 ]
│   └── requests 2.31.0 [ required: <3,>=2 ]
│       ├── certifi 2024.2.2 [ required: >=2017.4.17 ]
│       ├── charset-normalizer 3.3.2 [ required: <4,>=2 ]
│       ├── idna 3.7 [ required: <4,>=2.5 ]
│       └── urllib3 2.2.1 [ required: <3,>=1.21.1 ]
├── packaging 23.2 [ required: <24.0,>=23.2 ]
├── pydantic 2.7.1 [ required: <3,>=1 ]
│   ├── annotated-types 0.6.0 [ required: >=0.4.0 ]
│   ├── pydantic-core 2.18.2 [ required: ==2.18.2 ]
│   │   └── typing-extensions 4.11.0 [ required: !=4.7.0,>=4.6.0 ]
│   └── typing-extensions 4.11.0 [ required: >=4.6.1 ]
├── pyyaml 6.0.1 [ required: >=5.3 ]
└── tenacity 8.2.3 [ required: <9.0.0,>=8.1.0 ]
python-dotenv 1.0.1 [ required: ==1.0.1 ]


```

## Licenses

| Name               | Version  | License                              | URL                                                        |
|--------------------|----------|--------------------------------------|------------------------------------------------------------|
| PyYAML             | 6.0.1    | MIT License                          | https://pyyaml.org/                                        |
| annotated-types    | 0.6.0    | MIT License                          | UNKNOWN                                                    |
| anyio              | 4.3.0    | MIT License                          | https://anyio.readthedocs.io/en/stable/versionhistory.html |
| certifi            | 2024.2.2 | Mozilla Public License 2.0 (MPL 2.0) | https://github.com/certifi/python-certifi                  |
| charset-normalizer | 3.3.2    | MIT License                          | https://github.com/Ousret/charset_normalizer               |
| h11                | 0.14.0   | MIT License                          | https://github.com/python-hyper/h11                        |
| httpcore           | 1.0.5    | BSD License                          | https://www.encode.io/httpcore/                            |
| httpx              | 0.27.0   | BSD License                          | https://github.com/encode/httpx                            |
| idna               | 3.7      | BSD License                          | https://github.com/kjd/idna                                |
| jsonpatch          | 1.33     | BSD License                          | https://github.com/stefankoegl/python-json-patch           |
| jsonpointer        | 2.4      | BSD License                          | https://github.com/stefankoegl/python-json-pointer         |
| langchain-core     | 0.1.48   | MIT License                          | https://github.com/langchain-ai/langchain                  |
| langsmith          | 0.1.52   | MIT License                          | https://smith.langchain.com/                               |
| orjson             | 3.10.2   | Apache Software License; MIT License | https://github.com/ijl/orjson                              |
| packaging          | 23.2     | Apache Software License; BSD License | https://github.com/pypa/packaging                          |
| pydantic           | 2.7.1    | MIT License                          | https://github.com/pydantic/pydantic                       |
| pydantic_core      | 2.18.2   | MIT License                          | https://github.com/pydantic/pydantic-core                  |
| python-dotenv      | 1.0.1    | BSD License                          | https://github.com/theskumar/python-dotenv                 |
| requests           | 2.31.0   | Apache Software License              | https://requests.readthedocs.io                            |
| sniffio            | 1.3.1    | Apache Software License; MIT License | https://github.com/python-trio/sniffio                     |
| tenacity           | 8.2.3    | Apache Software License              | https://github.com/jd/tenacity                             |
| typing_extensions  | 4.11.0   | Python Software Foundation License   | https://github.com/python/typing_extensions                |
| urllib3            | 2.2.1    | MIT License                          | https://github.com/urllib3/urllib3/blob/main/CHANGES.rst   |

## Radon maintainability metrics


```
radon mi -s app || true
app/server.py - A (100.00)
app/__init__.py - A (100.00)
app/routes/googlesearch/__init__.py - A (100.00)
app/routes/googlesearch/googlesearch_router.py - A (100.00)
app/routes/test_llm/test_llm_router.py - A (84.06)
app/routes/test_llm/__init__.py - A (95.23)
app/routes/duckduckgo/__init__.py - A (100.00)
app/routes/duckduckgo/duckduckgo_router.py - A (100.00)
app/routes/instagram/__init__.py - A (100.00)
app/routes/instagram/instagram_router.py - A (100.00)
app/routes/test/test_router.py - A (92.42)
app/routes/test/__init__.py - A (93.88)
app/routes/mermaid/__init__.py - A (100.00)
app/routes/mermaid/mermaid_router.py - A (100.00)
app/routes/qareact/__init__.py - A (100.00)
app/routes/qareact/qareact_router.py - A (87.24)
app/routes/health/health_router.py - A (100.00)
app/routes/health/__init__.py - A (100.00)
app/routes/gpt4vision/gpt4vision_router.py - A (100.00)
app/routes/gpt4vision/__init__.py - A (100.00)
app/routes/webex_summarizer/webex.py - A (80.86)
app/routes/webex_summarizer/__init__.py - A (95.23)
app/routes/webex_summarizer/webex_summarizer_router.py - A (87.14)
app/routes/geministt/test.py - A (100.00)
app/routes/geministt/geministt_router.py - A (100.00)
app/routes/geministt/__init__.py - A (100.00)
app/routes/wikipedia/config.py - A (100.00)
app/routes/wikipedia/__init__.py - A (93.88)
app/routes/wikipedia/wikipedia_router.py - A (100.00)
app/routes/wikipedia/wikipedia.py - A (78.06)
app/routes/time/__init__.py - A (100.00)
app/routes/time/time_router.py - A (100.00)
app/routes/time/tools/__init__.py - A (100.00)
app/routes/time/tools/system_time_tool.py - A (100.00)
app/routes/docbuilder/docbuilder_router.py - A (77.15)
app/routes/docbuilder/__init__.py - A (95.23)
app/routes/summarizer/__init__.py - A (100.00)
app/routes/summarizer/summarizer_router.py - A (100.00)
app/routes/jokes/__init__.py - A (100.00)
app/routes/jokes/jokes_router.py - A (100.00)
app/staging_routes/datagenerator/datagenerator_router.py - A (100.00)
app/staging_routes/datagenerator/__init__.py - A (95.23)
radon cc -s app || true
app/routes/googlesearch/googlesearch_router.py
    F 15:0 format_prompt - A (1)
    F 27:0 add_custom_routes - A (1)
app/routes/test_llm/test_llm_router.py
    F 17:0 add_custom_routes - A (1)
app/routes/duckduckgo/duckduckgo_router.py
    F 15:0 format_prompt - A (1)
    F 27:0 add_custom_routes - A (1)
app/routes/instagram/instagram_router.py
    F 14:0 add_custom_routes - A (1)
app/routes/test/test_router.py
    F 14:0 add_custom_routes - A (1)
app/routes/mermaid/mermaid_router.py
    F 23:0 get_text_between_markers - A (2)
    F 18:0 format_prompt - A (1)
    F 32:0 mm - A (1)
    F 45:0 add_custom_routes - A (1)
app/routes/qareact/qareact_router.py
    F 16:0 add_custom_routes - A (1)
app/routes/health/health_router.py
    F 7:0 add_custom_routes - A (1)
app/routes/gpt4vision/gpt4vision_router.py
    F 13:0 call_gpt4_vision_api - A (1)
    F 50:0 add_custom_routes - A (1)
app/routes/webex_summarizer/webex.py
    F 24:0 download_transcript - A (4)
    F 75:0 main - A (2)
    F 18:0 approximate_token_count - A (1)
    F 59:0 summarize_call - A (1)
app/routes/webex_summarizer/webex_summarizer_router.py
    F 27:0 add_custom_routes - A (1)
    C 20:0 WebexSummarizationRequest - A (1)
app/routes/geministt/test.py
    F 8:0 transcribe_audio_from_url - A (2)
app/routes/geministt/geministt_router.py
    F 13:0 add_custom_routes - A (1)
app/routes/wikipedia/config.py
    C 6:0 Settings - A (1)
app/routes/wikipedia/wikipedia_router.py
    F 22:0 add_custom_routes - A (1)
app/routes/wikipedia/wikipedia.py
    F 46:0 search_wikipedia - B (6)
    F 119:0 format_response - A (2)
    C 26:0 ResultsType - A (1)
    C 31:0 WikipediaSearchInput - A (1)
    C 41:0 ResponseItem - A (1)
app/routes/time/time_router.py
    F 14:0 format_prompt - A (1)
    F 26:0 add_custom_routes - A (1)
app/routes/time/tools/system_time_tool.py
    F 9:0 get_system_time - A (2)
app/routes/docbuilder/docbuilder_router.py
    F 23:0 clean_markdown_edge_quotes - A (1)
    F 48:0 add_custom_routes - A (1)
app/routes/summarizer/summarizer_router.py
    F 14:0 add_custom_routes - A (1)
app/routes/jokes/jokes_router.py
    F 13:0 add_custom_routes - A (1)
app/staging_routes/datagenerator/datagenerator_router.py
    F 24:0 add_custom_routes - A (1)
radon hal app || true
app/server.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/__init__.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/googlesearch/__init__.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/googlesearch/googlesearch_router.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/test_llm/test_llm_router.py:
    h1: 3
    h2: 6
    N1: 3
    N2: 6
    vocabulary: 9
    length: 9
    calculated_length: 20.264662506490406
    volume: 28.529325012980813
    difficulty: 1.5
    effort: 42.793987519471216
    time: 2.377443751081734
    bugs: 0.009509775004326938
app/routes/test_llm/__init__.py:
    h1: 1
    h2: 2
    N1: 1
    N2: 2
    vocabulary: 3
    length: 3
    calculated_length: 2.0
    volume: 4.754887502163469
    difficulty: 0.5
    effort: 2.3774437510817346
    time: 0.1320802083934297
    bugs: 0.0015849625007211565
app/routes/duckduckgo/__init__.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/duckduckgo/duckduckgo_router.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/instagram/__init__.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/instagram/instagram_router.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/test/test_router.py:
    h1: 1
    h2: 2
    N1: 1
    N2: 2
    vocabulary: 3
    length: 3
    calculated_length: 2.0
    volume: 4.754887502163469
    difficulty: 0.5
    effort: 2.3774437510817346
    time: 0.1320802083934297
    bugs: 0.0015849625007211565
app/routes/test/__init__.py:
    h1: 1
    h2: 2
    N1: 1
    N2: 2
    vocabulary: 3
    length: 3
    calculated_length: 2.0
    volume: 4.754887502163469
    difficulty: 0.5
    effort: 2.3774437510817346
    time: 0.1320802083934297
    bugs: 0.0015849625007211565
app/routes/mermaid/__init__.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/mermaid/mermaid_router.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/qareact/__init__.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/qareact/qareact_router.py:
    h1: 1
    h2: 2
    N1: 1
    N2: 2
    vocabulary: 3
    length: 3
    calculated_length: 2.0
    volume: 4.754887502163469
    difficulty: 0.5
    effort: 2.3774437510817346
    time: 0.1320802083934297
    bugs: 0.0015849625007211565
app/routes/health/health_router.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/health/__init__.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/gpt4vision/gpt4vision_router.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/gpt4vision/__init__.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/webex_summarizer/webex.py:
    h1: 2
    h2: 5
    N1: 4
    N2: 7
    vocabulary: 7
    length: 11
    calculated_length: 13.60964047443681
    volume: 30.880904142633646
    difficulty: 1.4
    effort: 43.2332657996871
    time: 2.401848099982617
    bugs: 0.010293634714211216
app/routes/webex_summarizer/__init__.py:
    h1: 1
    h2: 2
    N1: 1
    N2: 2
    vocabulary: 3
    length: 3
    calculated_length: 2.0
    volume: 4.754887502163469
    difficulty: 0.5
    effort: 2.3774437510817346
    time: 0.1320802083934297
    bugs: 0.0015849625007211565
app/routes/webex_summarizer/webex_summarizer_router.py:
    h1: 1
    h2: 1
    N1: 1
    N2: 1
    vocabulary: 2
    length: 2
    calculated_length: 0.0
    volume: 2.0
    difficulty: 0.5
    effort: 1.0
    time: 0.05555555555555555
    bugs: 0.0006666666666666666
app/routes/geministt/test.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/geministt/geministt_router.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/geministt/__init__.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/wikipedia/config.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/wikipedia/__init__.py:
    h1: 1
    h2: 2
    N1: 1
    N2: 2
    vocabulary: 3
    length: 3
    calculated_length: 2.0
    volume: 4.754887502163469
    difficulty: 0.5
    effort: 2.3774437510817346
    time: 0.1320802083934297
    bugs: 0.0015849625007211565
app/routes/wikipedia/wikipedia_router.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/wikipedia/wikipedia.py:
    h1: 4
    h2: 7
    N1: 4
    N2: 7
    vocabulary: 11
    length: 11
    calculated_length: 27.651484454403228
    volume: 38.053747805010275
    difficulty: 2.0
    effort: 76.10749561002055
    time: 4.228194200556697
    bugs: 0.012684582601670092
app/routes/time/__init__.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/time/time_router.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/time/tools/__init__.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/time/tools/system_time_tool.py:
    h1: 1
    h2: 2
    N1: 1
    N2: 2
    vocabulary: 3
    length: 3
    calculated_length: 2.0
    volume: 4.754887502163469
    difficulty: 0.5
    effort: 2.3774437510817346
    time: 0.1320802083934297
    bugs: 0.0015849625007211565
app/routes/docbuilder/docbuilder_router.py:
    h1: 2
    h2: 6
    N1: 4
    N2: 8
    vocabulary: 8
    length: 12
    calculated_length: 17.509775004326936
    volume: 36.0
    difficulty: 1.3333333333333333
    effort: 48.0
    time: 2.6666666666666665
    bugs: 0.012
app/routes/docbuilder/__init__.py:
    h1: 1
    h2: 2
    N1: 1
    N2: 2
    vocabulary: 3
    length: 3
    calculated_length: 2.0
    volume: 4.754887502163469
    difficulty: 0.5
    effort: 2.3774437510817346
    time: 0.1320802083934297
    bugs: 0.0015849625007211565
app/routes/summarizer/__init__.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/summarizer/summarizer_router.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/jokes/__init__.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/routes/jokes/jokes_router.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/staging_routes/datagenerator/datagenerator_router.py:
    h1: 0
    h2: 0
    N1: 0
    N2: 0
    vocabulary: 0
    length: 0
    calculated_length: 0
    volume: 0
    difficulty: 0
    effort: 0
    time: 0.0
    bugs: 0.0
app/staging_routes/datagenerator/__init__.py:
    h1: 1
    h2: 2
    N1: 1
    N2: 2
    vocabulary: 3
    length: 3
    calculated_length: 2.0
    volume: 4.754887502163469
    difficulty: 0.5
    effort: 2.3774437510817346
    time: 0.1320802083934297
    bugs: 0.0015849625007211565
radon raw -s app || true
app/server.py
    LOC: 51
    LLOC: 25
    SLOC: 36
    Comments: 7
    Single comments: 7
    Multi: 0
    Blank: 8
    - Comment Stats
        (C % L): 14%
        (C % S): 19%
        (C + M % L): 14%
app/__init__.py
    LOC: 0
    LLOC: 0
    SLOC: 0
    Comments: 0
    Single comments: 0
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 0%
app/routes/googlesearch/__init__.py
    LOC: 2
    LLOC: 1
    SLOC: 1
    Comments: 1
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 50%
        (C % S): 100%
        (C + M % L): 50%
app/routes/googlesearch/googlesearch_router.py
    LOC: 68
    LLOC: 29
    SLOC: 41
    Comments: 11
    Single comments: 11
    Multi: 0
    Blank: 16
    - Comment Stats
        (C % L): 16%
        (C % S): 27%
        (C + M % L): 16%
app/routes/test_llm/test_llm_router.py
    LOC: 55
    LLOC: 32
    SLOC: 33
    Comments: 7
    Single comments: 6
    Multi: 4
    Blank: 12
    - Comment Stats
        (C % L): 13%
        (C % S): 21%
        (C + M % L): 20%
app/routes/test_llm/__init__.py
    LOC: 31
    LLOC: 16
    SLOC: 20
    Comments: 2
    Single comments: 2
    Multi: 4
    Blank: 5
    - Comment Stats
        (C % L): 6%
        (C % S): 10%
        (C + M % L): 19%
app/routes/duckduckgo/__init__.py
    LOC: 2
    LLOC: 1
    SLOC: 1
    Comments: 1
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 50%
        (C % S): 100%
        (C + M % L): 50%
app/routes/duckduckgo/duckduckgo_router.py
    LOC: 67
    LLOC: 29
    SLOC: 41
    Comments: 10
    Single comments: 10
    Multi: 0
    Blank: 16
    - Comment Stats
        (C % L): 15%
        (C % S): 24%
        (C + M % L): 15%
app/routes/instagram/__init__.py
    LOC: 2
    LLOC: 1
    SLOC: 1
    Comments: 1
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 50%
        (C % S): 100%
        (C + M % L): 50%
app/routes/instagram/instagram_router.py
    LOC: 61
    LLOC: 30
    SLOC: 42
    Comments: 9
    Single comments: 9
    Multi: 0
    Blank: 10
    - Comment Stats
        (C % L): 15%
        (C % S): 21%
        (C + M % L): 15%
app/routes/test/test_router.py
    LOC: 48
    LLOC: 25
    SLOC: 30
    Comments: 7
    Single comments: 6
    Multi: 4
    Blank: 8
    - Comment Stats
        (C % L): 15%
        (C % S): 23%
        (C + M % L): 23%
app/routes/test/__init__.py
    LOC: 30
    LLOC: 16
    SLOC: 20
    Comments: 2
    Single comments: 2
    Multi: 3
    Blank: 5
    - Comment Stats
        (C % L): 7%
        (C % S): 10%
        (C + M % L): 17%
app/routes/mermaid/__init__.py
    LOC: 2
    LLOC: 1
    SLOC: 1
    Comments: 1
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 50%
        (C % S): 100%
        (C + M % L): 50%
app/routes/mermaid/mermaid_router.py
    LOC: 191
    LLOC: 88
    SLOC: 122
    Comments: 32
    Single comments: 32
    Multi: 0
    Blank: 37
    - Comment Stats
        (C % L): 17%
        (C % S): 26%
        (C + M % L): 17%
app/routes/qareact/__init__.py
    LOC: 2
    LLOC: 1
    SLOC: 1
    Comments: 1
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 50%
        (C % S): 100%
        (C + M % L): 50%
app/routes/qareact/qareact_router.py
    LOC: 96
    LLOC: 34
    SLOC: 61
    Comments: 16
    Single comments: 16
    Multi: 0
    Blank: 19
    - Comment Stats
        (C % L): 17%
        (C % S): 26%
        (C + M % L): 17%
app/routes/health/health_router.py
    LOC: 10
    LLOC: 6
    SLOC: 6
    Comments: 1
    Single comments: 1
    Multi: 0
    Blank: 3
    - Comment Stats
        (C % L): 10%
        (C % S): 17%
        (C + M % L): 10%
app/routes/health/__init__.py
    LOC: 2
    LLOC: 1
    SLOC: 1
    Comments: 1
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 50%
        (C % S): 100%
        (C + M % L): 50%
app/routes/gpt4vision/gpt4vision_router.py
    LOC: 79
    LLOC: 31
    SLOC: 51
    Comments: 13
    Single comments: 12
    Multi: 0
    Blank: 16
    - Comment Stats
        (C % L): 16%
        (C % S): 25%
        (C + M % L): 16%
app/routes/gpt4vision/__init__.py
    LOC: 2
    LLOC: 1
    SLOC: 1
    Comments: 1
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 50%
        (C % S): 100%
        (C + M % L): 50%
app/routes/webex_summarizer/webex.py
    LOC: 88
    LLOC: 50
    SLOC: 46
    Comments: 5
    Single comments: 4
    Multi: 19
    Blank: 19
    - Comment Stats
        (C % L): 6%
        (C % S): 11%
        (C + M % L): 27%
app/routes/webex_summarizer/__init__.py
    LOC: 31
    LLOC: 16
    SLOC: 20
    Comments: 2
    Single comments: 2
    Multi: 4
    Blank: 5
    - Comment Stats
        (C % L): 6%
        (C % S): 10%
        (C + M % L): 19%
app/routes/webex_summarizer/webex_summarizer_router.py
    LOC: 60
    LLOC: 37
    SLOC: 39
    Comments: 4
    Single comments: 3
    Multi: 4
    Blank: 14
    - Comment Stats
        (C % L): 7%
        (C % S): 10%
        (C + M % L): 13%
app/routes/geministt/test.py
    LOC: 41
    LLOC: 16
    SLOC: 24
    Comments: 6
    Single comments: 6
    Multi: 0
    Blank: 11
    - Comment Stats
        (C % L): 15%
        (C % S): 25%
        (C + M % L): 15%
app/routes/geministt/geministt_router.py
    LOC: 37
    LLOC: 12
    SLOC: 17
    Comments: 13
    Single comments: 12
    Multi: 0
    Blank: 8
    - Comment Stats
        (C % L): 35%
        (C % S): 76%
        (C + M % L): 35%
app/routes/geministt/__init__.py
    LOC: 2
    LLOC: 1
    SLOC: 1
    Comments: 1
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 50%
        (C % S): 100%
        (C + M % L): 50%
app/routes/wikipedia/config.py
    LOC: 23
    LLOC: 18
    SLOC: 12
    Comments: 4
    Single comments: 4
    Multi: 0
    Blank: 7
    - Comment Stats
        (C % L): 17%
        (C % S): 33%
        (C + M % L): 17%
app/routes/wikipedia/__init__.py
    LOC: 30
    LLOC: 16
    SLOC: 20
    Comments: 2
    Single comments: 2
    Multi: 3
    Blank: 5
    - Comment Stats
        (C % L): 7%
        (C % S): 10%
        (C + M % L): 17%
app/routes/wikipedia/wikipedia_router.py
    LOC: 53
    LLOC: 33
    SLOC: 35
    Comments: 6
    Single comments: 4
    Multi: 4
    Blank: 10
    - Comment Stats
        (C % L): 11%
        (C % S): 17%
        (C + M % L): 19%
app/routes/wikipedia/wikipedia.py
    LOC: 136
    LLOC: 62
    SLOC: 67
    Comments: 6
    Single comments: 5
    Multi: 36
    Blank: 28
    - Comment Stats
        (C % L): 4%
        (C % S): 9%
        (C + M % L): 31%
app/routes/time/__init__.py
    LOC: 2
    LLOC: 1
    SLOC: 1
    Comments: 1
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 50%
        (C % S): 100%
        (C + M % L): 50%
app/routes/time/time_router.py
    LOC: 88
    LLOC: 38
    SLOC: 49
    Comments: 16
    Single comments: 16
    Multi: 0
    Blank: 23
    - Comment Stats
        (C % L): 18%
        (C % S): 33%
        (C + M % L): 18%
app/routes/time/tools/__init__.py
    LOC: 0
    LLOC: 0
    SLOC: 0
    Comments: 0
    Single comments: 0
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 0%
app/routes/time/tools/system_time_tool.py
    LOC: 21
    LLOC: 10
    SLOC: 9
    Comments: 5
    Single comments: 6
    Multi: 0
    Blank: 6
    - Comment Stats
        (C % L): 24%
        (C % S): 56%
        (C + M % L): 24%
app/routes/docbuilder/docbuilder_router.py
    LOC: 172
    LLOC: 62
    SLOC: 98
    Comments: 22
    Single comments: 21
    Multi: 11
    Blank: 42
    - Comment Stats
        (C % L): 13%
        (C % S): 22%
        (C + M % L): 19%
app/routes/docbuilder/__init__.py
    LOC: 31
    LLOC: 16
    SLOC: 20
    Comments: 2
    Single comments: 2
    Multi: 4
    Blank: 5
    - Comment Stats
        (C % L): 6%
        (C % S): 10%
        (C + M % L): 19%
app/routes/summarizer/__init__.py
    LOC: 2
    LLOC: 1
    SLOC: 1
    Comments: 1
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 50%
        (C % S): 100%
        (C + M % L): 50%
app/routes/summarizer/summarizer_router.py
    LOC: 48
    LLOC: 27
    SLOC: 30
    Comments: 8
    Single comments: 8
    Multi: 0
    Blank: 10
    - Comment Stats
        (C % L): 17%
        (C % S): 27%
        (C + M % L): 17%
app/routes/jokes/__init__.py
    LOC: 2
    LLOC: 1
    SLOC: 1
    Comments: 1
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 50%
        (C % S): 100%
        (C + M % L): 50%
app/routes/jokes/jokes_router.py
    LOC: 35
    LLOC: 18
    SLOC: 21
    Comments: 6
    Single comments: 6
    Multi: 0
    Blank: 8
    - Comment Stats
        (C % L): 17%
        (C % S): 29%
        (C + M % L): 17%
app/staging_routes/datagenerator/datagenerator_router.py
    LOC: 93
    LLOC: 51
    SLOC: 61
    Comments: 10
    Single comments: 9
    Multi: 5
    Blank: 18
    - Comment Stats
        (C % L): 11%
        (C % S): 16%
        (C + M % L): 16%
app/staging_routes/datagenerator/__init__.py
    LOC: 31
    LLOC: 16
    SLOC: 20
    Comments: 2
    Single comments: 2
    Multi: 4
    Blank: 5
    - Comment Stats
        (C % L): 6%
        (C % S): 10%
        (C + M % L): 19%
** Total **
    LOC: 1827
    LLOC: 870
    SLOC: 1102
    Comments: 247
    Single comments: 237
    Multi: 109
    Blank: 379
    - Comment Stats
        (C % L): 14%
        (C % S): 22%
        (C + M % L): 19%

```


## Pyroma package checker


```
------------------------------
Checking .
Getting metadata for wheel...
Creating isolated environment: venv+pip...
Installing packages in isolated environment:
- pdm-backend
Getting build dependencies for wheel...
Getting metadata for wheel...
Found ica_integrations_host
------------------------------
The classifiers should specify what minor versions of Python you support as well as what major version.
Specifying a development status in the classifiers gives users a hint of how stable your software is.
------------------------------
Final rating: 9/10
Cottage Cheese
------------------------------

```


## Pyre check


```

```


## Spellcheck


```
make[1]: Entering directory '/home/cmihai/production/ica_integrations_host'
pyspelling
Spelling check passed :)
make[1]: Leaving directory '/home/cmihai/production/ica_integrations_host'

```


## Importchecker


```
make[1]: Entering directory '/home/cmihai/production/ica_integrations_host'
app/routes/docbuilder/__init__.py:20: add_custom_routes
app/routes/docbuilder/docbuilder_router.py:15: StaticFiles
app/routes/duckduckgo/__init__.py:2: add_custom_routes
app/routes/duckduckgo/duckduckgo_router.py:3: sys
app/routes/duckduckgo/duckduckgo_router.py:4: Path
app/routes/geministt/__init__.py:2: add_custom_routes
app/routes/geministt/geministt_router.py:2: sys
app/routes/geministt/geministt_router.py:3: Path
app/routes/geministt/geministt_router.py:6: LLMChain
app/routes/geministt/geministt_router.py:7: ChatPromptTemplate
app/routes/geministt/geministt_router.py:10: ChatConsultingAssistants
app/routes/googlesearch/__init__.py:2: add_custom_routes
app/routes/googlesearch/googlesearch_router.py:3: sys
app/routes/googlesearch/googlesearch_router.py:4: Path
app/routes/gpt4vision/__init__.py:2: add_custom_routes
app/routes/gpt4vision/gpt4vision_router.py:3: sys
app/routes/gpt4vision/gpt4vision_router.py:4: Path
app/routes/gpt4vision/gpt4vision_router.py:8: LLMChain
app/routes/gpt4vision/gpt4vision_router.py:9: PromptTemplate
app/routes/gpt4vision/gpt4vision_router.py:10: GoogleSearchAPIWrapper
app/routes/health/__init__.py:2: add_custom_routes
app/routes/health/health_router.py:2: json
app/routes/instagram/__init__.py:2: add_custom_routes
app/routes/instagram/instagram_router.py:3: sys
app/routes/instagram/instagram_router.py:4: Path
app/routes/jokes/__init__.py:2: add_custom_routes
app/routes/jokes/jokes_router.py:2: sys
app/routes/jokes/jokes_router.py:3: Path
app/routes/mermaid/__init__.py:2: add_custom_routes
app/routes/mermaid/mermaid_router.py:3: os
app/routes/mermaid/mermaid_router.py:5: sys
app/routes/mermaid/mermaid_router.py:6: Path
app/routes/mermaid/mermaid_router.py:8: requests
app/routes/mermaid/mermaid_router.py:12: GoogleSearchAPIWrapper
app/routes/qareact/__init__.py:2: add_custom_routes
app/routes/qareact/qareact_router.py:2: sys
app/routes/qareact/qareact_router.py:3: Path
app/routes/qareact/qareact_router.py:7: LLMChain
app/routes/summarizer/__init__.py:2: add_custom_routes
app/routes/summarizer/summarizer_router.py:3: sys
app/routes/summarizer/summarizer_router.py:4: Path
app/routes/test/__init__.py:19: add_custom_routes
app/routes/test_llm/__init__.py:20: add_custom_routes
app/routes/time/__init__.py:2: add_custom_routes
app/routes/webex_summarizer/__init__.py:20: add_custom_routes
app/routes/webex_summarizer/webex_summarizer_router.py:7: json
app/routes/webex_summarizer/webex_summarizer_router.py:12: ICAClient
app/routes/wikipedia/__init__.py:19: add_custom_routes
app/routes/wikipedia/wikipedia.py:8: os
app/routes/wikipedia/wikipedia.py:9: sys
app/routes/wikipedia/wikipedia.py:11: List
app/routes/wikipedia/wikipedia_router.py:12: ICAClient
app/server.py:3: sys
app/staging_routes/datagenerator/__init__.py:20: add_custom_routes
app/staging_routes/datagenerator/datagenerator_router.py:17: ICAClient
make[1]: Leaving directory '/home/cmihai/production/ica_integrations_host'

```


## Pytype


```
pytype --keep-going app/ || true
ninja: Entering directory `.pytype'
[1/40] infer time.time_router
[2/40] check time.__init__
[3/40] check time.time_router
FAILED: /home/cmihai/production/ica_integrations_host/.pytype/pyi/time/time_router.pyi
/home/cmihai/.venv/consulting_assistants_api/bin/python3 -m pytype.main --imports_info /home/cmihai/production/ica_integrations_host/.pytype/imports/time.time_router.imports --module-name time.time_router --platform linux -V 3.11 -o /home/cmihai/production/ica_integrations_host/.pytype/pyi/time/time_router.pyi --analyze-annotated --nofail --quick /home/cmihai/production/ica_integrations_host/app/routes/time/time_router.py
File "/home/cmihai/production/ica_integrations_host/app/routes/time/time_router.py", line 4, in <module>: Can't find module 'fastapi'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/time/time_router.py", line 5, in <module>: Can't find module 'langchain.chains'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/time/time_router.py", line 6, in <module>: Can't find module 'langchain.prompts'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/time/time_router.py", line 11, in <module>: Couldn't import pyi for 'tools.system_time_tool' [pyi-error]
  No struct_time in module time, referenced from 'datetime'

For more details, see https://google.github.io/pytype/errors.html
[4/40] check summarizer.summarizer_router
FAILED: /home/cmihai/production/ica_integrations_host/.pytype/pyi/summarizer/summarizer_router.pyi
/home/cmihai/.venv/consulting_assistants_api/bin/python3 -m pytype.main --imports_info /home/cmihai/production/ica_integrations_host/.pytype/imports/summarizer.summarizer_router.imports --module-name summarizer.summarizer_router --platform linux -V 3.11 -o /home/cmihai/production/ica_integrations_host/.pytype/pyi/summarizer/summarizer_router.pyi --analyze-annotated --nofail --quick /home/cmihai/production/ica_integrations_host/app/routes/summarizer/summarizer_router.py
File "/home/cmihai/production/ica_integrations_host/app/routes/summarizer/summarizer_router.py", line 6, in <module>: Can't find module 'fastapi'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/summarizer/summarizer_router.py", line 7, in <module>: Can't find module 'langchain.chains'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/summarizer/summarizer_router.py", line 8, in <module>: Can't find module 'langchain.prompts'. [import-error]

For more details, see https://google.github.io/pytype/errors.html#import-error
[5/40] check geministt.geministt_router
FAILED: /home/cmihai/production/ica_integrations_host/.pytype/pyi/geministt/geministt_router.pyi
/home/cmihai/.venv/consulting_assistants_api/bin/python3 -m pytype.main --imports_info /home/cmihai/production/ica_integrations_host/.pytype/imports/geministt.geministt_router.imports --module-name geministt.geministt_router --platform linux -V 3.11 -o /home/cmihai/production/ica_integrations_host/.pytype/pyi/geministt/geministt_router.pyi --analyze-annotated --nofail --quick /home/cmihai/production/ica_integrations_host/app/routes/geministt/geministt_router.py
File "/home/cmihai/production/ica_integrations_host/app/routes/geministt/geministt_router.py", line 5, in <module>: Can't find module 'fastapi'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/geministt/geministt_router.py", line 6, in <module>: Can't find module 'langchain.chains'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/geministt/geministt_router.py", line 7, in <module>: Can't find module 'langchain.prompts'. [import-error]

For more details, see https://google.github.io/pytype/errors.html#import-error
[6/40] check health.health_router
FAILED: /home/cmihai/production/ica_integrations_host/.pytype/pyi/health/health_router.pyi
/home/cmihai/.venv/consulting_assistants_api/bin/python3 -m pytype.main --imports_info /home/cmihai/production/ica_integrations_host/.pytype/imports/health.health_router.imports --module-name health.health_router --platform linux -V 3.11 -o /home/cmihai/production/ica_integrations_host/.pytype/pyi/health/health_router.pyi --analyze-annotated --nofail --quick /home/cmihai/production/ica_integrations_host/app/routes/health/health_router.py
File "/home/cmihai/production/ica_integrations_host/app/routes/health/health_router.py", line 4, in <module>: Can't find module 'fastapi'. [import-error]

For more details, see https://google.github.io/pytype/errors.html#import-error
[7/40] check instagram.instagram_router
FAILED: /home/cmihai/production/ica_integrations_host/.pytype/pyi/instagram/instagram_router.pyi
/home/cmihai/.venv/consulting_assistants_api/bin/python3 -m pytype.main --imports_info /home/cmihai/production/ica_integrations_host/.pytype/imports/instagram.instagram_router.imports --module-name instagram.instagram_router --platform linux -V 3.11 -o /home/cmihai/production/ica_integrations_host/.pytype/pyi/instagram/instagram_router.pyi --analyze-annotated --nofail --quick /home/cmihai/production/ica_integrations_host/app/routes/instagram/instagram_router.py
File "/home/cmihai/production/ica_integrations_host/app/routes/instagram/instagram_router.py", line 6, in <module>: Can't find module 'fastapi'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/instagram/instagram_router.py", line 7, in <module>: Can't find module 'langchain.chains'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/instagram/instagram_router.py", line 8, in <module>: Can't find module 'langchain.prompts'. [import-error]

For more details, see https://google.github.io/pytype/errors.html#import-error
[8/40] check qareact.qareact_router
FAILED: /home/cmihai/production/ica_integrations_host/.pytype/pyi/qareact/qareact_router.pyi
/home/cmihai/.venv/consulting_assistants_api/bin/python3 -m pytype.main --imports_info /home/cmihai/production/ica_integrations_host/.pytype/imports/qareact.qareact_router.imports --module-name qareact.qareact_router --platform linux -V 3.11 -o /home/cmihai/production/ica_integrations_host/.pytype/pyi/qareact/qareact_router.pyi --analyze-annotated --nofail --quick /home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py
File "/home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py", line 5, in <module>: Can't find module 'fastapi'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py", line 6, in <module>: Can't find module 'langchain.agents'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py", line 7, in <module>: Can't find module 'langchain.chains'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py", line 8, in <module>: Can't find module 'langchain.prompts'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py", line 9, in <module>: Can't find module 'langchain.tools'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py", line 10, in <module>: Can't find module 'langchain_community.utilities'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/qareact/qareact_router.py", line 87, in qareact: Name 'raw_result' is not defined [name-error]

For more details, see https://google.github.io/pytype/errors.html
[9/40] check jokes.jokes_router
FAILED: /home/cmihai/production/ica_integrations_host/.pytype/pyi/jokes/jokes_router.pyi
/home/cmihai/.venv/consulting_assistants_api/bin/python3 -m pytype.main --imports_info /home/cmihai/production/ica_integrations_host/.pytype/imports/jokes.jokes_router.imports --module-name jokes.jokes_router --platform linux -V 3.11 -o /home/cmihai/production/ica_integrations_host/.pytype/pyi/jokes/jokes_router.pyi --analyze-annotated --nofail --quick /home/cmihai/production/ica_integrations_host/app/routes/jokes/jokes_router.py
File "/home/cmihai/production/ica_integrations_host/app/routes/jokes/jokes_router.py", line 5, in <module>: Can't find module 'fastapi'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/jokes/jokes_router.py", line 6, in <module>: Can't find module 'langchain.chains'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/routes/jokes/jokes_router.py", line 7, in <module>: Can't find module 'langchain.prompts'. [import-error]

For more details, see https://google.github.io/pytype/errors.html#import-error
[10/40] check app.server
FAILED: /home/cmihai/production/ica_integrations_host/.pytype/pyi/app/server.pyi
/home/cmihai/.venv/consulting_assistants_api/bin/python3 -m pytype.main --imports_info /home/cmihai/production/ica_integrations_host/.pytype/imports/app.server.imports --module-name app.server --platform linux -V 3.11 -o /home/cmihai/production/ica_integrations_host/.pytype/pyi/app/server.pyi --analyze-annotated --nofail --quick /home/cmihai/production/ica_integrations_host/app/server.py
File "/home/cmihai/production/ica_integrations_host/app/server.py", line 8, in <module>: Can't find module 'fastapi'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/server.py", line 9, in <module>: Can't find module 'fastapi.middleware.cors'. [import-error]
File "/home/cmihai/production/ica_integrations_host/app/server.py", line 10, in <module>: Can't find module 'fastapi.staticfiles'. [import-error]

For more details, see https://google.github.io/pytype/errors.html#import-error
ninja: build stopped: cannot make progress due to previous errors.
Computing dependencies
Analyzing 42 sources with 0 local dependencies
Leaving directory '.pytype'

```
