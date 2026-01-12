import { Notyf } from 'notyf';
import 'notyf/notyf.min.css';

const notyf = new Notyf({
  duration: 3000,
  position: {
    x: 'right',
    y: 'top',
  },
  types: [
    {
      type: 'success',
      background: '#10B981', // Tailwind green-500
      icon: {
        className: 'material-icons',
        tagName: 'i',
        text: 'check_circle',
        color: 'white',
      },
    },
    {
      type: 'error',
      background: '#EF4444', // Tailwind red-500
      icon: {
        className: 'material-icons',
        tagName: 'i',
        text: 'error',
        color: 'white',
      },
    },
  ],
});

export const useToast = () => {
  return {
    success: (message) => notyf.success(message),
    error: (message) => notyf.error(message),
    info: (message) => notyf.open({ type: 'info', message }),
  };
};
