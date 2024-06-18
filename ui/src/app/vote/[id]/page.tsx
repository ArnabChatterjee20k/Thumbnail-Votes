"use server";
import { Button } from "@/components/ui/button";
import {
  NotFoundError,
  getProjectDetails,
  getThumbnail,
  isUserVoted,
} from "../utils";
import Image from "next/image";
import { notFound, redirect } from "next/navigation";

export default async function Vote({
  params: { id },
}: {
  params: { id: number };
}) {
  const { title, thumbnails } = await getProjectDetails(id);
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
            <Button variant="outline" size="sm">
              <ThumbsUpIcon className="w-4 h-4" />
            </Button>
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
                <Button variant="ghost" size="icon">
                  <ThumbsUpIcon className="w-4 h-4" />
                </Button>
                <div className="text-sm">12</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
// @ts-ignore
function ThumbsUpIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M7 10v12" />
      <path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2h0a3.13 3.13 0 0 1 3 3.88Z" />
    </svg>
  );
}
