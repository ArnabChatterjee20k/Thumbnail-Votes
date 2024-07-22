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
  messages: string[];
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
  const [messages, setMessages] = useState<string[]>([]);

  const sendMessage: ISocketContext["sendMessage"] = useCallback(
    (msg) => {
      console.log("Send Message", msg);
      if (socket) {
        socket.emit("event:message", { message: msg });
      }
    },
    [socket]
  );

  const upVote = useCallback((thumbnail_id:string) => {
    if(socket){
        socket.emit("vote",JSON.stringify({thumbnail_id}))
    }
  }, [socket]);

  const onMessageRec = useCallback((msg: string) => {
    console.log("From Server Msg Rec", msg);
    const { message } = JSON.parse(msg) as { message: string };
    setMessages((prev) => [...prev, message]);
  }, []);

  useEffect(() => {
    const _socket = io(`http://127.0.0.1:5000?email=${email}&project_id=${project_id}` as string);
    _socket.on("message", onMessageRec);
    _socket.on("disconnect",(msg)=>console.log(msg))

    setSocket(_socket);

    return () => {
      _socket.off("message", onMessageRec);
      _socket.disconnect();
      setSocket(undefined);
    };
  }, []);

  return (
    <SocketContext.Provider
      value={{ sendMessage, messages, project_id, email }}
    >
      {children}
    </SocketContext.Provider>
  );
};
