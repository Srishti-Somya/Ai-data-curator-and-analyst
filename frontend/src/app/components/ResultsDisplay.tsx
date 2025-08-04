'use client';

import { useState, useEffect } from 'react';
import { QueryResponse, apiService } from '../services/api';

interface ResultsDisplayProps {
  result: QueryResponse | null;
  onReset: () => void;
}

interface CsvRow {
  [key: string]: string;
}

export default function ResultsDisplay({ result, onReset }: ResultsDisplayProps) {
  const [csvData, setCsvData] = useState<string>('');
  const [svgData, setSvgData] = useState<string>('');
  const [parsedCsvData, setParsedCsvData] = useState<CsvRow[]>([]);
  const [activeTab] = useState<'csv'>('csv');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (result) {
      loadResults();
    }
  }, [result]);

  const loadResults = async () => {
    if (!result) return;
    
    setIsLoading(true);
    try {
      // Load CSV data
      const csvText = await apiService.getCsvData();
      setCsvData(csvText);
      
      // Parse CSV data for table display
      const rows = parseCsvData(csvText);
      setParsedCsvData(rows);
      
      // Load SVG data
      const svgText = await apiService.getSvgData();
      setSvgData(svgText);
    } catch (error) {
      console.error('Error loading results:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const parseCsvData = (csvText: string): CsvRow[] => {
    const lines = csvText.trim().split('\n');
    if (lines.length < 2) return [];
    
    const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
    const rows: CsvRow[] = [];
    
    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',').map(v => v.trim().replace(/"/g, ''));
      const row: CsvRow = {};
      headers.forEach((header, index) => {
        row[header] = values[index] || '';
      });
      rows.push(row);
    }
    
    return rows;
  };

  const downloadCsv = () => {
    if (!csvData) return;
    
    const blob = new Blob([csvData], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'structured_data.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const downloadSvg = () => {
    if (!svgData) return;
    
    const blob = new Blob([svgData], { type: 'image/svg+xml' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'relationships.svg';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  if (!result) return null;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Analysis Results</h2>
        <button
          onClick={onReset}
          className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
        >
          New Query
        </button>
      </div>

      {/* Success Message */}
      <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-md">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-green-800">
              {result.message}
            </p>
          </div>
        </div>
      </div>

      {/* Single Tab - Only CSV Data */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
                  <button
          className="py-2 px-1 border-b-2 font-medium text-sm border-blue-500 text-blue-600"
        >
            Structured Data (CSV)
          </button>
        </nav>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">Loading results...</span>
        </div>
      )}

      {/* CSV Tab Content */}
      {activeTab === 'csv' && !isLoading && (
        <div>
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-gray-900">Extracted Entities</h3>
            <button
              onClick={downloadCsv}
              className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors"
            >
              Download CSV
            </button>
          </div>
          
          {parsedCsvData.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    {Object.keys(parsedCsvData[0]).map((header) => (
                      <th
                        key={header}
                        className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        {header}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {parsedCsvData.map((row, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      {Object.values(row).map((value, cellIndex) => (
                        <td
                          key={cellIndex}
                          className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                        >
                          {value || '-'}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              No structured data found. The analysis may not have extracted any entities.
            </div>
          )}
        </div>
      )}

      {/* SVG Download Section */}
      {!isLoading && (
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-medium text-blue-900">Linguistic Relationships Visualization</h3>
              <p className="text-sm text-blue-700 mt-1">
                Download the enhanced SVG visualization showing linguistic dependencies and relationships.
              </p>
            </div>
            <button
              onClick={downloadSvg}
              className="px-4 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors flex items-center space-x-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span>Download SVG</span>
            </button>
          </div>
        </div>
      )}

      {/* File Information */}
      <div className="mt-6 p-4 bg-gray-50 rounded-md">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Generated Files:</h4>
        <div className="text-sm text-gray-600 space-y-1">
          <div>📄 CSV File: {result.csv_file}</div>
          <div>🎨 SVG File: {result.svg_file}</div>
        </div>
      </div>
    </div>
  );
} 