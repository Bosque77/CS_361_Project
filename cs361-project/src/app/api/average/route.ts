import { NextResponse } from 'next/server';

// Helper function to add CORS headers to the response
const addCorsHeaders = (response: NextResponse) => {
  response.headers.set('Access-Control-Allow-Origin', '*');
  response.headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  return response;
};

export async function OPTIONS() {
  const response = new NextResponse(null, { status: 204 });
  return addCorsHeaders(response);
}

export async function POST(request: Request) {
  try {
    // Parse the request body
    const body = await request.json();
    
    // Validate input
    if (!body.ratings || !Array.isArray(body.ratings)) {
      const response = NextResponse.json(
        { error: 'Invalid input: expected { "ratings": number[] }' },
        { status: 400 }
      );
      return addCorsHeaders(response);
    }

    const ratings = body.ratings as number[];
    
    // Handle empty array case
    if (ratings.length === 0) {
      const response = NextResponse.json(
        { error: 'No ratings provided', average: null },
        { status: 200 }
      );
      return addCorsHeaders(response);
    }

    // Validate all elements are numbers
    if (!ratings.every(rating => typeof rating === 'number' && !isNaN(rating))) {
      const response = NextResponse.json(
        { error: 'All ratings must be numbers' },
        { status: 400 }
      );
      return addCorsHeaders(response);
    }

    // Calculate average
    const sum = ratings.reduce((a, b) => a + b, 0);
    const average = sum / ratings.length;
    
    // Return the result with 2 decimal places
    const response = NextResponse.json({ 
      average: parseFloat(average.toFixed(2)) 
    });
    return addCorsHeaders(response);
    
  } catch (error) {
    console.error('Error processing request:', error);
    const response = NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
    return addCorsHeaders(response);
  }
}
