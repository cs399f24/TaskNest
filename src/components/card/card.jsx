import React from 'react';
import './card.css'
import { motion } from 'framer-motion'

// export const Card = (props) => {
//     return (
//         <motion.div
//             className='todo-card'
//             initial={{ opacity: 0, scale: 0 }}
//             animate={{ opacity: 1, scale: 1 }}
//         >
//             <div className='button-container'>
//                 <input className='todo-check-btn' type='checkbox'></input>
//               <button onClick={()=>props.deleteTask(props.index)} className='todo-delete-btn'>X</button>
//             </div>
//             <h3>Task #{props.number}</h3>

//             <div className="todo-card-text">
//                 <p>{props.description}</p>
//             </div>
//             <div className='random-line'></div>
//             <h3 className='due-date-h3'>Due Date: {props.time}</h3>

//         </motion.div>
//     )
// }

export const Card = (props) => {
    return (
        <motion.div
            className='todo-card'
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
        >
            <div className='button-container'>
                <input className='todo-check-btn' type='checkbox'></input>
              <button onClick={()=>props.deleteTask(props.index)} className='todo-delete-btn'>X</button>
            </div>
            <h3>Task #{props.number}</h3>

            <div className="todo-card-text">
                <p>{props.description}</p>
            </div>
        </motion.div>
    )
}