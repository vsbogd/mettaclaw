;Connect all the channels:
(= (initChannels)
   (progn (println! "Initializing channels")
          (commChannelInit)))

;Receive the latest user message considering all communication channels:
(= (receive) (commChannelReceiveMessage))

;Send a message to all communication channels:
!(change-state! &lastsend "")
(= (send $msg)
   (if (!= $msg (get-state &lastsend))
       (progn (change-state! &lastsend $msg)
              (let $safemsg (string-replace $msg  "\n" "\\n")
                   (let $temp (cut) (commChannelSendMessage $safemsg))))))

;Search the internet for some information:
(= (search $msg)
   (py-call (websearch.search $msg)))
