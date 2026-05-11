import React from 'react';
import { motion } from 'framer-motion';

const getBadgeColor = (type, value) => {
  const colors = {
    priority: {
      high: 'bg-red-100 text-red-800',
      medium: 'bg-yellow-100 text-yellow-800',
      low: 'bg-green-100 text-green-800',
    },
    category: {
      technical: 'bg-indigo-100 text-indigo-800',
      billing: 'bg-purple-100 text-purple-800',
      general: 'bg-pink-100 text-pink-800',
    },
    status: {
      open: 'bg-blue-100 text-blue-800',
      in_progress: 'bg-yellow-100 text-yellow-800',
      resolved: 'bg-green-100 text-green-800',
      closed: 'bg-gray-200 text-gray-700',
    }
  };

  return colors[type]?.[value] || 'bg-gray-100 text-gray-800';
};

const TicketDetails = ({ ticket, onClose }) => {
  if (!ticket) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 backdrop-blur-sm">
      <motion.div
        initial={{ opacity: 0, scale: 0.9, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.9, y: 20 }}
        transition={{ duration: 0.3 }}
        className="bg-white/90 backdrop-blur-xl rounded-2xl shadow-2xl p-8 max-w-2xl w-full mx-4 relative"
      >
        {/* Header */}
        <div className="flex justify-between items-center mb-6 border-b pb-4">
          <h2 className="text-2xl font-bold text-gray-900">{ticket.title}</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-700 text-3xl leading-none"
          >
            &times;
          </button>
        </div>

        {/* Content */}
        <div className="space-y-6 text-gray-700 max-h-[60vh] overflow-y-auto pr-2">
          <div>
            <h4 className="font-semibold text-gray-900">Description</h4>
            <p className="pl-2 mt-1 text-gray-600">{ticket.description}</p>
          </div>

          <div className="flex flex-wrap gap-3">
            <span
              className={`px-3 py-1 rounded-full text-sm font-medium capitalize ${getBadgeColor('category', ticket.category)}`}
            >
              {ticket.category}
            </span>
            <span
              className={`px-3 py-1 rounded-full text-sm font-medium capitalize ${getBadgeColor('priority', ticket.priority)}`}
            >
              {ticket.priority}
            </span>
            <span
              className={`px-3 py-1 rounded-full text-sm font-medium capitalize ${getBadgeColor('status', ticket.status)}`}
            >
              {ticket.status.replace('_', ' ')}
            </span>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg border">
            <h4 className="font-semibold text-gray-900">AI Agent Resolution</h4>
            <p className="pl-2 mt-2 text-gray-600">{ticket.resolution}</p>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 text-right">
          <button
            onClick={onClose}
            className="bg-gradient-to-r from-gray-600 to-gray-800 text-white font-semibold py-2 px-6 rounded-lg hover:from-gray-700 hover:to-black transition duration-300 shadow-md"
          >
            Close
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default TicketDetails;
