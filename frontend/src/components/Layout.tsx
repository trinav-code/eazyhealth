/**
 * Main layout component with navigation
 */
import { Link, useLocation } from 'react-router-dom';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <Link to="/" className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">EazyHealth AI</h1>
            </Link>
            <nav className="flex gap-6">
              <Link
                to="/"
                className={`font-medium transition-colors ${
                  isActive('/')
                    ? 'text-primary-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Home
              </Link>
              <Link
                to="/briefings"
                className={`font-medium transition-colors ${
                  isActive('/briefings')
                    ? 'text-primary-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Briefings
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-500">
            EazyHealth AI - Health information that finds you and answers you.
            <br />
            <strong>Disclaimer:</strong> This is an educational tool, not a source of medical advice.
            Always consult healthcare professionals for medical guidance.
          </p>
        </div>
      </footer>
    </div>
  );
}
