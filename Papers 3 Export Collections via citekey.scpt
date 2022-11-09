set cout to {}
tell application "Papers 3 (Legacy)"
	repeat with coll in every collection item
		set cout to cout & my get_pubs(coll)
	end repeat
end tell


on get_pubs(coll)
	tell application "Papers 3 (Legacy)"
		set thisColl to {collectionName:coll's name as string}
		
		set childCollections to {}
		
		--		set out to {"Collection: " & coll's name as string}
		log coll's name as string
		repeat with subcoll in coll's every collection item
			set childCollections to childCollections & my get_pubs(subcoll)
		end repeat
		set thisColl to thisColl & {children:childCollections}
		
		set memberPublications to {}
		
		repeat with p in the every publication item of coll
			set tmpCiteKey to the citekey of p
			set tmpTitle to the title of p
			set memberPublications to memberPublications & {{tmpCiteKey, tmpTitle}} 
		end repeat
		set thisColl to thisColl & {entries:memberPublications}
	end tell
	return {thisColl}
end get_pubs


-- Source: https://stackoverflow.com/a/3781066/49663
on write_to_file(this_data, target_file, append_data) -- (string, file path as string, boolean)
	try
		set the target_file to the target_file as text
		set the open_target_file to ¬
			open for access file target_file with write permission
		if append_data is false then ¬
			set eof of the open_target_file to 0
		write this_data to the open_target_file starting at eof as «class utf8»
		close access the open_target_file
		return true
	on error
		try
			close access file target_file
		end try
		return false
	end try
end write_to_file

my write_to_file("var data = ", ((path to desktop folder) as text) & "papers_collections.citekey.json", false)
tell application "JSON Helper"
	set j_out to (make JSON from cout)
	my write_to_file(j_out, ((path to desktop folder) as text) & "papers_collections.citekey.json", true)
end tell
