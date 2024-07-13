"use server";

import { auth } from "@/auth";
import { redirect } from "next/navigation";
export default async (form: FormData) => {
  const session = await auth();
  const user = session?.user
  if (!user) return;
  const name = form.get("name") as string;
  const prompt = form.get("prompt") as string;
  const count = form.get("count") as string;
  if (!name || !prompt || !count) return;
  const data = await create(user.email as string,name, prompt, parseInt(count));
  if(data) redirect(`/vote/${data.project}`)
};

type ProjectResult = {
  project:number
}

async function create(
  email: string,
  name: string,
  prompt: string,
  count: number
):Promise<ProjectResult> {
  const url = process.env.THUMBNAIL;
  const res = await fetch(url as string, {
    method: "POST",
    body: JSON.stringify({
      email,
      message: prompt,
      count,
      name,
    }),
    headers: { "Content-Type": "application/json" },
  });

  return await res.json()
}
