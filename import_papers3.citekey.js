var find_paper_by_citekey = async function(paper_citekey) {
  var s = new Zotero.Search();
  s.libraryID = Zotero.Libraries.userLibraryID;
  s.addCondition('citationKey', 'is', paper_citekey);
  return await s.search();
}

var add_item = async function(coll_obj) {
  
  // Set up a new Collection with this name
  var collname = coll_obj['collectionName'];
  var coll = new Zotero.Collection();
  coll.name = collname
  await coll.saveTx();
  
  // handle any children this collection might have
  if (coll_obj['children'].length > 0) {
    for (const child_coll of coll_obj['children']) {
      var sub_coll = await add_item(child_coll)
      sub_coll.parentID = coll.id;
      await sub_coll.saveTx();
    }
  }
  
  // now manage the actual entries themselves
  for (const this_entry of coll_obj['entries']) {
    // destructure the list
    var this_cite_key = this_entry[0];
    var this_title = this_entry[1]; // we don't actually need this, it just makes debugging easier
    
    paper_ids = await find_paper_by_citekey(this_cite_key)
  	for(pid of paper_ids)
  	{
  		await Zotero.DB.executeTransaction(async function()
  		{
  			await coll.addItem(pid);
  			await coll.save();
  		});
  	}
  }
  
  return coll;
  
}

for(const coll_list of data)
{
	await add_item(coll_list);
}

return "Finished!";
