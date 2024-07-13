import { auth } from "@/auth";
import { SignIn } from "@/components/ui/sign-in";

import Image from "next/image";

export default async  function Home() {
  const user = await auth()
  console.log(user?.user?.id)
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      {user?.user?.email ? <div className="text-white">{user?.user?.email}</div>:<SignIn/> }
    </main>
  );
}
