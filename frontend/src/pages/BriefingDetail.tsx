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
      <div className="card-lg text-center py-20">
        <div className="inline-block animate-spin rounded-full h-16 w-16 border-4 border-primary-200 border-t-primary-600"></div>
        <p className="mt-6 text-lg text-gray-600 font-medium">Loading briefing...</p>
      </div>
    );
  }

  if (error || !briefing) {
    return (
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="card bg-red-50 border-l-4 border-red-500">
          <div className="flex items-start gap-3">
            <svg className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <p className="font-semibold text-red-900">Error</p>
              <p className="text-red-800 mt-1">{error || 'Briefing not found'}</p>
            </div>
          </div>
        </div>
        <Link to="/briefings" className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium transition-colors group">
          <svg className="w-5 h-5 transition-transform group-hover:-translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to briefings
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Back Link */}
      <Link
        to="/briefings"
        className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium transition-all duration-slow group"
      >
        <svg
          className="w-5 h-5 transition-transform duration-slow group-hover:-translate-x-1"
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
        Back to all briefings
      </Link>

      {/* Briefing Content */}
      <article className="card-lg shadow-floating">
        {/* Header */}
        <header className="mb-10 pb-8 border-b border-gray-200">
          {/* Meta info - Type and Reading Level */}
          <div className="flex flex-wrap items-center gap-3 mb-6">
            <span className="tag tag-primary">
              {getSourceTypeLabel(briefing.source_type)}
            </span>
            <span className="tag tag-teal">
              📚 {briefing.reading_level.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </span>
            <span className="text-gray-400">•</span>
            <time className="text-sm text-gray-600">{formatDate(briefing.created_at)}</time>
          </div>

          {/* Title */}
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6 leading-tight">
            {briefing.title}
          </h1>

          {/* Tags */}
          {briefing.tags && briefing.tags.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {briefing.tags.map((tag, index) => (
                <span key={index} className="tag tag-gray">
                  {tag}
                </span>
              ))}
            </div>
          )}
        </header>

        {/* Summary - Highlighted */}
        <div className="mb-10 p-6 rounded-card bg-gradient-soft border-l-4 border-primary-500">
          <div className="flex items-start gap-3">
            <svg className="w-6 h-6 text-primary-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <h2 className="text-sm font-semibold text-primary-900 uppercase tracking-wide mb-2">Quick Summary</h2>
              <p className="text-gray-800 text-lg leading-relaxed">{briefing.summary}</p>
            </div>
          </div>
        </div>

        {/* Body - Markdown content */}
        <div className="prose max-w-none mb-10">
          <ReactMarkdown>{briefing.body}</ReactMarkdown>
        </div>

        {/* Sources Section */}
        {briefing.source_urls && briefing.source_urls.length > 0 && (
          <div className="mb-8 p-6 rounded-card bg-gray-50 border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
              </svg>
              Trusted Sources
            </h3>
            <ul className="space-y-3">
              {briefing.source_urls.map((url, index) => (
                <li key={index} className="flex items-start gap-2">
                  <svg className="w-4 h-4 text-teal-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <a
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-primary-700 hover:text-primary-900 hover:underline break-all transition-colors"
                  >
                    {url}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Reading Level Help Note */}
        <div className="mb-8 p-6 rounded-card gradient-soft border-l-4 border-accent-500">
          <div className="flex items-start gap-4">
            <div className="w-10 h-10 rounded-full bg-accent-100 flex items-center justify-center flex-shrink-0">
              <svg className="w-5 h-5 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <div>
              <p className="font-semibold text-gray-900 mb-2">Want this at a different reading level?</p>
              <p className="text-gray-700 leading-relaxed mb-3">
                Copy any source URL above and paste it into our{' '}
                <Link to="/" className="font-medium text-accent-600 hover:text-accent-700 underline">
                  Explain an Article
                </Link>{' '}
                tool on the home page. Choose your preferred reading level (Grade 3 to College) for a customized explanation.
              </p>
            </div>
          </div>
        </div>

        {/* Disclaimer */}
        <div className="rounded-card bg-yellow-50 border-l-4 border-yellow-500 p-6">
          <div className="flex items-start gap-3">
            <svg className="w-6 h-6 text-yellow-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div>
              <p className="font-semibold text-yellow-900 mb-1">Medical Disclaimer</p>
              <p className="text-sm text-yellow-800 leading-relaxed">{briefing.disclaimer}</p>
            </div>
          </div>
        </div>
      </article>
    </div>
  );
}
