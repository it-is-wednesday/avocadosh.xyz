Dont forget to run `lastfm_collage_generator` in a cronjob on your server:)

A `.env` file needs to be present with the following fields:
- LASTFM_API_KEY
- LASTFM_API_SECRET
- COLLAGE_TTF (full path to a `.ttf` file)

CV is generated and is available at `/cv.pdf`, `/cv.html`, `/cv.docx`. It's
embarrassing to include a link directly in the website so this is what we have
