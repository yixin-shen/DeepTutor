# simple_test.py - 简单测试脚本
import streamlit as st
import chromadb
import os

def main():
    st.title("🤖 Offline Zotero Assistant")
    st.markdown("*Your personal AI research assistant - completely offline*")
    
    # Connect to database
    try:
        client = chromadb.PersistentClient(path=os.path.expanduser("~/.config/zotero-mcp/chroma_db"))
        
        collection = client.get_collection("zotero_library")
        count = collection.count()
        
        # Display assistant status
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("🤖 **Assistant Status:**")
            with col2:
                st.success(f"✅ Online - {count} papers available")
        
        st.divider()
        
        # Chat interface
        st.markdown("### 💬 Ask me about your research papers")
        
        # Results control
        col1, col2 = st.columns([1, 2])
        with col1:
            n_results = st.selectbox("Number of results", [3, 5, 10, 15, 20], index=1)
        with col2:
            st.markdown(f"*Will show up to {n_results} most relevant papers*")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about your papers..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate assistant response
            with st.chat_message("assistant"):
                try:
                    # First, try to understand the user's intent
                    prompt_lower = prompt.lower()
                    
                    # Handle different types of queries
                    if any(word in prompt_lower for word in ['hello', 'hi', 'hey', 'greetings']):
                        response = "Hello! 👋 I'm your offline Zotero research assistant. I can help you find and discuss papers in your library. What would you like to know about your research?"
                    
                    elif any(word in prompt_lower for word in ['how are you', 'how do you work', 'what can you do']):
                        response = "I'm doing great! 🤖 I'm an offline AI assistant that can:\n\n• Search through your Zotero papers\n• Explain research topics\n• Compare different papers\n• Suggest related research areas\n• Answer questions about your library\n\nI work completely offline using semantic search on your local papers. What would you like to explore?"
                    
                    elif any(word in prompt_lower for word in ['thank', 'thanks', 'appreciate']):
                        response = "You're very welcome! 😊 I'm here to help with your research. Is there anything else you'd like to know about your papers?"
                    
                    elif any(word in prompt_lower for word in ['bye', 'goodbye', 'see you']):
                        response = "Goodbye! 👋 Feel free to come back anytime to explore your research library. Happy researching!"
                    
                    elif any(word in prompt_lower for word in ['help', 'what can you help', 'capabilities']):
                        response = "I can help you with:\n\n📚 **Paper Search**: Find papers by topic, author, or content\n🔍 **Semantic Search**: Understand what you're looking for even if you don't use exact keywords\n📊 **Research Analysis**: Compare papers and understand trends\n💡 **Topic Exploration**: Discover related research areas\n📝 **Paper Summaries**: Get quick overviews of papers\n\nJust ask me anything about your research!"
                    
                    elif any(word in prompt_lower for word in ['explain', 'what is', 'tell me about', 'describe']):
                        # This is a knowledge-seeking query
                        results = collection.query(
                            query_texts=[prompt],
                            n_results=n_results
                        )
                        
                        if results['documents'] and results['documents'][0]:
                            response = f"Based on your papers, here's what I found about '{prompt}':\n\n"
                            
                            for i, (doc, metadata, distance) in enumerate(zip(
                                results['documents'][0],
                                results['metadatas'][0],
                                results['distances'][0]
                            )):
                                similarity = 1 - distance
                                response += f"**{i+1}. {metadata.get('title', 'Untitled')}**\n"
                                response += f"   📊 Relevance: {similarity:.2f}\n"
                                response += f"   📝 {doc[:200]}...\n\n"
                            
                            response += f"These papers seem most relevant to your question. Would you like me to explain any specific aspect in more detail?"
                        else:
                            response = f"I don't have enough information in your library to explain '{prompt}' in detail. However, I can help you search for related topics or explore what's available in your papers. What specific aspect would you like to know more about?"
                    
                    else:
                        # Regular search query
                        results = collection.query(
                            query_texts=[prompt],
                            n_results=n_results
                        )
                        
                        if results['documents'] and results['documents'][0]:
                            response = f"I found {len(results['documents'][0])} relevant papers in your library:\n\n"
                            
                            for i, (doc, metadata, distance) in enumerate(zip(
                                results['documents'][0],
                                results['metadatas'][0],
                                results['distances'][0]
                            )):
                                similarity = 1 - distance
                                response += f"**{i+1}. {metadata.get('title', 'Untitled')}**\n"
                                response += f"   📊 Relevance: {similarity:.2f}\n"
                                response += f"   📝 {doc[:200]}...\n\n"
                            
                            response += f"These are the most relevant papers I found. Would you like me to explain any of these in more detail or search for something specific?"
                        else:
                            response = f"I couldn't find any papers directly related to '{prompt}' in your library. However, I can help you:\n\n• Search for similar topics\n• Explore what's available in your papers\n• Find papers on related subjects\n\nWhat would you like to try?"
                        
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                        
                except Exception as e:
                    response = f"Sorry, I encountered an error while processing your request: {e}"
                    st.error(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Sidebar with suggestions
        with st.sidebar:
            st.markdown("### 💡 Suggested Questions")
            suggestions = [
                "Tell me about doppler tomography",
                "What papers do you have on neural networks?",
                "Show me radar signal processing papers",
                "Find papers about machine learning",
                "What's in your library about computer vision?"
            ]
            
            for suggestion in suggestions:
                if st.button(suggestion, key=f"sugg_{suggestion[:20]}"):
                    # Simulate user input
                    st.session_state.messages.append({"role": "user", "content": suggestion})
                    st.rerun()
                    
    except Exception as e:
        st.error(f"❌ Connection error: {e}")
        st.info("Please make sure your Zotero database is properly set up.")

if __name__ == "__main__":
    main() 