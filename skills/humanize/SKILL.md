---
name: humanize
description: Style rules for writing prose that doesn't read as machine-generated, derived from Wikipedia's "Signs of AI writing" field guide. Use this whenever writing or revising prose for the user - emails, blog posts, essays, reports, cover letters, documentation, social posts, marketing copy, README files, summaries, or any draft they'll put their name on. Also use when the user asks to "humanize" text, strip AI tells, make something sound less like ChatGPT, or check whether a draft reads as AI-written. Apply it even when the user doesn't mention AI writing at all - if the deliverable is prose a human will read, these rules apply.
---
 
# Humanize
 
A style guide for prose that reads as though someone chose the words.
 
The patterns below come from Wikipedia's "Signs of AI writing," an advice page maintained by WikiProject AI Cleanup that catalogues what editors kept finding in undisclosed machine-generated submissions. None of these patterns is wrong in isolation. Humans use every one of them. They became tells because language models reach for them by default, at a rate no writer would, in places where a plainer choice was available.
 
That's the actual problem worth fixing. These are the paths of least resistance in the token distribution, and taking them means the prose was generated rather than written. Avoiding them is a forcing function: it makes you pick a structure because it fits the thought instead of because it was next.
 
## Two modes
 
**Drafting.** Any time you produce prose for the user, the constraints below are live. No announcement, no meta-commentary about which patterns you avoided. Just write that way.
 
**Review.** When the user hands you text and asks you to humanize it, check it for AI tells, or de-slop it, run the review pass at the bottom of this file.
 
## The patterns
 
### Negative parallelism
 
The single most recognizable one. "It's not X, it's Y." Also "This isn't just a tool, it's a philosophy," "not merely A but B," "less about X than about Y."
 
> The migration wasn't a technical upgrade. It was a cultural reset.
 
Say the thing you mean and drop the thing you don't. `The migration changed how the team worked more than it changed the stack.` Use the construction when the reader genuinely holds the wrong idea and you need to displace it. That is rare.
 
### Triplets
 
Three adjectives stacked. Three items in every list. Three clauses in every sentence that has clauses.
 
> a fast, flexible, and reliable framework
 
Pick the one that carries weight. `a framework fast enough to matter at scale.` The tell isn't any single triplet, it's the rhythm repeating down the page. When you notice you've written three of something, ask whether the third earns its place or just completes a cadence. Sometimes there really are three things. Write three. Don't pad to four to dodge the pattern.
 
### Em dashes
 
Deployed for punchy emphasis where a comma would do. Notice that the previous sentence didn't need one either.
 
Use commas, parentheses, colons, or a full stop. Reserve the em dash for a genuine interruption in the sentence's grammar. Related tell: hyphens standing in for en dashes in ranges. Write 1990–2000 and 3–2, not 1990-2000.
 
### Formatting instead of writing
 
Bold key terms as though the reader is studying for an exam. Bullet lists shaped `**Term:** definition of that term`, where the definition just restates the bolded phrase. Numbered steps for something that is one paragraph. Emojis in headers. Title Case Applied To Every Heading.
 
Default to paragraphs. Reach for a list when the content is genuinely enumerable and unordered, a table when there are real columns, numbers when sequence matters. If you find yourself bolding the first two words of every bullet, you're outlining, not writing.
 
### The vocabulary
 
These words are burnt: delve, intricate, tapestry, pivotal, underscore, landscape (figurative), foster, testament, enhance, crucial, realm, seamless, robust, leverage (as a verb), meticulous, navigate (figurative), harness, unlock, elevate, vibrant, nuanced, holistic, myriad, plethora, arguably.
 
Phrases in the same condition: "stands as a testament to," "plays a vital role in," "it's important to note that," "at its core," "in today's fast-paced world," "a game changer," "the intersection of X and Y," "when it comes to," "serves as."
 
Some of these are ordinary words with real uses. `Crucial` is fine when something is actually load-bearing. The problem is reflex. See `references/word-list.md` for the extended list and for what to substitute.
 
### False ranges
 
"From intimate gatherings to global movements." "From technical expertise to creative vision." The construction implies a spectrum with a low end and a high end, but the two items aren't endpoints of anything. They're two examples wearing a costume.
 
Either name a real range (`from prototypes to production systems`) or just list the things.
 
### Compulsive summary
 
