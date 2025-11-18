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
    <div className="space-y-10">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">Health Briefings</h1>
        <p className="text-lg md:text-xl text-gray-600 max-w-2xl mx-auto">
          AI-powered summaries of health trends and recent research from trusted sources
        </p>
      </div>

      {/* Stats Bar */}
      <div className="card bg-gradient-soft">
        <div className="flex flex-wrap items-center justify-center gap-6 md:gap-12">
          <div className="text-center">
            <p className="text-3xl font-bold text-primary-600">{total}</p>
            <p className="text-sm text-gray-600 mt-1">Total Briefings</p>
          </div>
          <div className="h-12 w-px bg-gray-300"></div>
          <div className="text-center">
            <p className="text-3xl font-bold text-accent-600">5</p>
            <p className="text-sm text-gray-600 mt-1">Reading Levels</p>
          </div>
          <div className="h-12 w-px bg-gray-300"></div>
          <div className="text-center">
            <p className="text-3xl font-bold text-teal-600">Daily</p>
            <p className="text-sm text-gray-600 mt-1">Updates</p>
          </div>
        </div>
      </div>

      {/* Filters - Pill-shaped */}
      <div className="card">
        <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
          <span className="text-sm font-semibold text-gray-700 flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            Filter:
          </span>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => {
                setFilter('all');
                setPage(0);
              }}
              className={`px-5 py-2 rounded-pill text-sm font-medium transition-all duration-slow ${
                filter === 'all'
                  ? 'bg-primary-600 text-white shadow-soft-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              All Briefings
            </button>
            <button
              onClick={() => {
                setFilter('data_analysis');
                setPage(0);
              }}
              className={`px-5 py-2 rounded-pill text-sm font-medium transition-all duration-slow ${
                filter === 'data_analysis'
                  ? 'bg-primary-600 text-white shadow-soft-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              📊 Data Analysis
            </button>
            <button
              onClick={() => {
                setFilter('article_summary');
                setPage(0);
              }}
              className={`px-5 py-2 rounded-pill text-sm font-medium transition-all duration-slow ${
                filter === 'article_summary'
                  ? 'bg-primary-600 text-white shadow-soft-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              📰 Article Summaries
            </button>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="card-lg text-center py-16">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-4 border-primary-200 border-t-primary-600"></div>
          <p className="mt-6 text-lg text-gray-600 font-medium">Loading briefings...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="card bg-red-50 border-l-4 border-red-500">
          <div className="flex items-start gap-3">
            <svg className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <p className="font-semibold text-red-900">Error Loading Briefings</p>
              <p className="text-red-800 mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Briefings List */}
      {!isLoading && !error && (
        <>
          {briefings.length === 0 ? (
            <div className="card-lg text-center py-16">
              <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gray-100 flex items-center justify-center">
                <svg className="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <p className="text-xl text-gray-600 font-medium">No briefings found</p>
              <p className="text-gray-500 mt-2">Try adjusting your filters</p>
            </div>
          ) : (
            <div className="space-y-6">
              {briefings.map((briefing) => (
                <div key={briefing.id} className="card-hover">
                  <BriefingCard briefing={briefing} />
                </div>
              ))}
            </div>
          )}

          {/* Pagination - Modern pill design */}
          {totalPages > 1 && (
            <div className="card flex flex-col sm:flex-row justify-center items-center gap-4">
              <button
                onClick={() => setPage((p) => Math.max(0, p - 1))}
                disabled={page === 0}
                className={`px-6 py-2.5 rounded-pill font-medium transition-all duration-slow flex items-center gap-2 ${
                  page === 0
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white border-2 border-gray-200 text-gray-700 hover:border-primary-500 hover:text-primary-600 hover:shadow-soft'
                }`}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Previous
              </button>
              <div className="flex items-center gap-2">
                <span className="text-gray-600">Page</span>
                <span className="px-4 py-2 bg-primary-100 text-primary-700 font-semibold rounded-pill">
                  {page + 1}
                </span>
                <span className="text-gray-600">of {totalPages}</span>
              </div>
              <button
                onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
                disabled={page >= totalPages - 1}
                className={`px-6 py-2.5 rounded-pill font-medium transition-all duration-slow flex items-center gap-2 ${
                  page >= totalPages - 1
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white border-2 border-gray-200 text-gray-700 hover:border-primary-500 hover:text-primary-600 hover:shadow-soft'
                }`}
              >
                Next
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
