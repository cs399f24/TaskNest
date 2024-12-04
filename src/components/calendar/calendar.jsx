import Calendar from 'react-calendar';

function CalendarComponent({ value, onChange }) {
  return (
    <div className='calendar-component'>
      <Calendar onChange={onChange} value={value} />
    </div>
  );
}

export default CalendarComponent;