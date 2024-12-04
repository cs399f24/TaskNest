import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Card } from '../../components/card/card';
import './home.css';
import { desc } from 'framer-motion/client';
import CalendarComponent from '../../components/calendar/calendar';
import 'react-calendar/dist/Calendar.css';


export const Home = () => {
  const [tasks, setTasks] = useState([]);
  const [newTodo, setNewTodo] = useState("");
  const [value, onChange] = useState(new Date());
  const [calendar, showCalendar] = useState(false);


  const region = "us-east-1";
  const API_ID = "1r0yw16xc5";
  const stage_name = "prod";

  let backendUrl = `https://${API_ID}.execute-api.${region}.amazonaws.com/${stage_name}`;

  console.log(value)

  const calendarToggle = () => {
    showCalendar(!calendar);
  }

  useEffect(() => {
    const userId = localStorage.getItem("user_id");
    const accessToken = localStorage.getItem("accessToken");
    const idToken = localStorage.getItem("idToken");
    const emailToken = localStorage.getItem("email");

    if (emailToken && userId && idToken) {
      autoSubscribeToSNS(emailToken, userId, idToken);
    }

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

  const autoSubscribeToSNS = async (email, userId, idToken) => {
    try {
      const response = await fetch(`${backendUrl}/subscribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${idToken}`,
        },
        body: JSON.stringify({
          user_id: userId,
          email: email
        }),
        mode: 'cors',
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      console.log('Successfully subscribed to notifications');
    } catch (error) {
      console.error('Error subscribing to notifications:', error);
    }
  };

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
    const emailToken = localStorage.getItem("email");

    const currentDate = new Date();
    console.log('Current date:', currentDate);
    const timeDifference = value.getTime() - currentDate.getTime();
    console.log('Time difference:', timeDifference);
    const adjustedDate = new Date(currentDate.getTime() + timeDifference);
    console.log('Adjusted date:', adjustedDate);

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
            time: adjustedDate,
            email: emailToken
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
  };

  const deleteTask = async (description) => {
    const accessToken = localStorage.getItem("accessToken");
    const idToken = localStorage.getItem("idToken");
    const userId = localStorage.getItem("user_id");

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
          </motion.div>
          }
        </div>
      </motion.div>

      <div className="todo-grid">
        {tasks.map((task, index) => {
          // Calculate the difference in days between the current date and the task date
          const taskDate = new Date(task.time);
          const currentDate = new Date();
          const timeDifference = taskDate - currentDate;
          const daysRemaining = Math.ceil(timeDifference / (1000 * 60 * 60 * 24)); // Convert milliseconds to days

          return (
            <Card
              number={index + 1}
              deleteTask={() => deleteTask(task.description)}
              description={task.description}
              time={daysRemaining > 0
                ? `${daysRemaining} day${daysRemaining > 1 ? 's' : ''} left`
                : 'Due today or overdue'}
            />
          );
        })}
      </div>

    </div>
  );
}

export default Home;