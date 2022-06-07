# Anime365

Simple quiz app based on posts from. /r/Anime365. For now, just collects images from there and stores them. Ideally,
this will be a self-contained online app that handles the quiz with minimal manaagement.

**Features, as of 2022-06-06 (only image collection update module for now):**

* Fetch all posts and comments within given range from the subreddit, using Pushshift API.
* Store images in files and some metadata in sqlite db - some abnormal cases are handled
* Get anime title from comments (Roboragi post)
* some CLI handling

**TODO (in priority order):**

1. Refactor and clean up the update module
2. Create quiz module - display images (and hidden answers) - MVP, with this quiz can be carried out, with external
   tools for answering etc.
3. Create a web app that can handle participants, answers, administration etc., needs specification