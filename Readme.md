# Transfer Papers 3 Mac to Zotero

## What is it?

This is a collection of stuff to help you move from Papers 3 to
Zotero. I made it because Papers 3 is no longer being updated, and
ReadCube Papers is not good enough (e.g., missing scripting support
and a decent iPad app).

It consists of three things:

- A script that helps you get your papers from Papers 3 into Zotero,
	including your BibTeX keys
	(forked from [this
	gist](https://gist.github.com/daeh/abc6d46d897b58a657699fa1a408573e))
- A script to extract your collections from Papers 3
- A script to recreate your collections in Zotero

*Note: this procedure will duplicate the way Papers 3 handles
collections, so every paper in a sub-collection will also be in the
parent collection.*

## Prerequisites

- You need to be running Papers 3 on a Mac.
- You need to be running Zotero 5 also on your Mac.
- You should be comfortable with the possibility for failure. I've
	tested this about once, with my own library.
- You need to install [JSON Helper for AppleScript](https://apps.apple.com/gb/app/json-helper-for-applescript/id453114608?mt=12)
	(Mac App Store link)

## How to use it?

It's not a single click process, unfortunately, but it should be
doable.

1. Follow the instructions from the `Papers3_to_Zotero.py`
	 file. That will help you get all of your papers from Papers 3 into
	 Zotero.
2. Make sure Papers 3 is running and you've installed the JSON Helper
	 above. Open `Papers 3 Export Collections.scpt` and run it. This
	 will create a file on your desktop called
	 `papers_collections.json`.
3. In Zotero, open both **Tools→Developer→Error Console** and
	 **Tools→Developer→Run JavaScript**. The Error Console will help you
	 see if anything goes horribly wrong.
4. Copy and paste the contents of `Desktop/papers_collections.json` into the
	 left pane of the Run JavaScript window.
5. Copy and paste the contents of `import_papers3.js` below that.
6. Make sure **Run as async function** is checked.
7. Hit **Run** and sit back and watch.
