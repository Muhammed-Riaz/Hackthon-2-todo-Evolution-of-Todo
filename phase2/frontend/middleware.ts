import { NextRequest, NextResponse } from 'next/server';

// Define protected routes
const protectedRoutes = ['/dashboard'];

export function middleware(request: NextRequest) {
  // Check if the route is protected
  const isProtectedRoute = protectedRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  );

  if (isProtectedRoute) {
    // Check if user is authenticated by checking for auth token in cookies
    // The token is stored in a cookie by our API client for server-side access
    const authToken = request.cookies.get('auth_token');

    if (!authToken) {
      // Redirect to login if not authenticated
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  return NextResponse.next();
}

// Apply middleware to specific paths
export const config = {
  matcher: ['/dashboard/:path*', '/profile/:path*'],
};