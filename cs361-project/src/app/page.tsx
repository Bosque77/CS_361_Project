'use client';

import { useState } from 'react';
import Image from "next/image";

export default function Home() {
  const [ratings, setRatings] = useState<string>('4, 5, 3, 5');
  const [result, setResult] = useState<{average?: number, error?: string} | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const calculateAverage = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Parse the input string into an array of numbers
      const ratingsArray = ratings
        .split(',')
        .map(r => parseFloat(r.trim()))
        .filter(n => !isNaN(n));

      const response = await fetch('/api/average', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ratings: ratingsArray }),
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to calculate average');
      }
      
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8 md:p-12">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-3xl md:text-4xl font-bold mb-4">Ratings Average Microservice</h1>
          <p className="text-gray-600 dark:text-gray-300">
            A microservice that calculates the average of numeric ratings
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
          <div className="mb-6">
            <label htmlFor="ratings" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Enter ratings (comma-separated numbers):
            </label>
            <input
              type="text"
              id="ratings"
              value={ratings}
              onChange={(e) => setRatings(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              placeholder="e.g., 4, 5, 3, 5"
            />
          </div>
          
          <button
            onClick={calculateAverage}
            disabled={isLoading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? 'Calculating...' : 'Calculate Average'}
          </button>
          
          {(result || error) && (
            <div className={`mt-6 p-4 rounded-md ${
              error ? 'bg-red-50 border border-red-200 dark:bg-red-900/20 dark:border-red-800' : 
              'bg-green-50 border border-green-200 dark:bg-green-900/20 dark:border-green-800'
            }`}>
              <h3 className="text-lg font-medium mb-2">
                {error ? 'Error' : 'Result'}
              </h3>
              {result?.average !== undefined && (
                <p className="text-2xl font-bold">
                  Average: {result.average.toFixed(2)}
                </p>
              )}
              {(result?.error || error) && (
                <p className="text-red-600 dark:text-red-400">
                  {result?.error || error}
                </p>
              )}
            </div>
          )}
        </div>

        <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">API Documentation</h2>
          <p className="mb-4 text-gray-600 dark:text-gray-300">
            Send a POST request to <code className="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">/api/average</code> with a JSON body containing an array of numbers.
          </p>
          
          <div className="bg-black/80 dark:bg-gray-900 p-4 rounded-md overflow-x-auto">
            <pre className="text-green-400 text-sm">
{`// Request
POST /api/average
Content-Type: application/json

{
  "ratings": [4, 5, 3, 5]
}

// Success Response (200 OK)
{
  "average": 4.25
}

// Error Response (400 Bad Request)
{
  "error": "All ratings must be numbers"
}

// Empty Array Response (200 OK)
{
  "error": "No ratings provided",
  "average": null
}`}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
