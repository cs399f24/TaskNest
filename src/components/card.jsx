import React from 'react';
import './card.css'
import {motion} from 'framer-motion'

export const Card = (props) => {
    return (
        <motion.div 
        className='todo-card'
        initial={{ opacity: 0, scale: 0 }}
        animate={{ opacity: 1, scale: 1 }}
        >
            <h3>{props.number}</h3>

            <div className="todo-card-text">
                <p>{props.description}</p>

            </div>
        </motion.div>
    )
}