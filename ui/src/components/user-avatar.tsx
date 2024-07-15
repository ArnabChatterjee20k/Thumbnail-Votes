import React from "react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { signOut, useSession } from "next-auth/react";
import {
  Menubar,
  MenubarContent,
  MenubarItem,
  MenubarMenu,
  MenubarTrigger,
} from "@/components/ui/menubar";
export default function UserAvatar() {
  const { data, status } = useSession();
  return (
    <Menubar className="outline-transparent border-none rounded-full">
      <MenubarMenu>
        <MenubarTrigger>
          <Avatar className="hover:border-2  hover:border-white transition-all duration-75 cursor-pointer">
            {<AvatarImage src={data?.user?.image as string} />}
            <AvatarFallback>{data?.user?.name?.split(" ").map(e=>e[0]).join("")}</AvatarFallback>
          </Avatar>
        </MenubarTrigger>
        <MenubarContent className="bg-black outline-transparent border-none">
          <MenubarItem onClick={()=>signOut()} className="hover:bg-zinc-700 cursor-pointer">Logout</MenubarItem>
        </MenubarContent>
      </MenubarMenu>
    </Menubar>
  );
}
