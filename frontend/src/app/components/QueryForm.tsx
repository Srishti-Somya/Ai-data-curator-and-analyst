'use client';

import { useState } from 'react';
import { QueryRequest, ProcessingStatus } from '../services/api';

interface QueryFormProps {
  onSubmit: (request: QueryRequest) => Promise<void>;
  isProcessing: boolean;
}

const predefinedQueries = [
  {
    name: 'Climate Change Research',
    query: 'climate change solutions 2024',
    keywords: ['renewable energy', 'carbon capture']
  },
  {
    name: 'Quantum Computing',
    query: 'quantum computing applications 2024',
    keywords: ['quantum', 'computing', 'algorithms']
  },
  {
    name: 'Space Exploration',
    query: 'space exploration missions 2024',
    keywords: ['NASA', 'Mars', 'satellite']
  },
  {
    name: 'AI and Machine Learning',
    query: 'artificial intelligence trends 2024',
    keywords: ['machine learning', 'AI development']
  },
  {
    name: 'Cancer Research',
    query: 'cancer research breakthroughs 2024',
    keywords: ['oncology', 'treatment', 'clinical trials']
  },
  {
    name: 'Blockchain Technology',
    query: 'blockchain technology developments 2024',
    keywords: ['cryptocurrency', 'decentralized', 'smart contracts']
  }
];

const defaultColumns = ['Person', 'Org', 'Date', 'Loc'];

export default function QueryForm({ onSubmit, isProcessing }: QueryFormProps) {
  const [query, setQuery] = useState('');
  const [keywords, setKeywords] = useState('');
  const [selectedColumns, setSelectedColumns] = useState<string[]>(defaultColumns);
  const [selectedPredefined, setSelectedPredefined] = useState('');

  const handlePredefinedQueryChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selected = event.target.value;
    setSelectedPredefined(selected);
    
    if (selected) {
      const predefined = predefinedQueries.find(q => q.name === selected);
      if (predefined) {
        setQuery(predefined.query);
        setKeywords(predefined.keywords.join(', '));
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) {
      alert('Please enter a query');
      return;
    }

    const keywordsArray = keywords
      .split(',')
      .map(k => k.trim())
      .filter(k => k.length > 0);

    if (keywordsArray.length === 0) {
      alert('Please enter at least one keyword');
      return;
    }

    const request: QueryRequest = {
      query: query.trim(),
      keywords: keywordsArray,
      columns_to_save: selectedColumns
    };

    await onSubmit(request);
  };

  const toggleColumn = (column: string) => {
    setSelectedColumns(prev => 
      prev.includes(column) 
        ? prev.filter(c => c !== column)
        : [...prev, column]
    );
  };

  const handleColumnToggle = (column: string, checked: boolean) => {
    setSelectedColumns(prev => 
      checked 
        ? [...prev, column]
        : prev.filter(c => c !== column)
    );
  };

  const entityOptions = [
    { id: 'Person', label: 'Person' },
    { id: 'Org', label: 'Org (Organization)' },
    { id: 'Date', label: 'Date' },
    { id: 'Loc', label: 'Loc (Location)' },
    { id: 'Misc', label: 'Misc (Miscellaneous)' },
    { id: 'Money', label: 'Money' },
    { id: 'Percent', label: 'Percent' },
    { id: 'Time', label: 'Time' },
    { id: 'Quantity', label: 'Quantity' },
    { id: 'Ordinal', label: 'Ordinal' },
    { id: 'Cardinal', label: 'Cardinal' },
    { id: 'Product', label: 'Product' }
  ];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">AI Data Curation & Analysis</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Predefined Queries */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Quick Start (Predefined Queries)
          </label>
          <select
            value={selectedPredefined}
            onChange={handlePredefinedQueryChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select a predefined query...</option>
            {predefinedQueries.map((q) => (
              <option key={q.name} value={q.name}>
                {q.name}
              </option>
            ))}
          </select>
        </div>

        {/* Query Input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Search Query *
          </label>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your search query (e.g., artificial intelligence trends 2024)"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
            disabled={isProcessing}
          />
        </div>

        {/* Keywords Input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Keywords (comma-separated) *
          </label>
          <input
            type="text"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            placeholder="Enter keywords (e.g., AI, machine learning, neural networks)"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
            disabled={isProcessing}
          />
          <p className="text-sm text-gray-500 mt-1">
            Separate multiple keywords with commas
          </p>
        </div>

        {/* Columns Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Data Columns to Extract
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {entityOptions.map((option) => (
              <label key={option.id} className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={selectedColumns.includes(option.id)}
                  onChange={(e) => handleColumnToggle(option.id, e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">{option.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isProcessing}
          className={`w-full py-3 px-4 rounded-md font-medium transition-colors ${
            isProcessing
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 text-white'
          }`}
        >
          {isProcessing ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Processing...
            </div>
          ) : (
            'Start Analysis'
          )}
        </button>
      </form>

      {/* Processing Status */}
      {isProcessing && (
        <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
          <div className="flex items-center">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
            <span className="text-blue-800">
              Processing your query... This may take a few minutes.
            </span>
          </div>
        </div>
      )}
    </div>
  );
} 