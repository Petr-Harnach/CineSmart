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
          background: '#10B981',
          icon: false, // No icon for cleaner look
        },
        {
          type: 'error',
          background: '#EF4444',
          icon: false, // No icon
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
