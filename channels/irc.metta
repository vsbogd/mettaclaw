!(import! &self (library OmegaClaw-Core ./channels/irc.py))

(= (IRC_channel) (empty))
(= (IRC_server) (empty))
(= (IRC_port) (empty))
(= (IRC_user) (empty))

(= (commChannelInit)
   (progn (configure IRC_channel ##omegaclaw)
          (configure IRC_server "irc.quakenet.org")
          (configure IRC_port 6667)
          (configure IRC_user omegaclaw)
          (py-call (irc.start_irc (IRC_channel) (IRC_server) (IRC_port) (IRC_user)))))

(= (commChannelReceiveMessage)
   (py-call (irc.getLastMessage)))

(= (commChannelSendMessage $msg)
   (py-call (irc.send_message $msg)))
