!(import! &self (library OmegaClaw-Core ./channels/slack.py))

(= (SL_CHANNEL_ID) (empty))
(= (SL_POLL_INTERVAL) (empty))

(= (commChannelInit)
   (progn (configure SL_CHANNEL_ID "")
          (configure SL_POLL_INTERVAL 60)
          (py-call (slack.start_slack (SL_CHANNEL_ID) (SL_POLL_INTERVAL)))))

(= (commChannelReceiveMessage)
   (py-call (slack.getLastMessage)))

(= (commChannelSendMessage $msg)
   (py-call (slack.send_message $msg)))
