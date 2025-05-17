import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    // Parse the request body
    const body = await request.json();
    
    // Validate input
    if (!body.ratings || !Array.isArray(body.ratings)) {
      return NextResponse.json(
        { error: 'Invalid input: expected { "ratings": number[] }' },
        { status: 400 }
      );
    }

    const ratings = body.ratings as number[];
    
    // Handle empty array case
    if (ratings.length === 0) {
      return NextResponse.json(
        { error: 'No ratings provided', average: null },
        { status: 200 }
      );
    }

    // Validate all elements are numbers
    if (!ratings.every(rating => typeof rating === 'number' && !isNaN(rating))) {
      return NextResponse.json(
        { error: 'All ratings must be numbers' },
        { status: 400 }
      );
    }

    // Calculate average
    const sum = ratings.reduce((a, b) => a + b, 0);
    const average = sum / ratings.length;
    
    // Return the result with 2 decimal places
    return NextResponse.json({ 
      average: parseFloat(average.toFixed(2)) 
    });
    
  } catch (error) {
    console.error('Error processing request:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
