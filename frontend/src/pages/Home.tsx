/**
 * Home page with latest briefing and explainer input
 */
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import QueryInput from '../components/QueryInput';
import ExplainerResult from '../components/ExplainerResult';
import BriefingCard from '../components/BriefingCard';
import type { BriefingListItem, ExplainerResponse } from '../types';

export default function Home() {
  const [latestBriefing, setLatestBriefing] = useState<BriefingListItem | null>(null);
  const [explainerResult, setExplainerResult] = useState<ExplainerResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load latest briefing on mount
  useEffect(() => {
    loadLatestBriefing();
  }, []);

  const loadLatestBriefing = async () => {
    try {
      const response = await api.getBriefings({ limit: 1 });
      if (response.items.length > 0) {
        setLatestBriefing(response.items[0]);
      }
    } catch (err) {
      console.error('Failed to load latest briefing:', err);
    }
  };

  const handleExplainerSubmit = async (data: {
    query?: string;
    url?: string;
    readingLevel: any;
  }) => {
    setIsLoading(true);
    setError(null);
    setExplainerResult(null);

    try {
      const result = await api.explain({
        query: data.query,
        url: data.url,
        reading_level: data.readingLevel,
      });
      setExplainerResult(result);
    } catch (err: any) {
      setError(err.message || 'Failed to generate explainer. Please try again.');
      console.error('Explainer error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Health Information That Finds You and Answers You
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Get easy-to-understand explanations of health topics and stay informed with
          auto-generated briefings from trusted sources.
        </p>
      </section>

      {/* Latest Briefing */}
      {latestBriefing && (
        <section>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Latest Briefing</h2>
            <Link
              to="/briefings"
              className="text-primary-600 hover:text-primary-800 font-medium"
            >
              View all briefings →
            </Link>
          </div>
          <BriefingCard briefing={latestBriefing} />
        </section>
      )}

      {/* Explainer Section */}
      <section>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Ask About Any Health Topic</h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <QueryInput onSubmit={handleExplainerSubmit} isLoading={isLoading} />
          </div>

          {/* Info */}
          <div className="bg-gradient-to-br from-primary-50 to-blue-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              How It Works
            </h3>
            <ul className="space-y-3 text-gray-700">
              <li className="flex items-start">
                <svg
                  className="w-6 h-6 text-primary-600 mr-3 flex-shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span>
                  <strong>Ask any health question</strong> and we'll find relevant,
                  trustworthy sources
                </span>
              </li>
              <li className="flex items-start">
                <svg
                  className="w-6 h-6 text-primary-600 mr-3 flex-shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span>
                  <strong>Paste an article URL</strong> to get a simplified summary
                </span>
              </li>
              <li className="flex items-start">
                <svg
                  className="w-6 h-6 text-primary-600 mr-3 flex-shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span>
                  <strong>Choose your reading level</strong> from 3rd grade to college
                </span>
              </li>
            </ul>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mt-6 bg-red-50 border-l-4 border-red-500 p-4 rounded">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {/* Result Display */}
        {explainerResult && (
          <div className="mt-8">
            <ExplainerResult result={explainerResult} />
          </div>
        )}
      </section>
    </div>
  );
}
