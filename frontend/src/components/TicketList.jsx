import React, { useState } from 'react';

const STATUS_STYLES = {
  pending_approval: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
  resolved: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
  escalated: 'bg-red-500/15 text-red-400 border-red-500/30',
  rejected: 'bg-gray-600/30 text-gray-400 border-gray-600/40',
  open: 'bg-blue-500/15 text-blue-400 border-blue-500/30',
  in_progress: 'bg-violet-500/15 text-violet-400 border-violet-500/30',
};

const PRIORITY_STYLES = {
  high: 'text-red-400',
  medium: 'text-amber-400',
  low: 'text-gray-400',
};

const CATEGORY_ICON = {
  billing: '💳',
  technical: '⚙️',
  general: '📋',
};

function formatStatus(s) {
  return s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

function timeAgo(dateStr) {
  if (!dateStr) return '';
  const diff = (Date.now() - new Date(dateStr + 'Z').getTime()) / 1000;
  if (diff < 60) return `${Math.round(diff)}s ago`;
  if (diff < 3600) return `${Math.round(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.round(diff / 3600)}h ago`;
  return `${Math.round(diff / 86400)}d ago`;
}

export default function TicketList({ tickets, emptyMessage, onSelect }) {
  if (!tickets || tickets.length === 0) {
    return (
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-12 text-center">
        <p className="text-gray-500 text-sm">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tickets.map(ticket => (
        <button
          key={ticket.id}
          onClick={() => onSelect(ticket)}
          className="w-full text-left bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-violet-700/60 hover:bg-gray-900/80 transition-all group"
        >
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs text-gray-500">#{ticket.id}</span>
                <span className="text-xs">{CATEGORY_ICON[ticket.category] || '📋'}</span>
                <span className={`text-xs font-semibold ${PRIORITY_STYLES[ticket.priority]}`}>
                  {ticket.priority?.toUpperCase()}
                </span>
              </div>
              <p className="text-sm font-semibold text-white truncate group-hover:text-violet-300 transition-colors">
                {ticket.title}
              </p>
              <p className="text-xs text-gray-500 mt-1 line-clamp-1">{ticket.description}</p>
            </div>
            <div className="flex flex-col items-end gap-2 shrink-0">
              <span className={`px-2 py-0.5 rounded-full text-xs font-medium border ${STATUS_STYLES[ticket.status] || ''}`}>
                {formatStatus(ticket.status)}
              </span>
              <span className="text-xs text-gray-600">{timeAgo(ticket.created_at)}</span>
            </div>
          </div>
        </button>
      ))}
    </div>
  );
}