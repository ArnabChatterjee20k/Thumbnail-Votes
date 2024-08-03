import Voteview from "./Voteview";
import VoteRender from "./VoteRender";
import { getProjectDetails, isAdmin, getVotingInfo } from "../utils";
import { redirect } from "next/navigation";

export default async ({ params: { id } }: { params: { id: number } }) => {
  const votingData = await Promise.all([
    getProjectDetails(id),
    getVotingInfo(id),
  ]);

  const projectDetailsResult = votingData[0];
  const votingInfoResult = votingData[1];
  console.log({projectDetailsResult,votingInfoResult})
  if(!votingInfoResult) redirect("/signin")
  const { email } = projectDetailsResult
  const {voted,results:voteResults} = votingInfoResult
  const admin = await isAdmin(email);
  console.log({voted})
  return (
    <VoteRender establishSocket={voted}>
      <Voteview id={id} />
    </VoteRender>
  );
};
