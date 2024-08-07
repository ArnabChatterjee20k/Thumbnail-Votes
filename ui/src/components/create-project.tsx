/**
 * This code was generated by v0 by Vercel.
 * @see https://v0.dev/t/fAndDT4pTOL
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */

/** Add fonts into your Next.js project:

import { Libre_Baskerville } from 'next/font/google'
import { Archivo } from 'next/font/google'

libre_baskerville({
  subsets: ['latin'],
  display: 'swap',
})

archivo({
  subsets: ['latin'],
  display: 'swap',
})

To read more about using these font, please visit the Next.js documentation:
- App Directory: https://nextjs.org/docs/app/building-your-application/optimizing/fonts
- Pages Directory: https://nextjs.org/docs/pages/building-your-application/optimizing/fonts
**/
"use client";

import { ChangeEvent, useState } from "react";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";

import Link from "next/link";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import UserAvatar from "./user-avatar";
import { Slider } from "./ui/slider";
import createProject from "@/app/actions/create-project";
import { useFormStatus } from "react-dom";

interface Project {
  prompt: string;
  name: string;
  count:number;
}

export function CreateProject() {
  const [activeTab, setActiveTab] = useState<"create" | "view" | "stats">(
    "create"
  );
  const [projects, setProjects] = useState<Project[]>([]);
  const [currentProject, setCurrentProject] = useState<Project>({
    prompt: "",
    name: "",
    count:1
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCurrentProject((project) => ({
      ...project,
      [name]: value,
    }));
  };
  const handleTabChange = (value: string) => {
    if (value === "create" || value === "view" || value === "stats") {
      setActiveTab(value);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 lg:p-10 min-h-screen flex flex-col justify-center items-center">
      <div className="flex flex-col gap-6">
        <div className="flex items-center justify-between">
          <div className="grid gap-1">
            <h1 className="text-2xl font-bold">Admin Panel</h1>
            <div className="text-sm text-gray-500 dark:text-gray-400">
              Manage your projects and votes
            </div>
          </div>
          <div className="flex items-center gap-2">
            <UserAvatar />
          </div>
        </div>
        <Tabs value={activeTab} onValueChange={handleTabChange}>
          <TabsList className="bg-zinc-700">
            <TabsTrigger
              value="create"
              className={`${
                activeTab === "create"
                  ? "bg-zinc-800 text-white"
                  : "bg-transparent"
              }`}
            >
              Create Project
            </TabsTrigger>
            <TabsTrigger
              value="view"
              className={`${
                activeTab === "view"
                  ? "bg-zinc-800 text-white"
                  : "bg-transparent"
              }`}
            >
              View Projects
            </TabsTrigger>
            <TabsTrigger
              value="stats"
              className={`${
                activeTab === "stats"
                  ? "bg-zinc-800 text-white"
                  : "bg-transparent"
              }`}
            >
              Project Stats
            </TabsTrigger>
          </TabsList>
          <TabsContent value="create">
            <form className="grid gap-4" action={createProject}>
              <Input
                className="text-black"
                placeholder="Enter the name of your thumbnail collection"
                value={currentProject.name}
                name="name"
                onChange={handleChange}
              />
              <Input
                className="text-black"
                placeholder="Enter a prompt for your project"
                name="prompt"
                value={currentProject.prompt}
                onChange={handleChange}
              />
              <label htmlFor="count">Thumbnail Count - {currentProject.count}</label>
              <Slider id="count" name="count" value={[currentProject.count]} onValueChange={(value)=>setCurrentProject(project=>({...project,count:value[0]}))} defaultValue={[currentProject.count]} max={4} min={1} step={1} className="bg-zinc-700"/>
              <Submit/>
            </form>
          </TabsContent>
          <TabsContent value="view">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {projects.map((project) => (
                <Card key={project.id}>
                  <CardHeader>
                    <CardTitle>{project.prompt}</CardTitle>
                    <CardDescription>
                      Created: {new Date(project.createdAt).toLocaleString()}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => setCurrentProject(project)}
                      >
                        <FilePenIcon className="w-4 h-4" />
                      </Button>
                      <div className="text-sm">
                        {project.votes.length} votes
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
          <TabsContent value="stats">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {projects.map((project) => (
                <Card key={project.id}>
                  <CardHeader>
                    <CardTitle>{project.prompt}</CardTitle>
                    <CardDescription>
                      Created: {new Date(project.createdAt).toLocaleString()}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-col gap-2">
                      {project.votes.map((vote, index) => (
                        <div
                          key={index}
                          className="flex items-center justify-between"
                        >
                          <div className="text-sm">{vote}</div>
                          <div className="text-sm">
                            {project.votes.filter((v) => v === vote).length}{" "}
                            votes
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}

function Submit() {
  const status = useFormStatus();
  return <Button disabled={status.pending}>{status.pending?"Loading....":"Create Project"}</Button>
}

function FilePenIcon(props: any) {
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
      <path d="M12 22h6a2 2 0 0 0 2-2V7l-5-5H6a2 2 0 0 0-2 2v10" />
      <path d="M14 2v4a2 2 0 0 0 2 2h4" />
      <path d="M10.4 12.6a2 2 0 1 1 3 3L8 21l-4 1 1-4Z" />
    </svg>
  );
}

function XIcon(props: any) {
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
      <path d="M18 6 6 18" />
      <path d="m6 6 12 12" />
    </svg>
  );
}
