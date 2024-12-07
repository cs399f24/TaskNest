import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card } from '../../components/card/card';
import './home.css';
import CalendarComponent from '../../components/calendar/calendar';
import 'react-calendar/dist/Calendar.css';


export const Home = () => {
  const [tasks, setTasks] = useState([]);
  const [newTodo, setNewTodo] = useState("");
  const [value, onChange] = useState(new Date());
  const [calendar, showCalendar] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const region = "us-east-1";
  const API_ID = process.env.REACT_APP_API_ID ? process.env.REACT_APP_API_ID : "y0opv3uf4c";
  const stage_name = "prod";

  let backendUrl = `https://${API_ID}.execute-api.${region}.amazonaws.com/${stage_name}`;

  useEffect(() => {
    const userId = localStorage.getItem("user_id");
    const idToken = localStorage.getItem("idToken");

    setIsLoading(true);
    if (userId || idToken) {
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
    setIsLoading(false);
  }, []);

  const calendarToggle = () => {
    showCalendar(!calendar);
  };

  const updateTasks = async () => {
    const idToken = localStorage.getItem("idToken");
    const userId = localStorage.getItem("user_id");

    setIsLoading(true);
    if (!userId) {
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
    setIsLoading(false);
  };

  const createNewTask = async () => {
    const idToken = localStorage.getItem("idToken");
    const userId = localStorage.getItem("user_id");

    const time = value.getTime();
    console.log('Time:', time);
    const timeAdj = new Date(time).toISOString().replace('Z', '');

    setIsLoading(true);
    if (newTodo !== '' && userId) {
      try {
        const response = await fetch(`${backendUrl}/add`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${idToken}`,
          },
          body: JSON.stringify({
            user_id: userId,
            description: newTodo,
            time: timeAdj,
            idToken: idToken
          }),
          mode: 'cors',
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Task added successfully:', result);
        setNewTodo("");
        updateTasks();
      } catch (error) {
        console.error('Error adding task:', error);
      }
    }
    setIsLoading(false);
  };

  const deleteTask = async (description) => {
    const idToken = localStorage.getItem("idToken");
    const userId = localStorage.getItem("user_id");

    setIsLoading(true);
    if (!userId) {
      console.error('User ID is not available.');
      return;
    }

    try {
      const url = `${backendUrl}/delete?user_id=${encodeURIComponent(userId)}&description=${encodeURIComponent(description)}`;

      const response = await fetch(url, {
        method: 'POST',
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
    setIsLoading(false);
  };

  return (
    <div className='Home' style={{cursor: isLoading ? "wait" : "default"}}>
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
          
          <div className='btn-flex-ct'>
            <button className="todo-add-btn" onClick={createNewTask}>Add</button>
            <button onClick={calendarToggle} className='todo-calendar-btn'>Date</button>
          </div>

          {calendar && <motion.div
          className='calendar-container'
            initial={{ opacity: 0.5, scale: 1, y: -50 }}
            animate={{ opacity: 1, scale: 1, y: 10 }}
            transition={{ duration: 0.8 }}
          > <CalendarComponent value={value} onChange={onChange} />
          </motion.div>}
        </div>
      </motion.div>

      <div className="todo-grid">
        {tasks.map((task, index) => {
          const dueDate = new Date(task.time).toLocaleDateString('en-US', {
            month: '2-digit',
            day: '2-digit',
            year: 'numeric',
          });
          return (
            <Card
              key={index}
              number={index + 1}
              deleteTask={() => deleteTask(task.description)}
              description={task.description}
              time={dueDate}
            />
          );
        })}
      </div>
    </div>
  );
}

export default Home;