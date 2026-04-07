(= (getSkills)
  (let* (($internal (;INTERNAL:
                     "- Remember a particular string such as skills and memories: (remember string_in_quotes)"
                     "- Query long-term embedding memory for skills and memories with short phrases only: (query string_in_quotes)"
                     "- Episodes searches history for episodes around a time stamp, time format is same as in TIME: (episodes time_string_in_quotes)"
                     "- Pin a certain string as short-term working memory item to keep track of task state: (pin string_in_quotes)"))
         ($fileio (;SHELL AND FILE I/O:
                   "- Execute shell command without apostrophe in string, it returns the command output to you: (shell string_in_quotes)"))
         ($comm (;COMMUNICATION CHANNELS:
                 "- Send message to user: (send string_in_quotes)"
                 "- Search the web: (search string_in_quotes)"))
         ($code (;CODE EXECUTION:
                 "- Execute MeTTa expression: (metta sexpression)"
                 "Example to invoke Non-Axiomatic Logic via MeTTa: "
                 "(metta (|- ((--> (× sam garfield) friend) (stv 1.0 0.9))"
                 "           ((--> garfield animal) (stv 1.0 0.9))))"
                 "(metta (|- ((==> (--> (× $1 elephant) eat) (--> $1 ([] dangerous))) (stv 1.0 0.9))"
                 "           ((--> (× tiger elephant) eat) (stv 1.0 0.9))))"
                 "Also: note the $1 for independent variables, and for negated knowledge use (stv 0.0 0.9)"
                 "Additionally |- also works for revision, to merge evidence even when the term of both premises is the same.")))
         (merge-tuples ($internal $fileio (allowed-prompts) $comm $code))))

(= (allowed-skills) (read-file write-file append-file))

(= (allowed-prompts)
   (let* (($allskills (collapse (skills-list)))
          ($allowedskills (filter-atom $allskills is-skill-allowed)))
          (map-atom $allowedskills skills-prompt)))

(= (is-skill-allowed $skill)
   (let $allowedskills (allowed-skills)
        (is-member $skill $allowedskills)))

(= (merge-tuples $tuples)
   (foldl-atom $tuples () append))

(= (skills-list) (empty))

!(import_prolog_functions_from_file (library mettaclaw ./src/skills.pl) (shell first_char))

(= (metta $str)
   (let $code (sread $str)
        (eval $code)))
