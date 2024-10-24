# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: RAG with FAISS
"""

import os

import faiss
import fitz
import numpy as np
from transformers import DPRContextEncoder, DPRContextEncoderTokenizer

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class ICAFaiss:
    """
    A chatbot library that uses documents from various formats (PDF, plain text, etc.) to answer queries.
    It utilizes DPR for encoding text and FAISS for efficient similarity search.

    Attributes:
        tokenizer (DPRContextEncoderTokenizer): DPR context encoder tokenizer.
        model (DPRContextEncoder): DPR context encoder model.
        max_length (int): Maximum length of tokens for each document.
        documents (list): List of documents.
        index (faiss.swigfaiss.Index): FAISS index for efficient retrieval.

    Example:
        >>> chatbot = ICAFaiss('test.pdf')
        >>> query = "What was the 2023 performance."
        >>> responses = chatbot.query(query)
        >>> print("Top Responses:")
        >>> for i, response in enumerate(responses, 1):
        >>>     print(f"{i}: {response}")
    """

    def __init__(
        self,
        file_path: str,
        model_name: str = "facebook/dpr-ctx_encoder-single-nq-base",
        max_length: int = 512,
    ):
        """
        init__(self, file_path: str, model_name: str = 'facebook/dpr-ctx_encoder-single-nq-base', max_length: int = 512):
                Initializes the chatbot with a given document file path.

                Args:
                    file_path (str): Path to the document file to be used as the knowledge base.
                    model_name (str, optional): The model to be used for encoding the documents. Default is 'facebook/dpr-ctx_encoder-single-nq-base'.
                    max_length (int, optional): Maximum length of tokens for each document. Default is 512.
        """
        self.tokenizer = DPRContextEncoderTokenizer.from_pretrained(model_name)
        self.model = DPRContextEncoder.from_pretrained(model_name)
        self.max_length = max_length
        self.documents = self._extract_text(file_path)
        self.index = self._create_faiss_index()

    def _extract_text(self, file_path: str) -> list:
        """
        Determines the file type and extracts text accordingly.

        Args:
            file_path (str): Path to the document file.

        Returns:
            List of text extracted from the document.
        """
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() == ".pdf":
            return self._extract_text_from_pdf(file_path)
        elif file_extension.lower() == ".txt":
            return self._extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    def _extract_text_from_pdf(self, pdf_path: str) -> list:
        """
        Extracts text from a PDF file.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            List of text extracted from each page of the PDF.
        """
        doc = fitz.open(pdf_path)
        texts = [page.get_text() for page in doc]
        return texts

    def _extract_text_from_txt(self, txt_path: str) -> list:
        """
        Extracts text from a plain text file.

        Args:
            txt_path (str): Path to the plain text file.

        Returns:
            List containing the entire content of the text file in a single element.
        """
        with open(txt_path, "r", encoding="utf-8") as file:
            texts = [file.read()]
        return texts

    def _create_faiss_index(self):
        """
        Encodes the documents and creates a FAISS index for efficient retrieval.

        Returns:
            faiss.swigfaiss.Index: A FAISS index of the encoded documents.
        """
        document_embeddings = []
        for doc in self.documents:
            encoded_input = self.tokenizer(doc, return_tensors="pt", max_length=self.max_length, truncation=True)
            embeddings = self.model(**encoded_input).pooler_output
            document_embeddings.append(embeddings.detach().numpy())
        document_embeddings = np.vstack(document_embeddings)

        index = faiss.IndexFlatL2(document_embeddings.shape[1])
        index.add(document_embeddings)
        return index

    def query(self, query_text: str, top_k: int = 10) -> list:
        """
        Retrieves the top k documents most relevant to the query.

        Args:
            query_text (str): The query text.
            top_k (int, optional): The number of top documents to retrieve. Default is 10.

        Returns:
            List of the top k documents ranked by relevance.
        """
        query_encoded = self.tokenizer(query_text, return_tensors="pt")
        query_embedding = self.model(**query_encoded).pooler_output.detach().numpy()

        _, indices = self.index.search(query_embedding, top_k)
        return [self.documents[i] for i in indices[0]]


# Example usage
if __name__ == "__main__":
    file_path = "ibm-results.pdf"  # This can be a PDF or a plain text file
    chatbot = PDFChatbot(file_path)
    query = "What was the 2023 IBM performance."
    responses = chatbot.query(query)

    print("Top Responses:")
    for i, response in enumerate(responses, 1):
        print(f"{i}: {response}")
