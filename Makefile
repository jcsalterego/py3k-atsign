clean:
	find . \
	\( -name '*~' \
	    -or -name '#*#' \
	    -or -name '.DS_Store' \) \
	-exec rm -fv {} \;
