'use client';

import { useState } from 'react';
import QueryForm from './components/QueryForm';
import ResultsDisplay from './components/ResultsDisplay';
import ServerStatus from './components/ServerStatus';
import { QueryRequest, QueryResponse } from './services/api';

export default function Home() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (request: QueryRequest) => {
    setIsProcessing(true);
    setError(null);
    setResult(null);

    try {
      // Import the API service dynamically to avoid SSR issues
      const { apiService } = await import('./services/api');
      const response = await apiService.processQuery(request);
      setResult(response);
    } catch (err) {
      console.error('Error processing query:', err);
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                AI Data Curation & Analysis
              </h1>
              <p className="text-sm text-gray-600">
                Web scraping and NLP analysis for intelligent data extraction
              </p>
            </div>
            <ServerStatus />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">
                  Error Processing Query
                </h3>
                <p className="text-sm text-red-700 mt-1">
                  {error}
                </p>
              </div>
              <div className="ml-auto pl-3">
                <button
                  onClick={() => setError(null)}
                  className="text-red-400 hover:text-red-600"
                >
                  <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Content */}
        {result ? (
          <ResultsDisplay result={result} onReset={handleReset} />
        ) : (
          <div className="space-y-8">
            {/* Introduction */}
            <div className="text-center">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Intelligent Data Extraction & Analysis
              </h2>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Enter a search query and keywords to automatically scrape relevant web content, 
                extract structured data, and generate linguistic visualizations using advanced NLP techniques.
              </p>
            </div>

            {/* Features */}
            <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Web Scraping</h3>
                <p className="text-gray-600">
                  Automatically search and extract relevant content from multiple websites using intelligent crawling.
                </p>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">NLP Analysis</h3>
                <p className="text-gray-600">
                  Extract entities, relationships, and linguistic patterns using advanced natural language processing.
                </p>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Visualization</h3>
                <p className="text-gray-600">
                  Generate interactive visualizations and structured data exports for analysis and reporting.
                </p>
              </div>
            </div>

            {/* Query Form */}
            <QueryForm onSubmit={handleSubmit} isProcessing={isProcessing} />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p className="text-sm">
              AI Tool for Data Curation & Analysis - Powered by FastAPI, spaCy, and Next.js
            </p>
            <p className="text-xs mt-2 text-gray-500">
              Real-time web scraping and natural language processing for intelligent data extraction
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
