/**
 * Component for displaying a briefing preview card
 */
import { Link } from 'react-router-dom';
import type { BriefingListItem } from '../types';

interface BriefingCardProps {
  briefing: BriefingListItem;
}

export default function BriefingCard({ briefing }: BriefingCardProps) {
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

  return (
    <div className="briefing-card bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <Link to={`/briefings/${briefing.slug}`}>
            <h3 className="text-xl font-semibold text-gray-900 hover:text-primary-600 transition-colors">
              {briefing.title}
            </h3>
          </Link>
          <p className="text-sm text-gray-500 mt-1">{formatDate(briefing.created_at)}</p>
        </div>
        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800 ml-4">
          {getSourceTypeLabel(briefing.source_type)}
        </span>
      </div>

      <p className="text-gray-700 mb-4">{briefing.summary}</p>

      {/* Tags */}
      {briefing.tags && briefing.tags.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {briefing.tags.map((tag, index) => (
            <span
              key={index}
              className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-700"
            >
              {tag}
            </span>
          ))}
        </div>
      )}

      <Link
        to={`/briefings/${briefing.slug}`}
        className="inline-flex items-center text-primary-600 hover:text-primary-800 font-medium"
      >
        Read more
        <svg
          className="ml-2 w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5l7 7-7 7"
          />
        </svg>
      </Link>
    </div>
  );
}
