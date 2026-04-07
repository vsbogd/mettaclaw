(= (skills-list) read-file)

(= (skills-prompt read-file)
    "- Read file to string: (read-file filename_in_quotes)")

(= (read-file $file)
   (progn (translatePredicate (exists_file $file))
          (translatePredicate (read_file_to_string $file $content ()))
          $content))
