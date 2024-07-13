import { auth } from "@/auth"

const PRIVATE_ROUTES = ["/","/vote"]
const AUTH_ROUTE = "/signin"
export default auth((req)=>{
    const {nextUrl} = req
    const isAuthenticated = req.auth?.user
    const path = nextUrl.pathname
    if (!isAuthenticated && PRIVATE_ROUTES.includes(path)) return Response.redirect(new URL(AUTH_ROUTE,nextUrl))
    if(isAuthenticated && path === AUTH_ROUTE || path === "/") return Response.redirect(new URL("/vote",nextUrl))
})
export const config = {
	matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};