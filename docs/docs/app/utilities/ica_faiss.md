# ICAFaiss

[ica_integrations_host Index](../../README.md#ica_integrations_host-index) / [App](../index.md#app) / [Utilities](./index.md#utilities) / ICAFaiss

> Auto-generated documentation for [app.utilities.ica_faiss](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/utilities/ica_faiss.py) module.

- [ICAFaiss](#icafaiss)
  - [ICAFaiss](#icafaiss-1)
    - [ICAFaiss()._create_faiss_index](#icafaiss()_create_faiss_index)
    - [ICAFaiss()._extract_text](#icafaiss()_extract_text)
    - [ICAFaiss()._extract_text_from_pdf](#icafaiss()_extract_text_from_pdf)
    - [ICAFaiss()._extract_text_from_txt](#icafaiss()_extract_text_from_txt)
    - [ICAFaiss().query](#icafaiss()query)

## ICAFaiss

[Show source in ica_faiss.py:18](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/utilities/ica_faiss.py#L18)

A chatbot library that uses documents from various formats (PDF, plain text, etc.) to answer queries.
It utilizes DPR for encoding text and FAISS for efficient similarity search.

#### Attributes

- `tokenizer` *DPRContextEncoderTokenizer* - DPR context encoder tokenizer.
- `model` *DPRContextEncoder* - DPR context encoder model.
- `max_length` *int* - Maximum length of tokens for each document.
- `documents` *list* - List of documents.
- `index` *faiss.swigfaiss.Index* - FAISS index for efficient retrieval.

#### Examples

```python
>>> chatbot = ICAFaiss('test.pdf')
>>> query = "What was the 2023 performance."
>>> responses = chatbot.query(query)
>>> print("Top Responses:")
>>> for i, response in enumerate(responses, 1):
>>>     print(f"{i}: {response}")
```

#### Signature

```python
class ICAFaiss:
    def __init__(
        self,
        file_path: str,
        model_name: str = "facebook/dpr-ctx_encoder-single-nq-base",
        max_length: int = 512,
    ): ...
```

### ICAFaiss()._create_faiss_index

[Show source in ica_faiss.py:101](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/utilities/ica_faiss.py#L101)

Encodes the documents and creates a FAISS index for efficient retrieval.

#### Returns

- `faiss.swigfaiss.Index` - A FAISS index of the encoded documents.

#### Signature

```python
def _create_faiss_index(self): ...
```

### ICAFaiss()._extract_text

[Show source in ica_faiss.py:55](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/utilities/ica_faiss.py#L55)

Determines the file type and extracts text accordingly.

#### Arguments

- [file_path](#icafaiss) *str* - Path to the document file.

#### Returns

List of text extracted from the document.

#### Signature

```python
def _extract_text(self, file_path: str) -> list: ...
```

### ICAFaiss()._extract_text_from_pdf

[Show source in ica_faiss.py:73](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/utilities/ica_faiss.py#L73)

Extracts text from a PDF file.

#### Arguments

- `pdf_path` *str* - Path to the PDF file.

#### Returns

List of text extracted from each page of the PDF.

#### Signature

```python
def _extract_text_from_pdf(self, pdf_path: str) -> list: ...
```

### ICAFaiss()._extract_text_from_txt

[Show source in ica_faiss.py:87](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/utilities/ica_faiss.py#L87)

Extracts text from a plain text file.

#### Arguments

- `txt_path` *str* - Path to the plain text file.

#### Returns

List containing the entire content of the text file in a single element.

#### Signature

```python
def _extract_text_from_txt(self, txt_path: str) -> list: ...
```

### ICAFaiss().query

[Show source in ica_faiss.py:119](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/utilities/ica_faiss.py#L119)

Retrieves the top k documents most relevant to the query.

#### Arguments

- `query_text` *str* - The query text.
- `top_k` *int, optional* - The number of top documents to retrieve. Default is 10.

#### Returns

List of the top k documents ranked by relevance.

#### Signature

```python
def query(self, query_text: str, top_k: int = 10) -> list: ...
```
