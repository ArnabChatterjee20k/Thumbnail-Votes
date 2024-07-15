import Voteview from "./Voteview";
import VoteRender from "./VoteRender";
import { getProjectDetails, isAdmin } from "../utils";
import { auth } from "@/auth";


export  default async ({ params: { id } }: { params: { id: number } }) => {
  const {email} = await getProjectDetails(id)
  const admin = await isAdmin(email)
  return (
    <VoteRender establishSocket={admin?false:true}>
      <Voteview id={id} />
    </VoteRender>
  );
};
