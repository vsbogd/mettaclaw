!(import! &self (library OmegaClaw-Core ./channels/mattermost.py))

(= (MM_URL) (empty))
(= (MM_CHANNEL_ID) (empty))

(= (commChannelInit)
   (progn (configure MM_URL "https://chat.singularitynet.io")
          (configure MM_CHANNEL_ID "8fjrmabjx7gupy7e5kjznpt5qh")
          (py-call (mattermost.start_mattermost (MM_URL) (MM_CHANNEL_ID)))))

(= (commChannelReceiveMessage)
   (py-call (mattermost.getLastMessage)))

(= (commChannelSendMessage $msg)
   (py-call (mattermost.send_message $msg)))
