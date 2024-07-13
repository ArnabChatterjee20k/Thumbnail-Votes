import { auth } from "@/auth";
import { GoogleSignin } from "@/components/google-signin";

export default async function page() {
  return (
    <GoogleSignin/>
  )
}
