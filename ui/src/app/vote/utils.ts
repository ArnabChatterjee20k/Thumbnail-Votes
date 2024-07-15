import { auth } from "@/auth";
import { ProjectType } from "./types";
import { redirect } from "next/navigation";

export async function getProjectDetails(project_id: number) {
  const url = process.env.NEXT_PUBLIC_PROJECTURL || "";
  const res = await fetch(`${url}/${project_id}`,{next:{revalidate:40}});
  if (res.status !== 200) redirect("/error");
  const data: ProjectType = await res.json();
  return data;
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
