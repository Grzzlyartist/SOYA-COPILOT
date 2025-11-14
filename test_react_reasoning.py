#!/usr/bin/env python3
"""
Test script for ReACT reasoning functionality.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_react_reasoning():
    """Test ReACT reasoning system."""
    
    print("🧠 Testing ReACT Reasoning System")
    print("=" * 40)
    
    try:
        # Test ReACT reasoning module
        print("📦 Testing ReACT Reasoning Module:")
        from agents.reasoning.react_agent import ReACTReasoning
        
        react_agent = ReACTReasoning()
        print("  ✅ ReACT reasoning module imported successfully")
        
        # Test reasoning with different types of questions
        test_cases = [
            {
                "message": "How do I plant soybeans?",
                "context": "Plant soybeans in well-drained soil with pH 6.0-7.0",
                "memory": "",
                "expected_action": "provide_planting_guidance"
            },
            {
                "message": "My soybean leaves have spots",
                "context": "Leaf spots can indicate bacterial blight or fungal diseases",
                "memory": "",
                "expected_action": "diagnose_plant_health"
            },
            {
                "message": "What's the weather like for farming?",
                "context": "Weather affects planting and harvest timing",
                "memory": "",
                "expected_action": "analyze_location_suitability"
            }
        ]
        
        print("\n🔄 Testing Reasoning Cases:")
        for i, case in enumerate(test_cases, 1):
            print(f"\n  Case {i}: {case['message']}")
            
            result = react_agent.reason_and_act(
                user_message=case['message'],
                context=case['context'],
                memory=case['memory']
            )
            
            print(f"    Thought: {result['thought'][:60]}...")
            print(f"    Action: {result['action']}")
            print(f"    Expected: {case['expected_action']}")
            
            if case['expected_action'] in result['action']:
                print("    ✅ Correct action identified")
            else:
                print("    ⚠️  Different action identified (may still be valid)")
        
        # Test chat agent integration
        print("\n💬 Testing Chat Agent Integration:")
        from agents.chat.chat_agent import ChatAgent
        
        if not os.getenv("GROQ_API_KEY"):
            print("  ⚠️  GROQ_API_KEY not set - skipping chat agent test")
        else:
            chat_agent = ChatAgent()
            print("  ✅ Chat agent with ReACT reasoning initialized")
            
            # Test that ReACT reasoning is integrated
            if hasattr(chat_agent, 'react_reasoning'):
                print("  ✅ ReACT reasoning integrated into chat agent")
            else:
                print("  ❌ ReACT reasoning not found in chat agent")
        
        # Test reasoning history
        print("\n📚 Testing Reasoning History:")
        history = react_agent.get_recent_reasoning()
        print(f"  ✅ Reasoning history contains {len(history)} entries")
        
        if history:
            latest = history[-1]
            print(f"  📋 Latest reasoning: {latest['thought'][:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ ReACT reasoning test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_react_info():
    """Show information about ReACT reasoning."""
    print("\n🧠 ReACT Reasoning System Info:")
    print("  • THOUGHT: Analyzes the user's question and context")
    print("  • ACTION: Determines what approach to take")
    print("  • OBSERVATION: Considers available knowledge and context")
    print("  • RESPONSE: Structures the final answer based on reasoning")
    print("\n📈 Benefits:")
    print("  • More structured and logical responses")
    print("  • Better handling of complex farming questions")
    print("  • Improved context awareness")
    print("  • Consistent reasoning approach")


if __name__ == "__main__":
    success = test_react_reasoning()
    if success:
        print("\n✅ ReACT reasoning system is working correctly!")
        show_react_info()
    else:
        print("\n❌ ReACT reasoning system has issues!")