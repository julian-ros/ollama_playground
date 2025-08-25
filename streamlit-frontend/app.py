import streamlit as st
import requests
import json
import os
import time
from langchain_community.llms import Ollama

# Configuration
EMBEDDINGS_API_URL = os.environ.get("EMBEDDINGS_API_URL", "http://embeddings-api:8000")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://ollama_chat:11434")
OLLAMA_CHAT_MODEL = os.environ.get("OLLAMA_CHAT_MODEL", "llama3.2")

# Initialize Ollama for direct chat
@st.cache_resource
def get_ollama_client():
    return Ollama(
        model=OLLAMA_CHAT_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.7
    )

def main():
    st.set_page_config(
        page_title="AI Chat Assistant",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 AI Chat Assistant")
    st.markdown("Chat with your documents using local OLLAMA models")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        retrieve_embeddings = st.checkbox("Retrieve Embeddings", value=True, help="Include relevant document context in responses")
        include_history = st.checkbox("Include Conversation History", value=True, help="Summarize and include previous conversation context")
        use_streaming = st.checkbox("Enable Streaming", value=True, help="Stream responses for faster perceived performance")
        st.info(f"Chat Model: {OLLAMA_CHAT_MODEL}")
        st.info(f"Embeddings API: {EMBEDDINGS_API_URL}")
        
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    if (retrieve_embeddings or include_history) and use_streaming:
                        # Use streaming embeddings API for context-aware responses
                        response = get_streaming_embeddings_response(prompt, retrieve_embeddings, include_history)
                    elif retrieve_embeddings or include_history:
                        # Use embeddings API for context-aware responses
                        response = get_embeddings_response(prompt, retrieve_embeddings, include_history)
                    elif use_streaming:
                        # Use direct Ollama streaming
                        response = get_direct_streaming_response(prompt)
                    else:
                        # Use direct Ollama chat
                        ollama_client = get_ollama_client()
                        response = ollama_client.invoke(prompt)
                        st.markdown(response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

def get_streaming_embeddings_response(prompt, retrieve_embeddings=True, include_history=True):
    """Get streaming response using embeddings API for context"""
    try:
        # Prepare the conversation format expected by the API
        conversation = {
            "messages": st.session_state.messages.copy(),
            "retrieve_embeddings": retrieve_embeddings,
            "include_history_summary": include_history
        }
        
        # Add current prompt to the conversation
        conversation["messages"].append({"role": "user", "content": prompt})
        
        # Call the streaming embeddings API
        response = requests.post(
            f"{EMBEDDINGS_API_URL}/chat/stream",
            json={"text": conversation},
            stream=True,
            timeout=120
        )
        
        if response.status_code == 200:
            # Create a placeholder for streaming content
            message_placeholder = st.empty()
            full_response = ""
            
            # Process the streaming response
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]  # Remove 'data: ' prefix
                        if data == '[DONE]':
                            break
                        try:
                            chunk_data = json.loads(data)
                            if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                                delta = chunk_data['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    content = delta['content']
                                    full_response += content
                                    message_placeholder.markdown(full_response + "▌")
                                    time.sleep(0.01)  # Small delay for visual effect
                        except json.JSONDecodeError:
                            continue
            
            # Final update without cursor
            message_placeholder.markdown(full_response)
            return full_response
        else:
            return f"API Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.RequestException as e:
        return f"Connection Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_direct_streaming_response(prompt):
    """Get streaming response directly from Ollama"""
    try:
        ollama_client = get_ollama_client()
        
        # Create a placeholder for streaming content
        message_placeholder = st.empty()
        full_response = ""
        
        # Stream the response
        for chunk in ollama_client.stream(prompt):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.01)  # Small delay for visual effect
        
        # Final update without cursor
        message_placeholder.markdown(full_response)
        return full_response
        
    except Exception as e:
        return f"Streaming Error: {str(e)}"

def get_embeddings_response(prompt, retrieve_embeddings=True, include_history=True):
    """Get response using embeddings API for context"""
    try:
        # Prepare the conversation format expected by the API
        conversation = {
            "messages": st.session_state.messages.copy(),
            "retrieve_embeddings": retrieve_embeddings,
            "include_history_summary": include_history
        }
        
        # Add current prompt to the conversation
        conversation["messages"].append({"role": "user", "content": prompt})
        
        # Call the embeddings API
        response = requests.post(
            f"{EMBEDDINGS_API_URL}/chat",
            json={"text": conversation},
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"API Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.RequestException as e:
        return f"Connection Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    main()