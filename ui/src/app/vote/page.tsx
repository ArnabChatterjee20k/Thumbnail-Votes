import { auth } from "@/auth";
import { CreateProject } from "@/components/create-project";

export default async function Vote() {
  const user = await auth()
  return <CreateProject />;
}
