"use client";
import { useSocket } from "@/context/SocketContextProvider";
export default function LiveVoteCounter({initialCount,thumbnail_id}:{initialCount:number,thumbnail_id:string}) {
    const {votes} = useSocket()
  return (
    <div className="text-sm">
      {votes[thumbnail_id]?votes[thumbnail_id]:initialCount}
    </div>
  );
}
