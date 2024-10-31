import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Card } from '../../components/card/card';
import './home.css';
import { desc } from 'framer-motion/client';

export const Home = () => {
  const [tasks, setTasks] = useState([]);
  const [newTodo, setNewTodo] = useState("");

  let backendUrl = 'http://localhost:5300';

  try {
    const EC2_IP = process.env.REACT_APP_EC2_PUBLIC_IP;
    if (EC2_IP) {
      backendUrl = `http://${EC2_IP}:80`;
      console.log('Backend URL:', backendUrl); // for dev purposes
    }
  } catch (error) {
    console.error('Error setting backend URL:', error);
  }

  // Fetch tasks on component mount
  useEffect(() => {
    axios.get(`${backendUrl}/tasks`)
      .then(response => setTasks(response.data))
      .catch(error => console.error('Error fetching tasks:', error));
  }, []);

  const createNewTask = async () => {
    if (newTodo !== "") {
      try {
        const response = await axios.post(`${backendUrl}/add`, { description: newTodo, time: new Date().toISOString() });
        setTasks(response.data);
        setNewTodo("");
      } catch (error) {
        console.error('Error adding task:', error);
      }
    }
  };

  const deleteTask = async (index) => {
    try {
      const response = await axios.delete(`${backendUrl}/delete/${index}`);
      setTasks(response.data);
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  return (
    <div className="Home">
  
      <motion.div
        className="todo-task-container"
        initial={{ opacity: 0, y: -100 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 2 }}
      >
        <h2 className="title">Task Manager</h2>
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
        {Object.entries(tasks).map(([description, time], index) => (
          <Card
            key={index}
            index={index}
            deleteTask={() => deleteTask(description)} // Delete the task
            number={index + 1}
            description={description} // Display the task description
          />
        ))}
      </div>
    </div>
  );
}

export default Home;
