"use server";
import { Button } from "@/components/ui/button";
import {
  NotFoundError,
  getProjectDetails,
  getThumbnail,
  isUserVoted,
  isAdmin,
  getVotingInfo,
} from "../utils";
import { notFound, redirect } from "next/navigation";
import { auth, signIn } from "@/auth";
import Link from "next/link";
import { useSocket } from "@/context/SocketContextProvider";
import UpVoteButton from "@/components/UpVoteButton";

export default async function Vote({id}:{id:number}) {
  const { title, thumbnails, email } = await getProjectDetails(id);
  if(!id) return
  const admin = await isAdmin(email);
  const session = await auth()
  const votingInfo = await getVotingInfo(id)
  const isUserVoted = votingInfo?.voted
  return (
    <div className="max-w-4xl mx-auto p-6 lg:p-10 flex flex-col min-h-screen justify-center">
      <div className="flex flex-col gap-6">
        <div className="flex items-center justify-between">
          <div className="grid gap-1">
            <h1 className="text-2xl font-bold">{title}</h1>
            <div className="text-sm text-gray-500 dark:text-gray-400">
              Submitted by @doglovers
            </div>
          </div>
          <div className="flex items-center gap-2">
            {
              !session?.user && <Link href="/signin"><Button variant="outline">Login to continue</Button></Link>
            }
            {
              admin && <h3>Current voting results</h3>
            }
          </div>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {thumbnails.map((thumbnail) => (
            <div className="flex flex-col items-center gap-2">
              <img
                src={getThumbnail(thumbnail)}
                alt="Thumbnail"
                width={200}
                height={150}
                className="rounded-lg object-cover aspect-video"
              />
              <div className="flex items-center gap-2">
                {!admin && !isUserVoted && <UpVoteButton thumbnail_id={thumbnail} project_id={id}/>}
                {admin && <div className="text-sm">12 likes</div>}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

