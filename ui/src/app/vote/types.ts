export type ProjectType = {
  thumbnails: string[];
  title: string;
  email:string;
};

export type VotingResults = {
  results: {
    [key: string]: string[]; 
  } | {}; 
  voted: boolean;
}

export type VotingResultsOut = {
  [key:string] : number
}