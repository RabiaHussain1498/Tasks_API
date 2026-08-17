import { useState, useEffect } from 'react';

const API_URL = import.meta.env.VITE_API_URL;

function Notes({ token, setToken }) {
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');
  const [editingNoteId, setEditingNoteId] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  const authHeaders = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  const fetchNotes = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/api/v1/notes`, { headers: authHeaders });
      if (response.status === 401) {
        setToken(null);
        return;
      }
      if (!response.ok) throw new Error(`Failed to fetch notes: ${response.status}`);
      const data = await response.json();
      setNotes(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !body.trim()) return;

    if (editingNoteId) {
      await updateNote(editingNoteId, { title, body });
    } else {
      await createNote({ title, body });
    }
  };

  const createNote = async (noteData) => {
    try {
      const response = await fetch(`${API_URL}/api/v1/notes`, {
        method: 'POST',
        headers: authHeaders,
        body: JSON.stringify(noteData)
      });
      if (response.status === 401) return setToken(null);
      if (!response.ok) throw new Error(`Create failed: ${response.status}`);
      
      const newNote = await response.json();
      setNotes([...notes, newNote]);
      resetForm();
    } catch (err) {
      setError(err.message);
    }
  };

  const updateNote = async (id, noteData) => {
    try {
      const response = await fetch(`${API_URL}/api/v1/notes/${id}`, {
        method: 'PUT',
        headers: authHeaders,
        body: JSON.stringify(noteData)
      });
      
      if (response.status === 401) return setToken(null);
      if (response.status === 404) throw new Error('Note not found (404). It might have been deleted.');
      if (!response.ok) throw new Error(`Update failed: ${response.status}`);
      
      const updatedNote = await response.json();
      setNotes(notes.map(n => n.id === id ? updatedNote : n));
      resetForm();
    } catch (err) {
      setError(err.message);
    }
  };

  const deleteNote = async (id) => {
    if (!window.confirm('Are you sure you want to delete this note?')) return;
    
    try {
      const response = await fetch(`${API_URL}/api/v1/notes/${id}`, {
        method: 'DELETE',
        headers: authHeaders
      });
      
      if (response.status === 401) return setToken(null);
      if (response.status === 404) throw new Error('Note not found (404). It was already deleted.');
      if (!response.ok) throw new Error(`Delete failed: ${response.status}`);
      
      setNotes(notes.filter(n => n.id !== id));
    } catch (err) {
      setError(err.message);
    }
  };

  const startEditing = (note) => {
    setEditingNoteId(note.id);
    setTitle(note.title);
    setBody(note.body);
    window.scrollTo(0, 0);
  };

  const resetForm = () => {
    setEditingNoteId(null);
    setTitle('');
    setBody('');
  };

  return (
    <div className="notes-container">
      <div className="header-bar">
        <h1>Your Notes</h1>
        <button className="btn-secondary" onClick={() => setToken(null)}>Logout</button>
      </div>
      
      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={() => setError('')}>Dismiss</button>
        </div>
      )}

      <form onSubmit={handleSubmit} className="task-form glass-panel">
        <h2>{editingNoteId ? 'Edit Note' : 'Create Note'}</h2>
        
        <div className="form-group">
          <label htmlFor="title">Title:</label>
          <input 
            type="text" 
            id="title"
            value={title} 
            onChange={(e) => setTitle(e.target.value)} 
            placeholder="Enter note title"
            required 
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="body">Body:</label>
          <textarea 
            id="body"
            value={body} 
            onChange={(e) => setBody(e.target.value)} 
            placeholder="Enter note content"
            required
            rows={4}
            className="custom-textarea"
          />
        </div>
        
        <div className="form-actions">
          <button type="submit" className="btn-primary">
            {editingNoteId ? 'Update Note' : 'Add Note'}
          </button>
          {editingNoteId && (
            <button type="button" className="btn-secondary" onClick={resetForm}>
              Cancel
            </button>
          )}
        </div>
      </form>

      <div className="tasks-list glass-panel">
        <h2>Saved Notes</h2>
        {loading ? (
          <p>Loading notes...</p>
        ) : notes.length === 0 ? (
          <p className="empty-state">No notes found. Create one above!</p>
        ) : (
          <ul>
            {notes.map(note => (
              <li key={note.id} className="task-item">
                <div className="task-content">
                  <div className="note-text">
                    <span className="task-title">{note.title}</span>
                    <p className="note-body">{note.body}</p>
                  </div>
                </div>
                <div className="task-actions">
                  <button onClick={() => startEditing(note)} className="btn-edit">Edit</button>
                  <button onClick={() => deleteNote(note.id)} className="btn-delete">Delete</button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default Notes;
