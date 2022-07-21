# Anime365

Simple quiz app based on posts from /r/AnimeCalendar to use on anime conventions. Work in progress.
Ideally, this will be a self-contained online app that handles the quiz with minimal management.

**Features, as of 2022-07-22:**

* fetch all posts and comments within given range from the subreddit, using Pushshift API.
* store images in files and some metadata in sqlite db - some abnormal cases are handled
* get anime title from comments (Roboragi post)
* some CLI handling
* some work done on qt quiz frontend - needs to be finished before any release

**TODO (in priority order):**

1. Finish quiz module - display images (and hidden answers) - MVP, with this quiz can be carried out, with external
   tools for answering etc.
2. Refactor and clean up everything
3. Create a web app that can handle participants, answers, administration etc., needs specification
