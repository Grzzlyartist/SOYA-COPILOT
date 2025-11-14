"""Chat agent for soybean farming advice."""
from langchain_groq import ChatGroq
from .memory_manager import MemoryManager
from .rag_retriever import RAGRetriever
from ..reasoning.react_agent import ReACTReasoning
import os


class ChatAgent:
    """Chat agent that provides soybean farming advice."""
    
    def __init__(self):
        """Initialize the chat agent."""
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",
            temperature=0.3  # Lower temperature for more focused, consistent responses
        )
        self.memory_manager = MemoryManager(max_memory=4)
        self.rag_retriever = RAGRetriever()
        self.react_reasoning = ReACTReasoning()
        
        # System identity
        self.system_identity = "You are Soya Copilot, an AI agricultural assistant for soybean farmers worldwide."

    def process_message(self, user_message):
        """
        Process a user message and generate a response.
        Uses RAG to retrieve relevant knowledge from PDF files.
        
        Args:
            user_message: The user's question or message
            
        Returns:
            str: The AI's response based on knowledge base
        """
        # Get context from RAG (retrieves from PDF knowledge base)
        context_docs = self.rag_retriever.retrieve(user_message, k=5)  # Get top 5 relevant chunks
        
        if not context_docs:
            context = "No specific knowledge found. Provide general soybean farming advice."
        else:
            # Format context without source markers - just the raw information
            context_parts = []
            for doc in context_docs:
                content = doc["page_content"]
                # Truncate very long content
                if len(content) > 500:
                    content = content[:500] + "..."
                context_parts.append(content)
            context = "\n\n".join(context_parts)
        
        # Get recent conversation history
        memory = self.memory_manager.get_recent_memory()
        
        # Check if this is the first interaction
        is_first_interaction = len(self.memory_manager.conversation_memory) == 0
        
        # Apply ReACT reasoning
        reasoning_result = self.react_reasoning.reason_and_act(
            user_message=user_message,
            context=context,
            memory=memory,
            available_tools=["knowledge_base", "conversation_memory"]
        )
        
        # Create greeting based on interaction history
        if is_first_interaction:
            greeting = "Hello! I'm Soya Copilot, your AI agricultural assistant for soybean farming. "
        else:
            greeting = ""
        
        # Create enhanced prompt with ReACT reasoning
        reasoning_prompt = self.react_reasoning.get_reasoning_prompt(reasoning_result)
        
        prompt = f"""You are Soya Copilot, an AI agricultural assistant for soybean farmers worldwide.

=== RELEVANT KNOWLEDGE ===
{context}
===========================

{f"Recent conversation:{chr(10)}{memory}" if memory else ""}

Current question: {user_message}

=== REACT REASONING ANALYSIS ===
{reasoning_prompt}

INSTRUCTIONS:
1. {greeting}Follow the ReACT reasoning analysis above to structure your response
2. Use the relevant knowledge as your primary information source
3. Provide actionable, practical advice with specific details (numbers, timing, methods)
4. Be conversational and acknowledge previous context if continuing a conversation
5. Don't mention your reasoning process in the final response - just give the helpful answer
6. Focus on what the farmer can actually implement
7. Keep responses practical and farmer-friendly

Response:"""

        try:
            response = self.llm.invoke(prompt)
            response_text = response.content
        
        except Exception as e:
            response_text = f"I apologize, but I'm having trouble generating a response. Error: {str(e)}"
        
        # Update memory
        self.memory_manager.add_interaction(user_message, response_text)
        
        return response_text
