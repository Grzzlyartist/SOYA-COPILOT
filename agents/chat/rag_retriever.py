"""RAG retriever for soybean farming knowledge."""
import os

try:
    import chromadb
    # Try newer packages first
    try:
        from langchain_chroma import Chroma
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError:
        # Fallback to older packages
        from langchain_community.vectorstores import Chroma
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
        except ImportError:
            from langchain_community.embeddings import HuggingFaceEmbeddings
    CHROMADB_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  ChromaDB not available: {e}")
    print("   Using simple knowledge base instead")
    CHROMADB_AVAILABLE = False


class RAGRetriever:
    """Retrieves relevant soybean farming knowledge."""
    
    def __init__(self, persist_directory="./data/chromadb"):
        """Initialize the RAG retriever."""
        self.persist_directory = persist_directory
        self.knowledge_base = self._get_initial_knowledge()
        
        # Disable ChromaDB for now due to compatibility issues
        # Use reliable keyword search instead
        print("🔍 Using keyword-based search (ChromaDB disabled for stability)")
        self.use_vector_store = False

    def _get_initial_knowledge(self):
        """Get initial soybean farming knowledge base."""
        # Built-in knowledge
        builtin_knowledge = [
            "Soybeans grow best in temperatures between 20°C and 30°C.",
            "Well-drained soil with pH 6.0 to 7.0 is ideal for soybeans.",
            "Soybeans need consistent moisture during flowering and pod formation.",
            "Common soybean diseases include bacterial blight, powdery mildew, and soybean rust.",
            "Soybeans should be planted when soil temperature reaches at least 15°C.",
            "Crop rotation with corn or wheat helps prevent soil-borne diseases in soybeans.",
            "Plant soybeans 5-7 cm apart in rows 45-60 cm apart.",
            "Apply 200 kg/ha of NPK fertilizer at planting.",
            "Soybeans fix nitrogen from the air, reducing fertilizer needs.",
            "Harvest when leaves turn yellow and pods are dry."
        ]
        
        # Try to load knowledge from PDF/text files
        try:
            from pathlib import Path
            knowledge_dir = Path(__file__).parent.parent.parent / "data" / "knowledge"
            
            if knowledge_dir.exists():
                file_knowledge = self._load_files_from_directory(knowledge_dir)
                if file_knowledge:
                    print(f"✅ Loaded {len(file_knowledge)} knowledge items from files")
                    return builtin_knowledge + file_knowledge
        except Exception as e:
            print(f"⚠️  Could not load knowledge files: {e}")
        
        return builtin_knowledge
    
    def _load_files_from_directory(self, directory):
        """Load knowledge from text, markdown, and PDF files."""
        knowledge = []
        
        # Load text and markdown files
        for ext in ['.txt', '.md']:
            for file_path in directory.rglob(f'*{ext}'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if content:
                            # Split into paragraphs
                            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
                            knowledge.extend(paragraphs)
                            print(f"   📄 Loaded: {file_path.name}")
                except Exception as e:
                    print(f"   ❌ Error loading {file_path.name}: {e}")
        
        # Try to load PDF files if pypdf2 is available
        try:
            import PyPDF2
            for pdf_path in directory.rglob('*.pdf'):
                try:
                    with open(pdf_path, 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        text = ""
                        for page in pdf_reader.pages:
                            text += page.extract_text() + "\n"
                        
                        if text.strip():
                            # Split into paragraphs
                            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and len(p) > 50]
                            knowledge.extend(paragraphs)
                            print(f"   📄 Loaded PDF: {pdf_path.name} ({len(pdf_reader.pages)} pages)")
                except Exception as e:
                    print(f"   ❌ Error loading PDF {pdf_path.name}: {e}")
        except ImportError:
            pdf_files = list(directory.rglob('*.pdf'))
            if pdf_files:
                print(f"   ⚠️  Found {len(pdf_files)} PDF files but PyPDF2 not installed")
                print(f"   💡 Install with: pip install pypdf2")
        
        return knowledge

    def add_documents(self, documents):
        """Add documents to the vector store."""
        if self.use_vector_store:
            self.vector_store.add_documents(documents)

    def retrieve(self, query, k=4):
        """
        Retrieve relevant documents for a query.
        Prioritizes knowledge from PDF files.
        """
        if self.use_vector_store:
            try:
                # Retrieve more results to ensure we get PDF content
                results = self.vector_store.similarity_search(query, k=k*2)
                return [{"page_content": doc.page_content} for doc in results[:k]]
            except Exception as e:
                print(f"⚠️  Vector search failed: {e}")
        
        # Fallback to keyword matching
        query_lower = query.lower()
        query_words = [w for w in query_lower.split() if len(w) > 3]  # Filter short words
        
        # Score each knowledge item
        scored_items = []
        for knowledge in self.knowledge_base:
            knowledge_lower = knowledge.lower()
            score = sum(1 for word in query_words if word in knowledge_lower)
            if score > 0:
                scored_items.append((score, knowledge))
        
        # Sort by relevance score
        scored_items.sort(reverse=True, key=lambda x: x[0])
        
        # Return top k results
        relevant = [{"page_content": item[1]} for item in scored_items[:k]]
        
        # If no matches, return some default knowledge
        if not relevant:
            relevant = [{"page_content": self.knowledge_base[i]} for i in range(min(k, len(self.knowledge_base)))]
        
        return relevant

    def load_initial_knowledge(self):
        """Load initial knowledge into vector store."""
        if not self.use_vector_store or not self.knowledge_base:
            return
            
        try:
            from langchain_core.documents import Document
            
            # Create documents with metadata (limit to avoid memory issues)
            docs = []
            max_docs = min(50, len(self.knowledge_base))  # Limit to 50 documents
            
            for i, text in enumerate(self.knowledge_base[:max_docs]):
                # Skip very short or very long texts
                if len(text.strip()) < 20 or len(text) > 2000:
                    continue
                    
                # Determine if this is from a file or built-in
                source = "PDF Knowledge Base" if i >= 10 else "Built-in Knowledge"
                doc = Document(
                    page_content=text.strip(),
                    metadata={"source": source, "index": i}
                )
                docs.append(doc)
            
            if docs:
                # Add documents in smaller batches to avoid memory issues
                batch_size = 10
                for i in range(0, len(docs), batch_size):
                    batch = docs[i:i + batch_size]
                    try:
                        self.add_documents(batch)
                    except Exception as batch_e:
                        print(f"⚠️  Failed to add batch {i//batch_size + 1}: {batch_e}")
                        continue
                
                print(f"✅ Loaded {len(docs)} knowledge items into vector database")
            else:
                print("⚠️  No suitable documents found for vector store")
                
        except Exception as e:
            print(f"⚠️  Failed to load knowledge into vector store: {e}")
            print("   Continuing with keyword search fallback")
            self.use_vector_store = False
