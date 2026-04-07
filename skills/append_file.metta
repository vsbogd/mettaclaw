(= (skills-list) append-file)

(= (skills-prompt append-file)
    "- Append line to file: (append-file filename_in_quotes string_in_quotes)")

(= (append-file $file $str)
   (progn (translatePredicate (exists_file $file))
          (translatePredicate (open $file append $Out))
          (translatePredicate (write $Out $str))
          (translatePredicate (nl $Out)),
          (translatePredicate (close $Out))
          True))
