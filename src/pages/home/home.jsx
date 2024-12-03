import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Card } from '../../components/card/card';
import './home.css';
import { desc } from 'framer-motion/client';

export const Home = () => {
  const [tasks, setTasks] = useState([]);
  const [newTodo, setNewTodo] = useState("");

  const region = "us-east-1";
  const API_ID = "1r0yw16xc5";
  const stage_name = "prod";

  let backendUrl = `https://${API_ID}.execute-api.${region}.amazonaws.com/${stage_name}`;

  useEffect(() => {
    const userId = localStorage.getItem("user_id");
    const accessToken = localStorage.getItem("accessToken");
    const idToken = localStorage.getItem("idToken");
  
    if (userId || accessToken || idToken) {
      fetch(`${backendUrl}/tasks?user_id=${encodeURIComponent(userId)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${idToken}`,
        },
        mode: 'cors',
      })
        .then(async (response) => {
          if (!response.ok) {
            localStorage.clear();
            window.location.href = '/log-in';
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          let tasks = await response.json();
  
          if (typeof tasks.body === 'string') {
            try {
              tasks = JSON.parse(tasks.body);
            } catch (e) {
              console.error('Error parsing tasks:', e);
              tasks = [];
            }
          } else {
            tasks = tasks.body;
          }
          setTasks(tasks);
        })
        .catch((error) => {
          console.error('Error fetching tasks:', error);
        });
    } else {
      window.location.href = '/log-in';
    }
  }, []);
  
  const updateTasks = async () => {
    const accessToken = localStorage.getItem("accessToken");
    const idToken = localStorage.getItem("idToken");
    const userId = localStorage.getItem("user_id");
  
    if (!userId || !accessToken) {
      console.error("User ID is missing. Unable to fetch tasks.");
      return;
    }
  
    try {
      const response = await fetch(`${backendUrl}/tasks?user_id=${encodeURIComponent(userId)}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${idToken}`,
        },
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      let tasks = await response.json();
  
      if (typeof tasks.body === 'string') {
        try {
          tasks = JSON.parse(tasks.body);
        } catch (e) {
          console.error('Error parsing tasks:', e);
          tasks = [];
        }
      } else {
        tasks = tasks.body;
      }
  
      setTasks(tasks);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  const createNewTask = async () => {
    const accessToken = localStorage.getItem("accessToken");
    const idToken = localStorage.getItem("idToken");
    const userId = localStorage.getItem("user_id");
  
    if (newTodo !== '' && userId) {
      try {
        console.log(newTodo);
  
        const response = await fetch(`${backendUrl}/add`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${idToken}`,
          },
          body: JSON.stringify({
            user_id: userId,
            description: newTodo,
            time: new Date().toISOString()
          }),
          mode: 'cors',
        });
  
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
  
        const result = await response.json();
        console.log('Task added successfully:', result);
  
        updateTasks();
      } catch (error) {
        console.error('Error adding task:', error);
      }
    }
  };
  
  const deleteTask = async (description) => {
    const accessToken = localStorage.getItem("accessToken");
    const idToken = localStorage.getItem("idToken");
    const userId = localStorage.getItem("user_id");
    console.log(description);
  
    if (!userId) {
      console.error('User ID is not available.');
      return;
    }
  
    try {
      const url = `${backendUrl}/delete?user_id=${encodeURIComponent(userId)}&description=${encodeURIComponent(description)}`;
  
      const response = await fetch(url, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${idToken}`,
        },
        mode: 'cors',
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      console.log('Task deleted successfully');
      updateTasks();
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
        {tasks.map((task, index) => (
          <Card
            key={index}
            index={index}
            deleteTask={() => deleteTask(task.description)}
            number={index + 1}
            description={task.description}
            time={task.time}
          />
        ))}
      </div>
    </div>
  );
}

export default Home;
