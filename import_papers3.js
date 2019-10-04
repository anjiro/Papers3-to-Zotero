//Find the paper ID(s) by this title in the library
var find_paper = async function(paper_name)
{
	var s = new Zotero.Search();
	s.libraryID = Zotero.Libraries.userLibraryID;
	s.addCondition('title', 'is', paper_name);
	return await s.search();
};


var add_item = async function(coll_list)
{
	var collname = coll_list.shift().split("Collection: ")[1];
	var coll = new Zotero.Collection();
	coll.name = collname;
	await coll.saveTx();

	for(const item of coll_list)	
	{
		if(Array.isArray(item))
		{
			var sub_coll = await add_item(item);
			sub_coll.parentID = coll.id;
			await sub_coll.saveTx();
		}
		else
		{
			paper_ids = await find_paper(item);			
			for(pid of paper_ids)
			{
				await Zotero.DB.executeTransaction(async function()
				{
					await coll.addItem(pid);
					await coll.save();
				});
			}
		}
	}
	return coll;
}

for(const coll_list of data)
{
	await add_item(coll_list);
}

return "Finished!";
