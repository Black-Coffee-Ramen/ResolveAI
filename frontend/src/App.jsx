import React, { useState, useEffect, useCallback } from 'react';
import TicketForm from './components/TicketForm';
import TicketList from './components/TicketList';
import MetricsDashboard from './components/MetricsDashboard';
import TicketDetail from './components/TicketDetail';

const TABS = ['pending', 'all', 'metrics'];

function App() {
  const [tickets, setTickets] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('pending');
  const [selectedTicket, setSelectedTicket] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [ticketsRes, metricsRes] = await Promise.all([
        fetch('/api/tickets'),
        fetch('/api/metrics'),
      ]);
      if (!ticketsRes.ok) throw new Error('Failed to fetch tickets.');
      if (!metricsRes.ok) throw new Error('Failed to fetch metrics.');
      const ticketsData = await ticketsRes.json();
      const metricsData = await metricsRes.json();
      setTickets(ticketsData);
      setMetrics(metricsData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleTicketCreated = (newTicket) => {
    setTickets(prev => [newTicket, ...prev]);
    setActiveTab('pending');
    fetchData(); // refresh metrics too
  };

  const handleTicketUpdated = (updatedTicket) => {
    setTickets(prev => prev.map(t => t.id === updatedTicket.id ? updatedTicket : t));
    setSelectedTicket(null);
    fetchData(); // refresh metrics
  };

  const pendingTickets = tickets.filter(t => t.status === 'pending_approval');
  const displayedTickets = activeTab === 'pending' ? pendingTickets : tickets;

  return (
    <div className="bg-gray-950 min-h-screen text-gray-100 font-sans">
      {/* Header */}
      <header className="bg-gray-900 border-b border-gray-800 shadow-xl">
        <div className="container mx-auto px-6 py-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center shadow-lg">
              <span className="text-white font-bold text-sm">R</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-white leading-tight">ResolveAI</h1>
              <p className="text-xs text-gray-500">Enterprise Support Triage</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {pendingTickets.length > 0 && (
              <span className="px-2.5 py-1 rounded-full bg-amber-500/20 text-amber-400 text-xs font-semibold border border-amber-500/30 animate-pulse">
                {pendingTickets.length} pending review
              </span>
            )}
          </div>
        </div>
      </header>

      <main className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left: Submit form */}
          <div className="lg:col-span-1">
            <TicketForm onTicketCreated={handleTicketCreated} />
          </div>

          {/* Right: Main panel */}
          <div className="lg:col-span-2">
            {/* Tab bar */}
            <div className="flex gap-1 mb-6 bg-gray-900 p-1 rounded-xl border border-gray-800 w-fit">
              {[
                { id: 'pending', label: 'Pending Review', badge: pendingTickets.length },
                { id: 'all', label: 'All Tickets' },
                { id: 'metrics', label: 'Flow Metrics' },
              ].map(tab => (
                <button
                  key={tab.id}
                  onClick={() => { setActiveTab(tab.id); setSelectedTicket(null); }}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
                    activeTab === tab.id
                      ? 'bg-violet-600 text-white shadow-md shadow-violet-900/50'
                      : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800'
                  }`}
                >
                  {tab.label}
                  {tab.badge > 0 && (
                    <span className={`w-5 h-5 rounded-full text-xs flex items-center justify-center font-bold ${
                      activeTab === tab.id ? 'bg-white/20 text-white' : 'bg-amber-500 text-gray-900'
                    }`}>
                      {tab.badge}
                    </span>
                  )}
                </button>
              ))}
            </div>

            {loading && (
              <div className="flex items-center justify-center h-48">
                <div className="w-8 h-8 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
              </div>
            )}
            {error && (
              <div className="bg-red-900/30 border border-red-700/50 rounded-xl p-4 text-red-400 text-sm">{error}</div>
            )}

            {!loading && !error && (
              <>
                {activeTab === 'metrics' ? (
                  <MetricsDashboard metrics={metrics} />
                ) : selectedTicket ? (
                  <TicketDetail
                    ticket={selectedTicket}
                    onBack={() => setSelectedTicket(null)}
                    onUpdated={handleTicketUpdated}
                  />
                ) : (
                  <TicketList
                    tickets={displayedTickets}
                    emptyMessage={
                      activeTab === 'pending'
                        ? 'No tickets awaiting review. The AI pipeline is all caught up! ✓'
                        : 'No tickets submitted yet.'
                    }
                    onSelect={setSelectedTicket}
                  />
                )}
              </>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;