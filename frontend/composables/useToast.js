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
          icon: {
            className: 'notyf-icon',
            tagName: 'i',
            text: '', // Clear text
            html: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="white" width="24" height="24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>',
          },
        },
        {
          type: 'error',
          background: '#EF4444',
          icon: {
            className: 'notyf-icon',
            tagName: 'i',
            text: '', // Clear text
            html: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="white" width="24" height="24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>',
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
