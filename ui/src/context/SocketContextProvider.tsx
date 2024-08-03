"use client";
import React, {
  createContext,
  useContext,
  useCallback,
  useState,
  useEffect,
} from "react";
import { io, Socket } from "socket.io-client";

interface ISocketContext {
  sendMessage: (msg: string) => any;
  votes: Record<string,number>;
  project_id: number;
  email: string;
}
interface SocketProviderProps {
  children?: React.ReactNode;
  project_id: number;
  email: string;
}
const SocketContext = createContext<ISocketContext | null>(null);

export const useSocket = () => {
  const state = useContext(SocketContext);
  if (!state) throw new Error(`state is undefined`);

  return state;
};

export const SocketContextProvider: React.FC<SocketProviderProps> = ({
  children,
  project_id,
  email,
}) => {
  const [socket, setSocket] = useState<Socket>();
  const [votes,setVotes] = useState<Record<string,number>>({});
  const sendMessage: ISocketContext["sendMessage"] = useCallback(
    (msg) => {
      console.log("Send Message", msg);
      if (socket) {
        socket.emit("event:message", { message: msg });
      }
    },
    [socket]
  );

  const onVoteStatus = useCallback((msg: Record<string,number>) => {
    console.log({msg})
    if(msg){
      if(msg)setVotes(msg)
    }
  }, []);

  useEffect(() => {
    const _socket = io(`http://127.0.0.1:5000?email=${email}&project_id=${project_id}` as string);
    _socket.on("vote_status", onVoteStatus);
    console.log(_socket.connected)
    _socket.on("disconnect",(msg)=>console.log(msg))
    _socket.onAny((eventName, ...args) => {
      const logMessage = `Received '${eventName}' with data: ${JSON.stringify(args)}`;
      console.log(logMessage);
    });

    setSocket(_socket);

    return () => {
      _socket.off("vote_status", onVoteStatus);
      _socket.disconnect();
      setSocket(undefined);
    };
  }, []);

  return (
    <SocketContext.Provider
      value={{ sendMessage, votes, project_id, email }}
    >
      {children}
    </SocketContext.Provider>
  );
};
