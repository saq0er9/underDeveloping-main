import { useState, useEffect } from 'react';
import api from './api';
import './App.css';

function App() {
  const [students, setStudents] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [age, setAge] = useState('');

  const fetchStudents = async () => {
    try {
      const response = await api.get('/students/');
      setStudents(response.data);
    } catch (error) {
      console.error('Error fetching students:', error);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const handleAddStudent = async (e) => {
    e.preventDefault();
    
    // التحقق من أن العمر رقم موجب
    if (parseInt(age) <= 0) {
      alert('Please enter a valid positive age');
      return;
    }

    try {
      await api.post('/students/', {
        name,
        email,
        age: parseInt(age),
      });
      setName('');
      setEmail('');
      setAge('');
      fetchStudents();
    } catch (error) {
      console.error('Error adding student:', error);
    }
  };

  const handleDeleteStudent = async (id) => {
    try {
      await api.delete(`/students/${id}`);
      fetchStudents();
    } catch (error) {
      console.error('Error deleting student:', error);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>Student Management System</h1>
        <p>Full-Stack Application with FastAPI, React, & PostgreSQL</p>
      </header>

      <div className="grid-layout">
        {/* Add Student Card */}
        <div className="card">
          <h3 className="card-title">Add New Student</h3>
          <form onSubmit={handleAddStudent}>
            <div className="form-group">
              <label>Full Name</label>
              <input
                className="input-control"
                type="text"
                placeholder="Enter full name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label>Email Address</label>
              <input
                className="input-control"
                type="email"
                placeholder="example@domain.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            
            <div className="form-group">
              <label>Age</label>
              <input
                className="input-control"
                type="number"
                min="1"
                placeholder="Enter age"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="btn-primary">
              Save Student
            </button>
          </form>
        </div>

        {/* Student List Card */}
        <div className="card">
          <h3 className="card-title">Registered Students ({students.length})</h3>

          {students.length === 0 ? (
            <div className="empty-state">No students registered yet</div>
          ) : (
            <ul className="student-list">
              {students.map((student) => (
                <li key={student.id} className="student-item">
                  <div className="student-info">
                    <h4>
                      {student.name}
                      <span className="badge">{student.age} yrs</span>
                    </h4>
                    <p>{student.email}</p>
                  </div>
                  <button
                    onClick={() => handleDeleteStudent(student.id)}
                    className="btn-danger"
                  >
                    Delete
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;