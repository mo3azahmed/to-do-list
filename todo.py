import streamlit as st
from datetime import datetime
import uuid

# Configure the page
st.set_page_config(
    page_title="Do List",
    page_icon="✓",
    layout="centered"
)

st.markdown("""
<meta name="description" content="A free and simple to-do list app. No login, no sign-up, no nonsense—just add tasks and get stuff done.">
<meta name="keywords" content="todo, to-do list, task manager, productivity, streamlit, no login, no signup, free todo app">
<meta name="robots" content="index, follow">
""", unsafe_allow_html=True)


#CSS styling. i didnt do much here
st.markdown("""
<style>
    /* to override streamlit default theme!*/
    .stApp {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* same for the text */
    .stApp > div > div > div > div {
        color: #333333 !important;
    }
    
    /* colors!! */
    :root {
        --primary-color: #56ab2f;
        --secondary-color: #a8e6cf;
        --success-color: #00b894;
        --background-light: #f1f8e9;
        --text-dark: #333333;
        --text-muted: #2d5016;

        --white: #ffffff;
    }

    .main-header {
        text-align: center;
        color: var(--primary-color) !important;
        font-size: 3rem;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: bold;
    }
    
    /* more colors */
    .stApp h2, .stApp h3 {
        color: var(--text-dark) !important;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        background: linear-gradient(135deg, var(--background-light), #e9ecef) !important;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stat-item {
        text-align: center;
        padding: 0.5rem;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--primary-color) !important;
        display: block;
    }
    
    .stat-label {
        font-size: 1rem;
        color: var(--text-muted) !important;
        font-weight: 500;
        display: block;
        margin-top: 0.25rem;
    }
    
    .todo-item {
        background: var(--white) !important;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 12px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.12);
        border-left: 5px solid var(--primary-color);
        color: var(--text-dark) !important;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .todo-item:hover {
        box-shadow: 0 5px 10px rgba(0,0,0,0.15);
        transform: translateY(-1px);
    }
    
    .completed-item {
        opacity: 0.7;
        text-decoration: line-through;
        border-left-color: var(--success-color) !important;
        background: #f8f9fa !important;
    }
    
    .empty-state {
        text-align: center;
        color: var(--text-muted) !important;
        font-style: italic;
        padding: 3rem;
        background: var(--background-light) !important;
        border-radius: 15px;
        border: 2px dashed #a8e6cf;
        font-size: 1.2rem;
    }
    
    /* Fix input styling */
    .stTextInput > div > div > input {
        background-color: var(--white) !important;
        color: var(--text-dark) !important;
        border: 2px solid #e9ecef !important;
        border-radius: 8px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 2px rgba(86, 171, 47, 0.2) !important;
    }
    
    /* Fix button styling */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    /* Delete button styling - RED! - Multiple selectors to ensure it works */
    .stColumns > div:nth-child(3) .stButton > button,
    div[data-testid="column"]:nth-child(3) button,
    button[title="Delete task"] {
        background-color: #dc3545 !important;  
        background: #dc3545 !important;
        color: white !important;
        border: none !important;
    }
    
    .stColumns > div:nth-child(3) .stButton > button:hover,
    div[data-testid="column"]:nth-child(3) button:hover,
    button[title="Delete task"]:hover {
        background-color: #c82333 !important;
        background: #c82333 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(220, 53, 69, 0.4) !important;
    }        
        
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-color), #4a9426) !important;
        border: none !important;
        color: white !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #4a9426, var(--primary-color)) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: #6c757d !important;
        color: white !important;
        border: none !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #545b62 !important;
        transform: translateY(-1px) !important;
    }
    
    /* Ensure footer text is visible */
    .stMarkdown p {
        color: var(--text-dark) !important;
    }
    
    /* Fix markdown content */
    .stMarkdown {
        color: var(--text-dark) !important;
    }
    
    /* Override any remaining dark theme elements */
    div[data-testid="stMarkdownContainer"] {
        color: var(--text-dark) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for storing todos (a streamlit thingy i dont really understand)
if 'todos' not in st.session_state:
    st.session_state.todos = []
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# Helper functions
def add_todo(text):
    """Add a new todo item"""
    todo = {
        'id': str(uuid.uuid4()),
        'text': text,
        'completed': False,
        'created_at': datetime.now()
    }
    st.session_state.todos.append(todo)
    # Increment input key to clear the text input
    st.session_state.input_key += 1

def toggle_todo(todo_id):
    """Toggle completion status of a todo"""
    for todo in st.session_state.todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            break

def delete_todo(todo_id):
    """delete a todo item"""
    st.session_state.todos = [todo for todo in st.session_state.todos if todo['id'] != todo_id]

def get_stats():
    """calculate our todos. total completed and remaining"""
    total = len(st.session_state.todos)
    completed = sum(1 for todo in st.session_state.todos if todo['completed'])
    remaining = total - completed
    return total, completed, remaining

# Main App
def main():
    # Title
    st.markdown('<h1 class="main-header">✓ To-Do List</h1>', unsafe_allow_html=True)
    
    # Add new todo section
    st.subheader("📝 Add New Task")
    
    # Create columns for input and button
    col1, col2 = st.columns([4, 1])
    
    with col1:
        new_todo = st.text_input("What needs to be done?", placeholder="Enter a new task...", label_visibility="collapsed", key=f"todo_input_{st.session_state.input_key}")
    
    with col2:
        add_button = st.button("Add", type="primary", use_container_width=True)
    
    # Add todo when button is clicked or Enter is pressed
    if add_button and new_todo.strip():
        add_todo(new_todo.strip())
        st.rerun()
    
    # Display statistics
    total, completed, remaining = get_stats()
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-item">
            <div class="stat-number">{total}</div>
            <div class="stat-label">Total Tasks</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{completed}</div>
            <div class="stat-label">Completed</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{remaining}</div>
            <div class="stat-label">Remaining</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display todos
    st.subheader("📋 Your Tasks")
    
    if not st.session_state.todos:
        st.markdown('<div class="empty-state">No tasks yet. Add one to get started! 🚀</div>', unsafe_allow_html=True)
    else:
        # Sort todos: incomplete first, then completed
        sorted_todos = sorted(st.session_state.todos, key=lambda x: (x['completed'], x['created_at']))
        
        for todo in sorted_todos:
            # Create columns for todo item
            col1, col2, col3 = st.columns([6, 1, 1])
            
            with col1:
                # Display todo text with completion status
                status_icon = "✅" if todo['completed'] else "⏳"
                todo_class = "completed-item" if todo['completed'] else ""
                st.markdown(f'<div class="todo-item {todo_class}">{status_icon} {todo["text"]}</div>', unsafe_allow_html=True)
            
            with col2:
                # Toggle completion button
                button_text = "Undo" if todo['completed'] else "Done"
                button_type = "secondary" if todo['completed'] else "primary"
                if st.button(button_text, key=f"toggle_{todo['id']}", type=button_type):
                    toggle_todo(todo['id'])
                    st.rerun()
            
            with col3:
                # Delete button
                if st.button("🗑️", key=f"delete_{todo['id']}", help="Delete task"):
                    delete_todo(todo['id'])
                    st.rerun()
    
    # Footer
    st.markdown("---")

if __name__ == "__main__":
    main()
