"use server"
import { auth } from "@/auth"
import { revalidateTag } from "next/cache"
import { redirect } from "next/navigation"

export async function upVote(thumbnail_id:string,project_id:number){
    const session = await auth()
    if(!session?.user) return
    const url = `${process.env.VOTE_SOCKETS}/${project_id}/${thumbnail_id}?email=${session.user.email}`
    const res = await fetch(url,{
        method:"POST",
    })
    if(!res.ok) redirect("/error")
    console.log(await res.json())
    revalidateTag("projectDetails")
}