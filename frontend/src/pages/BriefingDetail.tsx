/**
 * Individual briefing detail page
 */
import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { api } from '../services/api';
import type { BriefingDetail } from '../types';

export default function BriefingDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const [briefing, setBriefing] = useState<BriefingDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (slug) {
      loadBriefing(slug);
    }
  }, [slug]);

  const loadBriefing = async (slug: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await api.getBriefing(slug);
      setBriefing(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load briefing');
      console.error('Error loading briefing:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    } catch {
      return dateString;
    }
  };

  const getSourceTypeLabel = (sourceType: string) => {
    switch (sourceType) {
      case 'data_analysis':
        return 'Data Analysis';
      case 'article_summary':
        return 'Article Summary';
      default:
        return sourceType;
    }
  };

  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <p className="mt-4 text-gray-600">Loading briefing...</p>
      </div>
    );
  }

  if (error || !briefing) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded mb-6">
          <p className="text-red-800">{error || 'Briefing not found'}</p>
        </div>
        <Link to="/briefings" className="text-primary-600 hover:text-primary-800">
          ← Back to briefings
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Back Link */}
      <Link
        to="/briefings"
        className="inline-flex items-center text-primary-600 hover:text-primary-800 mb-6"
      >
        <svg
          className="w-4 h-4 mr-2"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 19l-7-7 7-7"
          />
        </svg>
        Back to briefings
      </Link>

      {/* Briefing Content */}
      <article className="bg-white rounded-lg shadow-md p-8">
        {/* Header */}
        <header className="mb-8 border-b border-gray-200 pb-6">
          <div className="flex items-start justify-between mb-4">
            <h1 className="text-3xl font-bold text-gray-900 flex-1">
              {briefing.title}
            </h1>
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800 ml-4">
              {getSourceTypeLabel(briefing.source_type)}
            </span>
          </div>

          <div className="flex items-center gap-4 text-sm text-gray-600">
            <time>{formatDate(briefing.created_at)}</time>
            <span>•</span>
            <span>Reading Level: {briefing.reading_level.replace('_', ' ')}</span>
          </div>

          {/* Tags */}
          {briefing.tags && briefing.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-4">
              {briefing.tags.map((tag, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </header>

        {/* Summary */}
        <div className="mb-8 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
          <p className="text-gray-800 font-medium">{briefing.summary}</p>
        </div>

        {/* Body */}
        <div className="prose prose-blue max-w-none mb-8">
          <ReactMarkdown>{briefing.body}</ReactMarkdown>
        </div>

        {/* Sources */}
        {briefing.source_urls && briefing.source_urls.length > 0 && (
          <div className="mb-8 p-4 bg-gray-50 rounded-lg">
            <h3 className="text-sm font-semibold text-gray-900 mb-2">Sources:</h3>
            <ul className="space-y-1">
              {briefing.source_urls.map((url, index) => (
                <li key={index}>
                  <a
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-primary-700 hover:text-primary-900 underline break-all"
                  >
                    {url}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Disclaimer */}
        <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
          <p className="text-sm text-yellow-900">
            <strong>Disclaimer:</strong> {briefing.disclaimer}
          </p>
        </div>
      </article>
    </div>
  );
}
