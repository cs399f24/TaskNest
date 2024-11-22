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
  const API_ID = "nra2caqdd1";
  const stage_name = "prod";

  let backendUrl = `https://${API_ID}.execute-api.${region}.amazonaws.com/${stage_name}`;

  try {
    const EC2_IP = process.env.REACT_APP_EC2_PUBLIC_IP;
    if (EC2_IP) {
      backendUrl = `http://${EC2_IP}:80`;
    }
  } catch (error) {
    console.error('Error setting backend URL:', error);
  }

  useEffect(() => {
    const userId = "b4089458-50e1-70bf-4e54-812dfa914f48";
  
    if (userId) {
      axios
        .get(`${backendUrl}/tasks`, {
          params: { user_id: userId },
          headers: { 'Content-Type': 'application/json' },
        })
        .then(response => {
          let tasks = response.data.body;
          if (typeof tasks === 'string') {
            try {
              tasks = JSON.parse(tasks);
            } catch (e) {
              console.error('Error parsing tasks:', e);
              tasks = [];
            }
          }
          setTasks(tasks);
        })
        .catch(error => console.error('Error fetching tasks:', error));
    } else {
      window.location.href = '/log-in';
    }
  }, []);

  const createNewTask = async () => {
    // const userId = localStorage.getItem("user_id");
    const userId = 'b4089458-50e1-70bf-4e54-812dfa914f48';
  
    if (newTodo !== '' && userId) {
      try {
        console.log(newTodo);
        const response = await axios.post(`${backendUrl}/add`, {
          user_id: userId,
          description: newTodo,
          time: new Date().toISOString()
        }, {
          headers: { 'Content-Type': 'application/json' }
        });
        axios
        .get(`${backendUrl}/tasks`, {
          params: { user_id: userId },
          headers: { 'Content-Type': 'application/json' },
        })
        .then(response => {
          let tasks = response.data.body;
          if (typeof tasks === 'string') {
            try {
              tasks = JSON.parse(tasks);
            } catch (e) {
              console.error('Error parsing tasks:', e);
              tasks = [];
            }
          }
          setTasks(tasks);
        })
        .catch(error => console.error('Error fetching tasks:', error));
      } catch (error) {
        console.error('Error adding task:', error);
      }
    }
  };
  


const deleteTask = async (description) => {
  const userId = localStorage.getItem("user_id");

  if (!userId) {
      console.error('User ID is not available.');
      return;
  }

  try {
      const response = await axios.delete(`${backendUrl}/delete`, {
          params: { user_id: userId, description: description }
      });
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
