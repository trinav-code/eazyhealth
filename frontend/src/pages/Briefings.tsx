/**
 * Briefings list page with filtering and pagination
 */
import { useState, useEffect } from 'react';
import { api } from '../services/api';
import BriefingCard from '../components/BriefingCard';
import type { BriefingListItem } from '../types';

export default function Briefings() {
  const [briefings, setBriefings] = useState<BriefingListItem[]>([]);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'data_analysis' | 'article_summary'>('all');
  const [page, setPage] = useState(0);
  const pageSize = 10;

  useEffect(() => {
    loadBriefings();
  }, [filter, page]);

  const loadBriefings = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await api.getBriefings({
        limit: pageSize,
        offset: page * pageSize,
        source_type: filter !== 'all' ? filter : undefined,
      });

      setBriefings(response.items);
      setTotal(response.total);
    } catch (err: any) {
      setError(err.message || 'Failed to load briefings');
      console.error('Error loading briefings:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Health Briefings</h1>
        <p className="text-gray-600">
          Auto-generated summaries of health trends and recent research
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm p-4">
        <div className="flex items-center gap-4">
          <span className="text-sm font-medium text-gray-700">Filter by type:</span>
          <div className="flex gap-2">
            <button
              onClick={() => {
                setFilter('all');
                setPage(0);
              }}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                filter === 'all'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              All
            </button>
            <button
              onClick={() => {
                setFilter('data_analysis');
                setPage(0);
              }}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                filter === 'data_analysis'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Data Analysis
            </button>
            <button
              onClick={() => {
                setFilter('article_summary');
                setPage(0);
              }}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                filter === 'article_summary'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Article Summaries
            </button>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="mt-4 text-gray-600">Loading briefings...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Briefings List */}
      {!isLoading && !error && (
        <>
          {briefings.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-lg shadow-sm">
              <p className="text-gray-600">No briefings found.</p>
            </div>
          ) : (
            <div className="space-y-6">
              {briefings.map((briefing) => (
                <BriefingCard key={briefing.id} briefing={briefing} />
              ))}
            </div>
          )}

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex justify-center items-center gap-4 mt-8">
              <button
                onClick={() => setPage((p) => Math.max(0, p - 1))}
                disabled={page === 0}
                className="px-4 py-2 rounded-md bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <span className="text-sm text-gray-600">
                Page {page + 1} of {totalPages}
              </span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
                disabled={page >= totalPages - 1}
                className="px-4 py-2 rounded-md bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
