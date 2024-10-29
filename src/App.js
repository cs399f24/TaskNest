import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Card } from './components/card';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTodo, setNewTodo] = useState("");

  useEffect(() => {
    axios.get('http://localhost:5000/tasks')
      .then(response => setTasks(response.data))
      .catch(error => console.error('Error fetching tasks:', error));
  }, []);

  const createNewTask = () => {
    if (newTodo !== "") {
      axios.post('http://localhost:5000/add', { description: newTodo })
        .then(response => {
          setTasks(response.data);
          setNewTodo("");
        })
        .catch(error => console.error('Error adding task:', error));
    }
  };

  const deleteTask = (index) => {
    axios.delete(`http://localhost:5000/delete/${index}`)
      .then(response => setTasks(response.data))
      .catch(error => console.error('Error deleting task:', error));
  };

  return (
    <div className="App">
      <motion.div
        className="todo-task-container"
        initial={{ opacity: 0, y: -100 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 2 }}
      >
        <h2 className="title">TaskNest</h2>
        <div className="todo-input-div">
          <input
            className="todo-input"
            type="text"
            onChange={(e) => setNewTodo(e.target.value)}
            value={newTodo}
            placeholder="Add Tasks Here"
          />
          <button className="todo-add-btn" onClick={createNewTask}>Add</button>
        </div>
      </motion.div>

      <div className="todo-grid">
        {tasks.map((task, index) => (
          <Card
            key={index}
            index={index}
            deleteTask={() => deleteTask(index)}
            number={index + 1}
            description={task}
          />
        ))}
      </div>
    </div>
  );
}

export default App;
