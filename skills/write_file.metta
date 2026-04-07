(= (skills-list) write-file)

(= (skills-prompt write-file)
    "- Write string to file: (write-file filename_in_quotes string_in_quotes)")

(= (write-file $file $str)
   (progn (translatePredicate (open $file write $Out))
          (translatePredicate (write $Out $str))
          (translatePredicate (close $Out))
          True))
