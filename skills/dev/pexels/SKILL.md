---
name: pexels
description: >
  Pexels — free stock photos and videos via API. Use for UI mockups, client assets, social content,
  landing page imagery. API key already configured. Search by keyword, get download URLs instantly.
---

# Pexels — Stock Photos & Videos

## API Key (Already Configured)
```
API Key: Hgl5gh1pwLYYS5pUNKy4gBEzTCv6NTnChBhWhoIvgNNu8g2IftSq3Fsj
Account: alo@gohalomarketing.com
```

## Setup
```bash
npm install pexels
```
```js
import { createClient } from 'pexels'
const client = createClient('Hgl5gh1pwLYYS5pUNKy4gBEzTCv6NTnChBhWhoIvgNNu8g2IftSq3Fsj')
```

## Core Operations

### Search Photos
```js
// Search
const photos = await client.photos.search({
  query: 'chiropractor clinic',
  per_page: 10,
  orientation: 'landscape', // landscape | portrait | square
  size: 'large', // large | medium | small
})

photos.photos.forEach(photo => {
  console.log(photo.src.large2x) // Full URL
  console.log(photo.src.original)
  console.log(photo.photographer)
  console.log(photo.alt)
})
```

### Search Videos
```js
const videos = await client.videos.search({
  query: 'healthcare professional',
  per_page: 5,
  orientation: 'landscape',
})

videos.videos.forEach(video => {
  // Get best quality file
  const bestFile = video.video_files
    .filter(f => f.quality === 'hd')
    .sort((a, b) => b.width - a.width)[0]
  console.log(bestFile.link) // Download URL
})
```

### Curated Photos (High Quality Picks)
```js
const curated = await client.photos.curated({ per_page: 15 })
```

### Download Photo (Node.js)
```js
import https from 'https'
import fs from 'fs'

async function downloadPhoto(url, filename) {
  return new Promise((resolve) => {
    const file = fs.createWriteStream(filename)
    https.get(url, { headers: { Authorization: API_KEY } }, res => {
      res.pipe(file)
      file.on('finish', resolve)
    })
  })
}

await downloadPhoto(photo.src.large2x, 'hero-image.jpg')
```

### Curl (no code needed)
```bash
# Search photos
curl -H "Authorization: Hgl5gh1pwLYYS5pUNKy4gBEzTCv6NTnChBhWhoIvgNNu8g2IftSq3Fsj" \
  "https://api.pexels.com/v1/search?query=chiropractor&per_page=5" | jq '.photos[].src.large2x'

# Search videos
curl -H "Authorization: Hgl5gh1pwLYYS5pUNKy4gBEzTCv6NTnChBhWhoIvgNNu8g2IftSq3Fsj" \
  "https://api.pexels.com/videos/search?query=healthcare&per_page=3" | jq '.videos[].video_files[0].link'
```

## Search Queries for Our Niches
```
Healthcare/Chiro: "chiropractor", "physical therapy", "spine treatment", "wellness clinic"
Dental: "dentist", "dental clinic", "dental care"
Marketing agency: "business meeting", "marketing team", "office collaboration"
Doctor/practitioner: "doctor patient", "medical consultation", "physician"
Modern office: "modern office", "startup office", "tech workspace"
```

## Best Use Cases for Our Builds
- **Halo landing page** — hero images for each specialty
- **Client portals** — industry-specific imagery per practice
- **AI agency site** — professional team/office photos
- **Social content** — B-roll for Reels
- **UI mockups** — placeholder imagery that actually looks good

## Skill Injection for Codex/Claude Code
```
Use Pexels API for all stock imagery. Key: Hgl5gh1pwLYYS5pUNKy4gBEzTCv6NTnChBhWhoIvgNNu8g2IftSq3Fsj
npm install pexels | createClient(key).photos.search({ query, per_page })
Always use photo.src.large2x for quality. Check photographer attribution.
For videos: filter video_files by quality='hd', sort by width descending.
```
