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

!(let $commext (py-str ("./channels/" (commchannel)))
   (progn (println! (py-str ("Loading communication channel extension" $commext)))
          (import! &self (library OmegaClaw-Core $commext))
          (import! &self (library OmegaClaw-Core src/channels))
          ))
