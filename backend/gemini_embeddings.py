import numpy as np
import os
from typing import List, Dict, Any
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure Gemini API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"[OK] Gemini API configured with key: {GEMINI_API_KEY[:20]}...")
else:
    print("[ERROR] GEMINI_API_KEY not found in environment variables")

class GeminiEmbeddings:
    def __init__(self):
        self.model_name = "models/text-embedding-004"
        self.embedding_dimension = 768  # Gemini text-embedding-004 outputs 768-dimensional embeddings

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Gemini Text Embeddings API"""
        try:
            if not texts:
                print("[ERROR] No texts provided for embedding generation")
                return []

            if not GEMINI_API_KEY:
                print("[ERROR] Gemini API key not configured, using fallback")
                return self._fallback_embeddings(texts)

            print(f"[PROCESSING] Generating Gemini embeddings for {len(texts)} texts...")

            # Generate embeddings for all texts
            embeddings = []
            for i, text in enumerate(texts):
                try:
                    # Gemini API call for embedding
                    result = genai.embed_content(
                        model=self.model_name,
                        content=text,
                        task_type="retrieval_document"  # For document embeddings
                    )

                    embedding = result['embedding']
                    embeddings.append(embedding)

                    if (i + 1) % 10 == 0:
                        print(f"  [OK] Generated {i + 1}/{len(texts)} embeddings")

                except Exception as e:
                    print(f"[ERROR] Error generating embedding for text {i}: {e}")
                    # Use zero vector as fallback for this text
                    embeddings.append([0.0] * self.embedding_dimension)

            print(f"[OK] Successfully generated {len(embeddings)} Gemini embeddings with dimension {self.embedding_dimension}")

            return embeddings

        except Exception as e:
            print(f"[ERROR] Gemini embedding error: {e}")
            # Fallback to simple embeddings
            return self._fallback_embeddings(texts)

    def get_query_embedding(self, query: str) -> List[float]:
        """Get embedding for a single query"""
        try:
            if not query:
                print("[ERROR] Empty query provided")
                return [0.0] * self.embedding_dimension

            if not GEMINI_API_KEY:
                print("[ERROR] Gemini API key not configured, using fallback")
                return self._fallback_embeddings([query])[0]

            print(f"[PROCESSING] Generating Gemini query embedding...")

            # Gemini API call for query embedding
            result = genai.embed_content(
                model=self.model_name,
                content=query,
                task_type="retrieval_query"  # For query embeddings
            )

            embedding = result['embedding']

            print(f"[OK] Generated query embedding with dimension {len(embedding)}")

            return embedding

        except Exception as e:
            print(f"[ERROR] Error generating query embedding: {e}")
            return self._fallback_embeddings([query])[0]

    def find_relevant_chunks(self, query: str, document_chunks: List[str],
                           document_embeddings: List[List[float]], top_k: int = 5) -> List[dict]:
        """Find most relevant chunks using cosine similarity"""
        try:
            if not document_chunks or not document_embeddings:
                print("[ERROR] No document chunks or embeddings provided")
                return []

            if len(document_chunks) != len(document_embeddings):
                print(f"[ERROR] Mismatch: {len(document_chunks)} chunks but {len(document_embeddings)} embeddings")
                return []

            # Get query embedding
            query_embedding = self.get_query_embedding(query)

            if not query_embedding or all(x == 0 for x in query_embedding):
                print("[ERROR] Failed to generate query embedding, using keyword search")
                return self._simple_keyword_search(query, document_chunks, top_k)

            # Calculate cosine similarities
            similarities = []
            query_embedding_np = np.array(query_embedding).reshape(1, -1)

            for i, doc_emb in enumerate(document_embeddings):
                try:
                    # Ensure same dimensions
                    if len(doc_emb) != len(query_embedding):
                        print(f"[WARNING] Dimension mismatch: query={len(query_embedding)}, doc={len(doc_emb)}")
                        continue

                    doc_emb_np = np.array(doc_emb).reshape(1, -1)

                    # Handle zero vectors
                    if np.all(query_embedding_np == 0) or np.all(doc_emb_np == 0):
                        similarity = 0.0
                    else:
                        similarity = cosine_similarity(query_embedding_np, doc_emb_np)[0][0]

                    similarities.append((i, similarity))

                except Exception as e:
                    print(f"[ERROR] Error computing similarity for chunk {i}: {e}")
                    continue

            if not similarities:
                print("[ERROR] No valid similarities computed, using keyword search")
                return self._simple_keyword_search(query, document_chunks, top_k)

            # Sort by similarity and take top k
            similarities.sort(key=lambda x: x[1], reverse=True)

            results = []
            for idx, sim_score in similarities[:top_k]:
                if sim_score > 0.1:  # Relevance threshold
                    results.append({
                        'chunk_index': int(idx),
                        'content': document_chunks[idx],
                        'relevance_score': float(sim_score)
                    })

            print(f"[OK] Found {len(results)} relevant chunks with scores: {[r['relevance_score'] for r in results]}")

            # If no results from embedding search, try keyword search
            if not results:
                print("[ERROR] No relevant chunks found with embeddings, trying keyword search")
                return self._simple_keyword_search(query, document_chunks, top_k)

            return results

        except Exception as e:
            print(f"[ERROR] Error in relevance search: {e}")
            # Fallback to simple keyword matching
            return self._simple_keyword_search(query, document_chunks, top_k)

    def _simple_keyword_search(self, query: str, chunks: List[str], top_k: int = 5) -> List[dict]:
        """Fallback: Simple keyword-based search"""
        try:
            query_words = set(query.lower().split())

            chunk_scores = []
            for i, chunk in enumerate(chunks):
                chunk_words = set(chunk.lower().split())
                # Calculate score based on word overlap
                overlap = query_words.intersection(chunk_words)
                score = len(overlap) / len(query_words) if query_words else 0

                # Bonus for exact phrase matches
                if query.lower() in chunk.lower():
                    score += 0.5

                chunk_scores.append((i, score))

            # Sort by score and take top k
            chunk_scores.sort(key=lambda x: x[1], reverse=True)

            results = []
            for idx, score in chunk_scores[:top_k]:
                if score > 0:
                    results.append({
                        'chunk_index': idx,
                        'content': chunks[idx],
                        'relevance_score': score
                    })

            print(f"[OK] Keyword search found {len(results)} relevant chunks")

            return results

        except Exception as e:
            print(f"[ERROR] Error in keyword search: {e}")
            return []

    def _fallback_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Fallback: Simple word-based embeddings with fixed dimensions"""
        print("[WARNING] Using fallback embeddings (simple word vectors)")

        # Create a fixed vocabulary from all texts
        all_words = set()
        for text in texts:
            words = text.lower().split()
            all_words.update(words)

        # Use top words for consistency (up to embedding dimension)
        word_list = sorted(list(all_words))[:self.embedding_dimension]

        # Pad to exactly embedding_dimension
        while len(word_list) < self.embedding_dimension:
            word_list.append(f"pad_{len(word_list)}")

        embeddings = []
        for text in texts:
            words = set(text.lower().split())
            embedding = [1.0 if word in words else 0.0 for word in word_list]
            embeddings.append(embedding)

        return embeddings

# Global embeddings instance
embeddings_engine = GeminiEmbeddings()
