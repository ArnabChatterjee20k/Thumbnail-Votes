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
  voted
}: {
  children: React.ReactNode;
  establishSocket: boolean;
  voted:boolean;
}) {
  const session = useSession();
  const param = useParams();
  if (!session.data?.user?.email)
    return (
      <Link href="/signin">
        <Button variant="default">Login to continue</Button>
      </Link>
    );
  if (voted && establishSocket)
    return (
      <SocketContextProvider
        project_id={parseInt(param.id as string) as number}
        email={session.data?.user?.email as string}
      >
        {children}
      </SocketContextProvider>
    );
    // TODO: use two context with same interface -> one with http and other with socket. Build a single context and put the methods as a dependecy injection
  return <>{children}</>;
}
