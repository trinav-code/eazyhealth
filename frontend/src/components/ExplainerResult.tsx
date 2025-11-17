/**
 * Component for displaying structured explainer results
 */
import ReactMarkdown from 'react-markdown';
import type { ExplainerResponse } from '../types';

interface ExplainerResultProps {
  result: ExplainerResponse;
}

export default function ExplainerResult({ result }: ExplainerResultProps) {
  return (
    <div className="explainer-result bg-white rounded-lg shadow-md p-6 space-y-6">
      {/* Title */}
      <h1 className="text-3xl font-bold text-gray-900">{result.title}</h1>

      {/* Sources */}
      {result.sources && result.sources.length > 0 && (
        <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
          <h3 className="text-sm font-semibold text-blue-900 mb-2">
            Sources Used:
          </h3>
          <ul className="space-y-1">
            {result.sources.map((source, index) => (
              <li key={index}>
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-blue-700 hover:text-blue-900 underline"
                >
                  {source.title}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Sections */}
      <div className="space-y-6">
        {result.sections.map((section, index) => (
          <section key={index} className="section">
            <h2 className="text-xl font-semibold text-gray-800 mb-3 border-b-2 border-gray-200 pb-2">
              {section.heading}
            </h2>
            <div className="prose prose-blue max-w-none text-gray-700">
              <ReactMarkdown>{section.content}</ReactMarkdown>
            </div>
          </section>
        ))}
      </div>

      {/* Disclaimer */}
      <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded mt-6">
        <p className="text-sm text-yellow-900">
          <strong>Disclaimer:</strong> {result.disclaimer}
        </p>
      </div>
    </div>
  );
}
