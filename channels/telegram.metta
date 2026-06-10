!(import! &self (library OmegaClaw-Core ./channels/telegram.py))

(= (TG_CHAT_ID) (empty))
(= (TG_POLL_TIMEOUT) (empty))

(= (commChannelInit)
   (progn (configure TG_CHAT_ID "")
          (configure TG_POLL_TIMEOUT 20)
          (py-call (telegram.start_telegram (TG_CHAT_ID) (TG_POLL_TIMEOUT)))))

(= (commChannelReceiveMessage)
   (py-call (telegram.getLastMessage)))

(= (commChannelSendMessage $msg)
   (py-call (telegram.send_message $msg)))
