import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Card } from '../../components/card/card';
import { fetchAuthSession } from 'aws-amplify/auth';
import './home.css';

export const Home = () => {
  const [tasks, setTasks] = useState([]);
  const [newTodo, setNewTodo] = useState("");
  const [authToken, setAuthToken] = useState(null);

  const region = "us-east-1";
  const API_ID = "nra2caqdd1";
  const stage_name = "prod";

  let backendUrl = `https://${API_ID}.execute-api.${region}.amazonaws.com/${stage_name}`;

  // Get auth token on component mount
  useEffect(() => {
    const getAuthToken = async () => {
      try {
        const session = await fetchAuthSession();
        const token = session.tokens.idToken.toString();
        setAuthToken(token);
        // Once we have the token, fetch tasks
        fetchTasks(token);
      } catch (error) {
        console.error('Error getting authentication token:', error);
        // Redirect to login if auth fails
        window.location.href = '/log-in';
      }
    };

    getAuthToken();
  }, []);

  const fetchTasks = async (token) => {
    try {
      const response = await axios.get(`${backendUrl}/tasks`, {
        headers: {
          'Authorization': token,
          'Content-Type': 'application/json'
        }
      });
      
      let tasks = response.data.body;
      if (typeof tasks === 'string') {
        tasks = JSON.parse(tasks);
      }
      setTasks(tasks);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      if (error.response?.status === 401) {
        window.location.href = '/log-in';
      }
    }
  };

  const updateTasks = async () => {
    if (authToken) {
      await fetchTasks(authToken);
    }
  };

  const createNewTask = async () => {
    if (newTodo !== '' && authToken) {
      try {
        await axios.post(`${backendUrl}/add`, {
          description: newTodo,
          time: new Date().toISOString()
        }, {
          headers: {
            'Authorization': authToken,
            'Content-Type': 'application/json'
          }
        });
        await updateTasks();
        setNewTodo(""); // Clear input after successful creation
      } catch (error) {
        console.error('Error adding task:', error);
        if (error.response?.status === 401) {
          window.location.href = '/log-in';
        }
      }
    }
  };

  const deleteTask = async (description) => {
    if (!authToken) {
      console.error('Not authenticated');
      return;
    }

    try {
      await axios.delete(`${backendUrl}/delete`, {
        params: { description },
        headers: {
          'Authorization': authToken
        }
      });
      await updateTasks();
    } catch (error) {
      console.error('Error deleting task:', error);
      if (error.response?.status === 401) {
        window.location.href = '/log-in';
      }
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
};

export default Home;