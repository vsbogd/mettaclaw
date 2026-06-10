!(import! &self (library OmegaClaw-Core ./channels/mock.py))

(= (commChannelInit)
   (py-call (mock.start_mock)))

(= (commChannelReceiveMessage)
   (py-call (mock.getLastMessage)))

(= (commChannelSendMessage $msg)
   (py-call (mock.send_message $msg)))
