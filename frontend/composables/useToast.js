import { Notyf } from 'notyf';
import 'notyf/notyf.min.css';

let notyfInstance = null;

export const useToast = () => {
  // Ensure we are on the client side before initializing Notyf
  if (process.client && !notyfInstance) {
    notyfInstance = new Notyf({
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
  }

  return {
    success: (message) => {
      if (process.client && notyfInstance) notyfInstance.success(message);
    },
    error: (message) => {
      if (process.client && notyfInstance) notyfInstance.error(message);
    },
    info: (message) => {
      if (process.client && notyfInstance) notyfInstance.open({ type: 'info', message });
    },
  };
};
