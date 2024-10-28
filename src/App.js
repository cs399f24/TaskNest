import logo from './logo.svg';
import './App.css';
import { Card } from './components/card';
import { useState } from 'react';
import { motion } from 'framer-motion'

function App() {

  const [tasks, setTask] = useState([])
  const [newTodo, setNewTodo] = useState("")

  const createNewTask = () => {
    if (newTodo !== "") {
      setTask([...tasks, newTodo])
      setNewTodo("")
    }
  }

  const deleteTask = (index) => {
    setTask((prevTask) => prevTask.filter((_, i) => i !== index));

  }

  return (
    <div className="App">
      <motion.div
        className='todo-task-container'
        initial={{ opacity: 0, y: -100 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 2 }}
      >
        <h2 className='title'>TaskNest</h2>
        <div className='todo-input-div'>
          <input
            className='todo-input'
            type='text'
            onChange={(e) => setNewTodo(e.target.value)}
            value={newTodo}
            placeholder='Add Tasks Here'
          ></input>
          <button className='todo-add-btn' onClick={() => createNewTask()}>Add</button>
        </div>
      </motion.div>

      <div className='todo-grid'>
        {
          tasks.map((task, index) => (
            <Card index={index} deleteTask={deleteTask} number={index + 1} description={task} />
          ))
        }
      </div>
    </div>
  );
}

export default App;
