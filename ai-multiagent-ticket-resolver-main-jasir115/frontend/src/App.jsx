import React, { useState, useEffect } from 'react';
import TicketForm from './components/TicketForm';
import TicketList from './components/TicketList';

function App() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTickets = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`/api/tickets`);
        if (!response.ok) throw new Error('Could not fetch tickets from the server.');
        const data = await response.json();
        setTickets(data.sort((a, b) => b.id - a.id)); // newest first
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchTickets();
  }, []);

  const handleTicketCreated = (newTicket) => {
    // Add the new ticket to the top of the list
    setTickets(prev => [newTicket, ...prev]);
  };

  return (
    <div className="bg-gray-900 min-h-screen text-gray-100 font-sans">
      <header className="bg-gray-800 shadow-md">
        <div className="container mx-auto px-4 py-6 text-center">
          <h1 className="text-4xl font-bold text-white">AI Multi-Agent Ticket Resolver</h1>
          <p className="text-gray-400 mt-2">Submit a ticket and let our AI agents handle it.</p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-10">
        <TicketForm onTicketCreated={handleTicketCreated} />

        <div className="mt-12">
          {loading && <p className="text-center text-gray-400">Loading tickets...</p>}
          {error && <p className="text-center text-red-500 font-semibold">{error}</p>}
          
          {!loading && !error && (
            <TicketList tickets={tickets} />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;