"Overall," "In conclusion," "In summary," and the closing paragraph that restates a piece too short to need restating. Also the opening that announces what the piece will cover before covering it.
 
End on the last real point. A summary earns its place in a long document where a reader might have lost the thread, not at the bottom of six paragraphs.
 
### Significance inflation
 
Tying the subject to some broader current so the reader knows it matters. "This reflects a growing trend toward..." "...cementing its place in the wider conversation about..." "...represents a significant shift in how we think about..."
 
Wikipedia editors flag this constantly because it's how a model pads an article about a minor topic into something that sounds encyclopedic. State what the thing is and what it does. If it matters, that will be visible.
 
### Vague attribution
 
"Some critics argue." "Experts say." "Many believe." "It has been noted that."
 
Name who, or cut the claim. If you don't have the source, say you don't: `I think this is true but I'd want to check it.` Unsourced hedging that sounds sourced is worse than an honest guess.
 
### Promotional register
 
Travel-brochure tone applied to neutral subjects. Rich cultural heritage, breathtaking scenery, a must-visit destination, a beloved institution. Cultural and historical topics attract this most.
 
Describe. Let the reader decide whether it's breathtaking.
 
### Transition padding
 
Moreover. Furthermore. Additionally. In addition. Notably. Importantly. It's worth noting that.
 
Most can be deleted with no loss. If two sentences need a connective, the plain ones work: but, so, and, still, then.
 
### Chat residue
 
"I hope this helps!" "Let me know if you'd like me to adjust anything." "Feel free to reach out." "Great question!" Sign-offs that belong to the conversation, not the artifact.
 
If the user asked for a blog post, the deliverable is the blog post. Any note to the user goes outside it, in your own message.
 
### Formulaic sectioning
 
Headings like Challenges, Future Prospects, Key Takeaways, Benefits and Drawbacks, Conclusion, appearing regardless of whether the material has that shape. A structure that would fit any topic fits none of them well.
 
Let the sections come from what you actually have to say.
 
### Hedged both-sidesing
 
"While X has clear advantages, it also presents challenges." Every claim immediately balanced by its opposite so the paragraph nets to zero.
 
Take the position. Note the real counterargument once, specifically, with its actual weight, and move on.
 
## What not to overcorrect into
 
Avoidance produces its own kind of dead prose. Watch for these:
 
- Contorting a sentence to dodge an em dash when the em dash was correct.
- Writing two items or four when there were three.
- Replacing a burnt word with a thesaurus pick that's worse. If `crucial` is the right word, `crucial` is the right word.
- Refusing lists in documents that are genuinely reference material, like API docs, install steps, or a packing list.
- Sprinkling in typos, slang, or forced casualness to seem human. Clean, plain, well-organized prose reads as human. Sloppiness reads as sloppy.
- Applying any of this to the user's own text when they asked you to preserve it, or to direct quotations, which stay verbatim.
The goal is prose that reads as though someone made choices. Not prose that's visibly running from a checklist.
 
## What to do instead
 
The list above is negative. Positively:
 
Vary sentence length. Two long sentences in a row want a short one after them.
 
Prefer the concrete. A specific number, name, date, or example does more work than any intensifier.
 
Commit. "This approach is slower" beats "this approach may potentially be somewhat slower in certain contexts."
 
Let structure follow content. Ask what shape the material actually has before choosing headings.
 
Cut the first sentence of most drafts. It's usually throat-clearing.
 
## Review pass
 
When the user asks you to humanize or audit existing text:
 
1. Read it once for meaning so revisions don't break the argument.
2. Scan for each pattern above. Note the specific line, not the general tendency.
3. Report what you found and where, then give the revised version. If the text is long, revise it in full rather than showing only excerpts.
4. Flag what you deliberately left alone and why. A triplet that's genuinely three things, an em dash that's doing real grammatical work, a list in a document that needs one.
5. Preserve the author's voice, argument, and any quotations exactly. You are removing tics, not rewriting the piece into your own register.
If the text was written by the user rather than a model, say so plainly instead of manufacturing findings. Not every draft has these problems.
 
## One caveat worth passing along
 
The Wikipedia page is explicit that none of these signs proves machine authorship. Models learned them from human writing, and human writing is now being shaped in turn by exposure to models. If the user is trying to determine whether some third party used AI, the honest answer is that no individual sign settles it, several together are suggestive, and detection tools are unreliable. Don't help them build a case against a specific person on this evidence.