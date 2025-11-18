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
    <div className="space-y-16">
      {/* Hero Section - Gradient background with modern design */}
      <section className="relative -mt-12 -mx-4 sm:-mx-6 lg:-mx-8 px-4 sm:px-6 lg:px-8 py-20 gradient-hero text-white overflow-hidden">
        {/* Decorative background elements */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 right-0 w-96 h-96 bg-white rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-accent-300 rounded-full blur-3xl"></div>
        </div>

        <div className="relative max-w-container mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
            Health Information That
            <br />
            <span className="text-accent-200">Finds You and Answers You</span>
          </h1>
          <p className="text-xl md:text-2xl text-blue-100 max-w-3xl mx-auto mb-10 leading-relaxed">
            Get easy-to-understand explanations of health topics and stay informed with
            AI-powered briefings from trusted sources.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="#ask"
              className="btn btn-accent inline-flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              Ask a Health Question
            </a>
            <Link
              to="/briefings"
              className="btn bg-white/20 text-white border-2 border-white/40 hover:bg-white/30 hover:shadow-soft backdrop-blur-sm"
            >
              Browse All Briefings
            </Link>
          </div>
        </div>
      </section>

      {/* Latest Briefing - Featured section */}
      {latestBriefing && (
        <section>
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">Latest Briefing</h2>
              <p className="text-gray-600">Stay updated with the newest health insights</p>
            </div>
            <Link
              to="/briefings"
              className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium transition-colors group"
            >
              View all briefings
              <svg className="w-5 h-5 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </Link>
          </div>
          <div className="card-lg shadow-floating">
            <BriefingCard briefing={latestBriefing} />
          </div>
        </section>
      )}

      {/* Explainer Section */}
      <section id="ask" className="scroll-mt-20">
        <div className="mb-10 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-3">Ask About Any Health Topic</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Get personalized explanations at your reading level from trusted health sources
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Card */}
          <div className="card-lg">
            <QueryInput onSubmit={handleExplainerSubmit} isLoading={isLoading} />
          </div>

          {/* Info Card - How It Works */}
          <div className="card-lg gradient-soft">
            <h3 className="text-xl font-semibold text-gray-900 mb-6 flex items-center gap-2">
              <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              How It Works
            </h3>
            <ul className="space-y-5">
              <li className="flex items-start">
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center mr-4">
                  <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <div>
                  <p className="font-semibold text-gray-900 mb-1">Ask any health question</p>
                  <p className="text-gray-600 text-sm">We'll find relevant, trustworthy sources from CDC, NIH, Mayo Clinic, and more</p>
                </div>
              </li>
              <li className="flex items-start">
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-accent-100 flex items-center justify-center mr-4">
                  <svg className="w-5 h-5 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                  </svg>
                </div>
                <div>
                  <p className="font-semibold text-gray-900 mb-1">Paste an article URL</p>
                  <p className="text-gray-600 text-sm">Get a simplified summary of complex medical articles in plain language</p>
                </div>
              </li>
              <li className="flex items-start">
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-teal-100 flex items-center justify-center mr-4">
                  <svg className="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <div>
                  <p className="font-semibold text-gray-900 mb-1">Choose your reading level</p>
                  <p className="text-gray-600 text-sm">From 3rd grade to college — content tailored to your comprehension</p>
                </div>
              </li>
            </ul>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mt-8 bg-red-50 border-l-4 border-red-500 rounded-card p-5">
            <div className="flex items-start">
              <svg className="w-6 h-6 text-red-600 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-red-800 font-medium">{error}</p>
            </div>
          </div>
        )}

        {/* Result Display */}
        {explainerResult && (
          <div className="mt-10">
            <ExplainerResult result={explainerResult} />
          </div>
        )}
      </section>
    </div>
  );
}
