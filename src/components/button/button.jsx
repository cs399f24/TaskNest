import './button.css';
export const Button = (props) => {
    return (
        <button type={props.submit} className="cool-btn">
            {props.text}
        
        </button>
    )
    }


export default Button;