import React from 'react';

// Helper to get colors for different priorities and statuses
const getPriorityColor = (priority) => {
  switch (priority) {
    case 'high':
      return 'bg-red-200 text-red-800';
    case 'medium':
      return 'bg-yellow-200 text-yellow-800';
    default:
      return 'bg-green-200 text-green-800';
  }
};

const getCategoryColor = (category) => {
  switch (category) {
    case 'technical':
      return 'bg-blue-200 text-blue-800';
    case 'billing':
      return 'bg-purple-200 text-purple-800';
    default:
      return 'bg-gray-200 text-gray-800';
  }
};


const TicketItem = ({ ticket }) => {
  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700 mb-6 transition-transform hover:scale-[1.02]">
      {/* Header section with Title and Badges */}
      <div className="flex flex-col sm:flex-row justify-between sm:items-start mb-4">
        <h3 className="text-xl font-bold text-white mb-2 sm:mb-0">{ticket.title}</h3>
        {/* Container for the badges */}
        <div className="flex items-center gap-3 flex-shrink-0 ml-4">
          <span className={`px-3 py-1 text-xs font-bold text-white rounded-full ${getPriorityColor(ticket.priority)}`}>
            {ticket.priority}
          </span>
          <span className={`px-3 py-1 text-xs font-bold text-white rounded-full ${getCategoryColor(ticket.category)}`}>
            {ticket.category}
          </span>
        </div>
      </div>
      
      {/* Description */}
      <p className="text-gray-400 mb-5">{ticket.description}</p>
      
      {/* Resolution/AI Response */}
      {ticket.resolution && (
        <div className="bg-gray-700 p-4 rounded-md border border-gray-600">
            <p className="text-gray-300 font-semibold mb-2 text-sm">AI Response:</p>
            <p className="text-gray-300 whitespace-pre-wrap font-mono text-sm">{ticket.resolution}</p>
        </div>
      )}
    </div>
  );
};

export default TicketItem;

