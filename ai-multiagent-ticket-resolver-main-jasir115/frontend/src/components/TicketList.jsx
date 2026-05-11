import React from 'react';
import TicketItem from './TicketItem'; 

const TicketList = ({ tickets }) => {
  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold mb-6 text-white border-b border-gray-700 pb-2">
        Submitted Tickets
      </h2>
      {tickets.length > 0 ? (
        tickets.map(ticket => (
          <TicketItem key={ticket.id} ticket={ticket} />
        ))
      ) : (
        <p className="text-gray-500 text-center py-8">No tickets submitted yet.</p>
      )}
    </div>
  );
};

export default TicketList;