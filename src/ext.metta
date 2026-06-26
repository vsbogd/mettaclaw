; TODO: the main reason of moving loading the extensions loading out of the
; (init... ) functions is that dependency should be loaded before the dependent
; module in PeTTa otherwise the dependency functions will not be callable from
; the dependent module (see https://github.com/trueagi-io/PeTTa/issues/181).
; This module is loaded before loop.metta and thus the extensions API is
; available before loop.metta which is critical to call (initChannels) and
; similar. If #181 is fixed it will be possible to move code below into
; (initChannels) in channels.metta and similar.

;configured at runtime:
(= (commchannel) (empty))
!(configure commchannel irc)

(= (load-commchannel-py $extname)
  (if (== 1 (py-call (ext.commchannel $extname)))
    (progn (add-atom &self (= (commChannelReceiveMessage) (py-call (ext.commChannelReceiveMessage))))
           (add-atom &self (= (commChannelSendMessage $msg) (py-call (ext.commChannelSendMessage $msg))))
           True)
    False))

(= (empty-to-false $x)
   (case $x
     ((() False)
      ($_ True))))


(= (load-commchannel $extname)
   (progn (println! (atom_concat "Loading communication channel extension: " $extname))
          (if (empty-to-false (collapse (import! &self (library OmegaClaw-Core (atom_concat "./channels/" $extname))))) True
          (if (empty-to-false (collapse (import! &self (library OmegaClaw-Core (atom_concat "./extensions/" $extname))))) True
          (if (load-commchannel-py $extname) True
          (progn (println! (atom_concat "Could not load communication channel extension: " $extname))
                 False))))))

!(load-commchannel (commchannel))

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
