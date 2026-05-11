import React from 'react';

function StatCard({ label, value, sub, color = 'text-white', icon }) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
      <div className="flex items-start justify-between">
        <p className="text-xs text-gray-500 uppercase tracking-wider font-medium">{label}</p>
        <span className="text-lg">{icon}</span>
      </div>
      <p className={`text-3xl font-bold mt-2 ${color}`}>{value ?? '—'}</p>
      {sub && <p className="text-xs text-gray-500 mt-1">{sub}</p>}
    </div>
  );
}

function BarSegment({ label, value, total, color }) {
  const pct = total > 0 ? Math.round((value / total) * 100) : 0;
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs text-gray-400">
        <span>{label}</span>
        <span className="font-mono">{value} ({pct}%)</span>
      </div>
      <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full transition-all duration-700 ${color}`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

function formatSeconds(s) {
  if (s === null || s === undefined) return '—';
  if (s < 60) return `${s.toFixed(1)}s`;
  if (s < 3600) return `${(s / 60).toFixed(1)}m`;
  return `${(s / 3600).toFixed(1)}h`;
}

function formatRate(r) {
  if (r === null || r === undefined) return '—';
  return `${Math.round(r * 100)}%`;
}

export default function MetricsDashboard({ metrics }) {
  if (!metrics) {
    return (
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-12 text-center">
        <p className="text-gray-500 text-sm">No metrics available yet. Submit a ticket to get started.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-base font-bold text-white mb-1">Flow Metrics Dashboard</h2>
        <p className="text-xs text-gray-500">Real-time operational intelligence for the AI triage pipeline.</p>
      </div>

      {/* Key metric cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          label="Total Tickets"
          value={metrics.total_tickets}
          icon="🎫"
          color="text-white"
        />
        <StatCard
          label="Pending Review"
          value={metrics.pending_approval}
          sub="awaiting human approval"
          icon="⏳"
          color="text-amber-400"
        />
        <StatCard
          label="Avg. Time to Triage"
          value={formatSeconds(metrics.avg_time_to_triage_seconds)}
          sub="ticket creation → AI draft ready"
          icon="⚡"
          color="text-violet-400"
        />
        <StatCard
          label="Escalation Rate"
          value={formatRate(metrics.escalation_rate)}
          sub="safety precheck triggers"
          icon="🛡️"
          color={metrics.escalation_rate > 0.3 ? 'text-red-400' : 'text-emerald-400'}
        />
      </div>

      {/* Status breakdown */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-4">Ticket Status Breakdown</p>
        <div className="space-y-3">
          <BarSegment label="Resolved" value={metrics.resolved} total={metrics.total_tickets} color="bg-emerald-500" />
          <BarSegment label="Pending Approval" value={metrics.pending_approval} total={metrics.total_tickets} color="bg-amber-500" />
          <BarSegment label="Escalated (Safety)" value={metrics.escalated} total={metrics.total_tickets} color="bg-red-500" />
          <BarSegment label="Rejected by Analyst" value={metrics.rejected} total={metrics.total_tickets} color="bg-gray-500" />
        </div>
      </div>

      {/* AI Accuracy proxy */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">AI Draft Acceptance Rate</p>
        <p className="text-xs text-gray-600 mb-4">Ratio of tickets where the analyst approved the AI draft without edits — a proxy for classification accuracy.</p>
        
        {metrics.approval_without_edit_rate !== null ? (
          <div className="space-y-2">
            <div className="flex items-end justify-between">
              <span className={`text-4xl font-bold ${
                metrics.approval_without_edit_rate >= 0.7 ? 'text-emerald-400' :
                metrics.approval_without_edit_rate >= 0.4 ? 'text-amber-400' : 'text-red-400'
              }`}>
                {formatRate(metrics.approval_without_edit_rate)}
              </span>
              <span className="text-xs text-gray-500 mb-1">
                {metrics.approval_without_edit_rate >= 0.7 ? '✓ High confidence' :
                 metrics.approval_without_edit_rate >= 0.4 ? '⚠ Needs review' : '⚠ Low confidence'}
              </span>
            </div>
            <div className="h-3 bg-gray-800 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-700 ${
                  metrics.approval_without_edit_rate >= 0.7 ? 'bg-emerald-500' :
                  metrics.approval_without_edit_rate >= 0.4 ? 'bg-amber-500' : 'bg-red-500'
                }`}
                style={{ width: `${Math.round(metrics.approval_without_edit_rate * 100)}%` }}
              />
            </div>
          </div>
        ) : (
          <p className="text-sm text-gray-500">Approve or reject tickets to generate this metric.</p>
        )}
      </div>
    </div>
  );
}
