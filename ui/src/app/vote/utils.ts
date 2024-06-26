import { ProjectType } from "./types";

export async function getProjectDetails(project_id: number) {
  const url = process.env.NEXT_PUBLIC_PROJECTURL || "";
  const res = await fetch(`${url}/${project_id}`);
  if (res.status !== 200) throw new NotFoundError(JSON.stringify({ code: res.status }));
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

export class NotFoundError extends Error {
  constructor(message?: string) {
    super(message);
    this.name = "NotFoundError";
  }
}
