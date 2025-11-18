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
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header - Clean, spacious, modern */}
      <header className="bg-white shadow-soft sticky top-0 z-50 backdrop-blur-sm bg-white/95">
        <div className="container-custom">
          <div className="flex justify-between items-center py-5">
            {/* Logo */}
            <Link
              to="/"
              className="flex items-center gap-2 group transition-all duration-slow"
            >
              <div className="w-10 h-10 bg-gradient-hero rounded-full flex items-center justify-center transition-transform duration-slow group-hover:scale-110">
                <svg
                  className="w-6 h-6 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                  />
                </svg>
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-accent-500 bg-clip-text text-transparent">
                EazyHealth AI
              </h1>
            </Link>

            {/* Navigation */}
            <nav className="flex gap-2">
              <Link
                to="/"
                className={`px-5 py-2 rounded-pill font-medium transition-all duration-slow ${
                  isActive('/')
                    ? 'bg-primary-100 text-primary-700'
                    : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                }`}
              >
                Home
              </Link>
              <Link
                to="/briefings"
                className={`px-5 py-2 rounded-pill font-medium transition-all duration-slow ${
                  isActive('/briefings')
                    ? 'bg-primary-100 text-primary-700'
                    : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                }`}
              >
                Briefings
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content - Flexible grow to push footer down */}
      <main className="flex-grow">
        <div className="container-custom py-12">
          {children}
        </div>
      </main>

      {/* Footer - Calm, informative */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="container-custom py-8">
          <div className="text-center space-y-4">
            <p className="text-sm text-gray-600 max-w-2xl mx-auto leading-relaxed">
              <span className="font-semibold text-gray-900">EazyHealth AI</span> — Accessible health information powered by AI.
              <br />
              Health information that finds you and answers you.
            </p>
            <div className="pt-4 border-t border-gray-100">
              <p className="text-xs text-gray-500 max-w-3xl mx-auto">
                <strong className="text-gray-700">Medical Disclaimer:</strong> This is an educational tool, not a source of medical advice.
                The information provided is for general knowledge only. Always consult qualified healthcare professionals for personalized medical guidance and treatment decisions.
              </p>
            </div>
            <p className="text-xs text-gray-400 pt-2">
              © {new Date().getFullYear()} EazyHealth AI. Built with care for better health literacy.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
