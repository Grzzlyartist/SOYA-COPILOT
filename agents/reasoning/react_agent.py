"""
ReACT (Reasoning and Acting) Agent for Soya Copilot
Implements structured reasoning for better decision making and responses
"""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class ReACTReasoning:
    """
    ReACT (Reasoning and Acting) framework for structured AI reasoning.
    
    The ReACT framework follows this pattern:
    1. THOUGHT: Analyze the situation and think about what needs to be done
    2. ACTION: Decide what action to take based on the analysis
    3. OBSERVATION: Observe the results and context
    4. RESPONSE: Provide the final response based on reasoning
    """
    
    def __init__(self):
        self.reasoning_history = []
    
    def reason_and_act(self, 
                      user_message: str, 
                      context: str, 
                      memory: str, 
                      available_tools: List[str] = None) -> Dict[str, Any]:
        """
        Apply ReACT reasoning to a user message.
        
        Args:
            user_message: The user's input
            context: Relevant knowledge context
            memory: Conversation history
            available_tools: List of available tools/actions
            
        Returns:
            Dict containing reasoning steps and final response
        """
        
        # Step 1: THOUGHT - Analyze the situation
        thought = self._analyze_situation(user_message, context, memory)
        
        # Step 2: ACTION - Determine what action to take
        action = self._determine_action(user_message, thought, available_tools or [])
        
        # Step 3: OBSERVATION - Consider available information
        observation = self._make_observation(context, memory, action)
        
        # Step 4: RESPONSE - Generate structured response
        response_strategy = self._plan_response(thought, action, observation)
        
        reasoning_result = {
            "thought": thought,
            "action": action,
            "observation": observation,
            "response_strategy": response_strategy,
            "user_message": user_message
        }
        
        # Store reasoning for potential follow-up
        self.reasoning_history.append(reasoning_result)
        
        return reasoning_result
    
    def _analyze_situation(self, user_message: str, context: str, memory: str) -> str:
        """
        THOUGHT: Analyze what the user is asking and what they need.
        """
        message_lower = user_message.lower()
        
        # Analyze question type
        if any(word in message_lower for word in ['how', 'when', 'what', 'where', 'why']):
            question_type = "information_seeking"
        elif any(word in message_lower for word in ['help', 'problem', 'issue', 'trouble']):
            question_type = "problem_solving"
        elif any(word in message_lower for word in ['should', 'recommend', 'suggest', 'advice']):
            question_type = "recommendation_seeking"
        else:
            question_type = "general_inquiry"
        
        # Analyze farming domain
        farming_topics = {
            'planting': ['plant', 'seed', 'sow', 'germination'],
            'disease': ['disease', 'sick', 'infection', 'pest', 'problem'],
            'weather': ['weather', 'rain', 'temperature', 'climate'],
            'harvest': ['harvest', 'yield', 'crop', 'production'],
            'soil': ['soil', 'fertilizer', 'nutrients', 'pH'],
            'general': ['soybean', 'farming', 'agriculture']
        }
        
        detected_topics = []
        for topic, keywords in farming_topics.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_topics.append(topic)
        
        # Consider conversation context
        has_context = bool(memory.strip())
        has_knowledge = bool(context.strip())
        
        thought = f"User is asking a {question_type} question about {', '.join(detected_topics) if detected_topics else 'general farming'}. "
        
        if has_context:
            thought += "This continues a previous conversation. "
        
        if has_knowledge:
            thought += "Relevant knowledge is available to answer this question."
        else:
            thought += "Limited specific knowledge available - will provide general guidance."
        
        return thought
    
    def _determine_action(self, user_message: str, thought: str, available_tools: List[str]) -> str:
        """
        ACTION: Decide what action to take based on the analysis.
        """
        message_lower = user_message.lower()
        
        # Determine primary action needed
        if any(word in message_lower for word in ['translate', 'language']):
            action = "provide_translation_info"
        elif any(word in message_lower for word in ['weather', 'climate', 'location']):
            action = "analyze_location_suitability"
        elif any(word in message_lower for word in ['disease', 'sick', 'problem', 'pest']):
            action = "diagnose_plant_health"
        elif any(word in message_lower for word in ['plant', 'seed', 'sow']):
            action = "provide_planting_guidance"
        elif any(word in message_lower for word in ['harvest', 'yield']):
            action = "provide_harvest_guidance"
        elif any(word in message_lower for word in ['fertilizer', 'soil', 'nutrients']):
            action = "provide_soil_management_advice"
        else:
            action = "provide_general_farming_advice"
        
        # Consider available tools
        if available_tools:
            action += f" using available tools: {', '.join(available_tools)}"
        
        return action
    
    def _make_observation(self, context: str, memory: str, action: str) -> str:
        """
        OBSERVATION: Consider the available information and context.
        """
        observations = []
        
        # Observe knowledge availability
        if context and len(context.strip()) > 50:
            observations.append("Comprehensive knowledge base available with specific information")
        elif context:
            observations.append("Some relevant knowledge available")
        else:
            observations.append("Limited specific knowledge - will rely on general expertise")
        
        # Observe conversation context
        if memory and len(memory.strip()) > 20:
            observations.append("Previous conversation context provides additional insight")
        
        # Observe action complexity
        if "location" in action or "weather" in action:
            observations.append("Location-specific analysis requires weather data")
        elif "disease" in action or "diagnose" in action:
            observations.append("Plant health diagnosis benefits from visual inspection")
        elif "translate" in action:
            observations.append("Translation request requires language processing")
        
        return ". ".join(observations) + "."
    
    def _plan_response(self, thought: str, action: str, observation: str) -> str:
        """
        Plan the response strategy based on reasoning.
        """
        strategy_components = []
        
        # Determine response structure
        if "problem" in thought.lower() or "diagnose" in action:
            strategy_components.append("Start with problem acknowledgment")
            strategy_components.append("Provide step-by-step diagnostic approach")
            strategy_components.append("Include preventive measures")
        elif "recommendation" in thought.lower() or "advice" in action:
            strategy_components.append("Provide clear recommendations")
            strategy_components.append("Include specific timing and measurements")
            strategy_components.append("Explain reasoning behind recommendations")
        elif "information" in thought.lower():
            strategy_components.append("Provide comprehensive information")
            strategy_components.append("Structure information logically")
            strategy_components.append("Include practical examples")
        
        # Add context-specific elements
        if "knowledge base available" in observation:
            strategy_components.append("Reference specific knowledge from database")
        
        if "conversation context" in observation:
            strategy_components.append("Acknowledge previous discussion")
        
        # Always include practical focus
        strategy_components.append("Focus on actionable, practical advice")
        strategy_components.append("Use farmer-friendly language")
        
        return "; ".join(strategy_components)
    
    def get_reasoning_prompt(self, reasoning_result: Dict[str, Any]) -> str:
        """
        Generate a prompt that includes the ReACT reasoning for the LLM.
        """
        return f"""Based on ReACT reasoning analysis:

THOUGHT: {reasoning_result['thought']}
ACTION: {reasoning_result['action']}
OBSERVATION: {reasoning_result['observation']}
RESPONSE STRATEGY: {reasoning_result['response_strategy']}

Now provide a helpful response to the farmer following this reasoning approach."""
    
    def clear_history(self):
        """Clear reasoning history."""
        self.reasoning_history = []
    
    def get_recent_reasoning(self, limit: int = 3) -> List[Dict[str, Any]]:
        """Get recent reasoning history."""
        return self.reasoning_history[-limit:] if self.reasoning_history else []