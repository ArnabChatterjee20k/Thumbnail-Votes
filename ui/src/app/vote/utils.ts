import { auth } from "@/auth";
import { ProjectType,VotingResults } from "./types";
import { redirect } from "next/navigation";

export async function getProjectDetails(project_id: number):Promise<ProjectType> {
  const url = process.env.NEXT_PUBLIC_PROJECTURL || "";
  const res = await fetch(`${url}/${project_id}`,{next:{revalidate:200}});
  if (res.status !== 200) redirect("/error");
  return res.json()
}

export async function getVotingInfo(project_id: number):Promise<VotingResults|null>{
  const session = await auth()
  const url = process.env.NEXT_PUBLIC_VOTERESULT || ""
  const urlObj = new URL(`${url}/${project_id}`);
  const params = new URLSearchParams(urlObj.search);
  if(!session?.user) return null
  params.append('email', session?.user?.email || "");
  urlObj.search = params.toString();
  const updatedUrl = urlObj.toString();
  const res = await fetch(updatedUrl,{next:{tags:["projectDetails"]}})
  return res.json()
}

export function getThumbnail(thumbnail_id: string) {
  const url = process.env.NEXT_PUBLIC_THUMBNAILCDN || "";
  return `${url}/thumbnails/${thumbnail_id}`;
}

export function isUserVoted() {
  // TODO: auth route needs to be implemented
  return false;
}

export function getTotalVotes(project_id: number) {
  // TODO: need to return if user is voted
  return 100;
}

export async function isAdmin(adminEmail:string){
  const session = await auth()
  const user = session?.user
  if(!user || !user.email) return false
  return user.email === adminEmail
}

export class NotFoundError extends Error {
  constructor(message?: string) {
    super(message);
    this.name = "NotFoundError";
  }
}
