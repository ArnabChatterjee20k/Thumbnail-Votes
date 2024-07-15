"use client";
import { Button } from "@/components/ui/button";
import { SocketContextProvider } from "@/context/SocketContextProvider";
import { useSession } from "next-auth/react";
import Link from "next/link";
import { useParams } from "next/navigation";
import React from "react";

export default function VoteRender({
  children,
  establishSocket,
}: {
  children: React.ReactNode;
  establishSocket: boolean;
}) {
  const session = useSession();
  const param = useParams();
  if (!session.data?.user?.email)
    return (
      <Link href="/signin">
        <Button variant="default">Login to continue</Button>
      </Link>
    );
  if (establishSocket)
    return (
      <SocketContextProvider
        project_id={parseInt(param.id as string) as number}
        email={session.data?.user?.email as string}
      >
        {children}
      </SocketContextProvider>
    );

  return <>{children}</>;
}
