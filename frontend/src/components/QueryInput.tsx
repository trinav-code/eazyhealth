/**
 * Component for inputting health queries or URLs
 */
import { useState } from 'react';
import { ReadingLevel } from '../types';
import ReadingLevelSelector from './ReadingLevelSelector';

interface QueryInputProps {
  onSubmit: (data: {
    query?: string;
    url?: string;
    readingLevel: ReadingLevel;
  }) => void;
  isLoading?: boolean;
}

export default function QueryInput({ onSubmit, isLoading = false }: QueryInputProps) {
  const [inputMode, setInputMode] = useState<'query' | 'url'>('query');
  const [query, setQuery] = useState('');
  const [url, setUrl] = useState('');
  const [readingLevel, setReadingLevel] = useState<ReadingLevel>('grade6');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (inputMode === 'query' && query.trim()) {
      onSubmit({ query: query.trim(), readingLevel });
    } else if (inputMode === 'url' && url.trim()) {
      onSubmit({ url: url.trim(), readingLevel });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Input Mode Toggle */}
      <div className="flex gap-2 border-b border-gray-200">
        <button
          type="button"
          onClick={() => setInputMode('query')}
          className={`px-4 py-2 font-medium transition-colors ${
            inputMode === 'query'
              ? 'text-primary-600 border-b-2 border-primary-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Ask a Question
        </button>
        <button
          type="button"
          onClick={() => setInputMode('url')}
          className={`px-4 py-2 font-medium transition-colors ${
            inputMode === 'url'
              ? 'text-primary-600 border-b-2 border-primary-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Explain an Article
        </button>
      </div>

      {/* Input Field */}
      {inputMode === 'query' ? (
        <div>
          <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
            What would you like to know?
          </label>
          <textarea
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., What is atrial fibrillation? How does diabetes affect the body?"
            rows={3}
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 px-4 py-2 border"
            disabled={isLoading}
          />
        </div>
      ) : (
        <div>
          <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
            Article URL
          </label>
          <input
            type="url"
            id="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com/health-article"
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 px-4 py-2 border"
            disabled={isLoading}
          />
        </div>
      )}

      {/* Reading Level Selector */}
      <ReadingLevelSelector value={readingLevel} onChange={setReadingLevel} />

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading || (inputMode === 'query' ? !query.trim() : !url.trim())}
        className="w-full bg-primary-600 text-white py-3 px-6 rounded-md font-medium hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
      >
        {isLoading ? 'Generating Explainer...' : 'Get Explanation'}
      </button>
    </form>
  );
}
