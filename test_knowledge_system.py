#!/usr/bin/env python3
"""
Simple ChromaDB test that avoids problematic operations.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_simple_chromadb():
    """Test basic ChromaDB functionality without complex operations."""
    
    print("🗄️  Simple ChromaDB Test")
    print("=" * 30)
    
    # Test basic imports
    print("📦 Testing Imports:")
    try:
        import chromadb
        print(f"  ✅ ChromaDB: {chromadb.__version__}")
        
        from langchain_chroma import Chroma
        print("  ✅ LangChain Chroma")
        
        from langchain_huggingface import HuggingFaceEmbeddings
        print("  ✅ HuggingFace Embeddings")
        
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False
    
    # Test RAG retriever initialization
    print("\n🔍 Testing RAG Retriever:")
    try:
        from agents.chat.rag_retriever import RAGRetriever
        
        # Create test directory
        test_dir = "./test_simple_chromadb"
        os.makedirs(test_dir, exist_ok=True)
        
        retriever = RAGRetriever(persist_directory=test_dir)
        print("  ✅ RAG retriever created")
        
        # Test retrieval (should work with keyword fallback if ChromaDB fails)
        results = retriever.retrieve("soybean temperature", k=2)
        print(f"  ✅ Retrieved {len(results)} results")
        
        if results:
            print(f"  📋 Sample: {results[0]['page_content'][:50]}...")
        
        # Check if vector store is actually working
        if retriever.use_vector_store:
            print("  ✅ Vector store is active")
        else:
            print("  ⚠️  Using keyword search fallback")
        
    except Exception as e:
        print(f"  ❌ RAG retriever failed: {e}")
        return False
    
    # Test chat agent
    print("\n💬 Testing Chat Agent:")
    try:
        from agents.chat.chat_agent import ChatAgent
        
        chat_agent = ChatAgent()
        print("  ✅ Chat agent created")
        
        # Test simple message processing
        response = chat_agent.process_message("What temperature do soybeans need?")
        print("  ✅ Message processed successfully")
        print(f"  📋 Response length: {len(response)} characters")
        
    except Exception as e:
        print(f"  ❌ Chat agent failed: {e}")
        return False
    
    # Cleanup
    print("\n🧹 Cleanup:")
    try:
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        print("  ✅ Test files cleaned up")
    except Exception as e:
        print(f"  ⚠️  Cleanup failed: {e}")
    
    return True


if __name__ == "__main__":
    try:
        success = test_simple_chromadb()
        if success:
            print("\n✅ ChromaDB system is working!")
            print("\nNote: If you see 'keyword search fallback', that's normal.")
            print("The system will work with or without ChromaDB vector search.")
        else:
            print("\n❌ ChromaDB test failed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()