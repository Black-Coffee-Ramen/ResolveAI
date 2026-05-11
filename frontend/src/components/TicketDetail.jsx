import React, { useState } from 'react';

const PRIORITY_BADGE = {
  high: 'bg-red-500/15 text-red-400 border-red-500/30',
  medium: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
  low: 'bg-gray-700/30 text-gray-400 border-gray-700/40',
};

const STATUS_BADGE = {
  pending_approval: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
  resolved: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
  escalated: 'bg-red-500/15 text-red-400 border-red-500/30',
  rejected: 'bg-gray-600/30 text-gray-400 border-gray-600/40',
};

function formatStatus(s) {
  return s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

export default function TicketDetail({ ticket, onBack, onUpdated }) {
  const [editedResolution, setEditedResolution] = useState(ticket.resolution || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const isPending = ticket.status === 'pending_approval';

  const handleApprove = async (useEdited = false) => {
    setLoading(true);
    setError(null);
    try {
      const body = useEdited ? { final_resolution: editedResolution } : {};
      const res = await fetch(`/api/tickets/${ticket.id}/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error('Failed to approve ticket.');
      const updated = await res.json();
      onUpdated(updated);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReject = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/tickets/${ticket.id}/reject`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      });
      if (!res.ok) throw new Error('Failed to reject ticket.');
      const updated = await res.json();
      onUpdated(updated);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const wasEdited = editedResolution.trim() !== (ticket.resolution || '').trim();

  return (
    <div className="space-y-5">
      {/* Header row */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors"
        >
          ← Back
        </button>
        <div className="flex gap-2">
          <span className={`px-2.5 py-1 rounded-full text-xs font-medium border ${PRIORITY_BADGE[ticket.priority] || ''}`}>
            {ticket.priority?.toUpperCase()} priority
          </span>
          <span className={`px-2.5 py-1 rounded-full text-xs font-medium border ${STATUS_BADGE[ticket.status] || ''}`}>
            {formatStatus(ticket.status)}
          </span>
        </div>
      </div>

      {/* Ticket info */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <div className="flex items-start justify-between gap-4 mb-3">
          <div>
            <p className="text-xs text-gray-500 mb-1">#{ticket.id} · {ticket.category}</p>
            <h2 className="text-lg font-bold text-white">{ticket.title}</h2>
          </div>
        </div>
        <p className="text-sm text-gray-300 leading-relaxed">{ticket.description}</p>
      </div>

      {/* RAG Context retrieved */}
      {ticket.rag_context && ticket.rag_context !== 'No relevant documentation found.' && (
        <div className="bg-gray-900 border border-indigo-800/40 rounded-xl p-5">
          <p className="text-xs font-semibold text-indigo-400 mb-2 uppercase tracking-wider">📚 Retrieved Knowledge Base Context</p>
          <pre className="text-xs text-gray-400 whitespace-pre-wrap leading-relaxed font-mono overflow-auto max-h-40">
            {ticket.rag_context}
          </pre>
        </div>
      )}

      {/* AI Draft Response */}
      <div className="bg-gray-900 border border-violet-800/40 rounded-xl p-5">
        <div className="flex items-center justify-between mb-3">
          <p className="text-xs font-semibold text-violet-400 uppercase tracking-wider">🤖 AI Draft Response</p>
          {!isPending && ticket.was_edited === 'true' && (
            <span className="text-xs text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded-full border border-amber-500/20">
              edited before approval
            </span>
          )}
          {!isPending && ticket.was_edited === 'false' && (
            <span className="text-xs text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
              approved as-is ✓
            </span>
          )}
        </div>
        {isPending ? (
          <textarea
            value={editedResolution}
            onChange={e => setEditedResolution(e.target.value)}
            rows={6}
            className="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-sm text-gray-200 focus:outline-none focus:border-violet-500 resize-none leading-relaxed"
          />
        ) : (
          <p className="text-sm text-gray-300 leading-relaxed whitespace-pre-wrap">{ticket.resolution}</p>
        )}
      </div>

      {/* HITL Action buttons */}
      {isPending && (
        <div className="flex flex-col sm:flex-row gap-3">
          {wasEdited ? (
            <button
              onClick={() => handleApprove(true)}
              disabled={loading}
              className="flex-1 py-2.5 px-4 rounded-lg bg-violet-600 hover:bg-violet-500 text-white text-sm font-semibold transition-colors disabled:opacity-50"
            >
              {loading ? '...' : '✏️ Approve with Edits'}
            </button>
          ) : (
            <button
              onClick={() => handleApprove(false)}
              disabled={loading}
              className="flex-1 py-2.5 px-4 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-semibold transition-colors disabled:opacity-50"
            >
              {loading ? '...' : '✓ Approve AI Draft'}
            </button>
          )}
          <button
            onClick={handleReject}
            disabled={loading}
            className="flex-1 py-2.5 px-4 rounded-lg bg-gray-800 hover:bg-red-900/40 text-gray-300 hover:text-red-400 border border-gray-700 hover:border-red-700/50 text-sm font-semibold transition-all disabled:opacity-50"
          >
            {loading ? '...' : '✕ Reject — Escalate Manually'}
          </button>
        </div>
      )}

      {error && (
        <div className="bg-red-900/30 border border-red-700/50 rounded-lg p-3 text-red-400 text-sm">{error}</div>
      )}
    </div>
  );
}
