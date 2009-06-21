clean:
	find . \
	\( -name '*~' \
	    -or -name '#*#' \
	    -or -name '.DS_Store' \) \
	-exec rm -fv {} \;
patch:
	cd py3k && \
	svn diff > ../py3k-atsign.diff

