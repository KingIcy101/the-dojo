# Analytics Loop — Postiz API

## Connecting Posts to TikTok Video IDs

After the user publishes from their TikTok inbox, the post needs to be connected to its TikTok video ID before per-post analytics work.

### ⚠️ CRITICAL: Wait at least 2 hours after publishing

TikTok's API has an indexing delay. If you try to connect immediately, the new video won't be in the list yet, and you might connect to the wrong video. This mistake is hard to undo.

### How the Matching Works

1. TikTok video IDs are sequential integers (e.g. `7605531854921354518`, `7605630185727118614`)
2. Higher number = more recently published
3. Sort both Postiz posts (by publish date) and TikTok IDs (numerically) in the same order
4. Match them up: oldest post → lowest unconnected ID, newest post → highest unconnected ID
5. This is reliable because both Postiz and TikTok maintain chronological order

### The Connection Script

`scripts/check-analytics.js --config tiktok-marketing/config.json --days 3 --connect`

The script:
1. Fetches all Postiz posts from the last N days
2. Skips posts published less than 2 hours ago (indexing delay)
3. For unconnected posts, calls `GET /posts/{id}/missing` to get all TikTok videos on the account
4. Matches posts to videos chronologically
5. Excludes already-connected video IDs to avoid duplicates
6. Connects each post via `PUT /posts/{id}/release-id`
7. Pulls per-post analytics (views, likes, comments, shares)

### Manual Connection

If needed:
- `GET /posts/{id}/missing` — returns all TikTok videos with thumbnail URLs
- Identify the correct video by thumbnail or timing
- `PUT /posts/{id}/release-id` with `{"releaseId": "tiktok-video-id"}`
- `GET /analytics/post/{id}` now returns views/likes/comments/shares

### ⚠️ Known Issue: Release ID Cannot Be Overwritten

Once a Postiz post is connected to a TikTok video ID via `PUT /posts/{id}/release-id`, it **cannot be changed**. If you connect the wrong video, the analytics will permanently show the wrong video's stats for that post.

**Best practice:**
1. Post as draft → user publishes with music
2. Wait at least 2 hours (the daily morning cron handles this naturally)
3. The newest unconnected TikTok video ID (highest number) corresponds to the most recently published video
4. Always verify: the number of unconnected Postiz posts should match the number of new TikTok video IDs
5. If something looks wrong, ask the user to confirm by checking the video thumbnail

## Postiz API Endpoints

### Per-Post Analytics
```
GET /analytics/post/{id}
Response: { views, likes, comments, shares }
```

### Platform Analytics
```
GET /analytics/platform/{integrationId}?period=7d
Response: { followers, impressions, engagement, ... }
```

### List Posts
```
GET /posts?limit=50&offset=0
Response: { posts: [...] }
```

### Get Missing Releases
```
GET /posts/{id}/missing
Response: { videos: [{ id, thumbnail, ... }] }
```

### Connect Release ID
```
PUT /posts/{id}/release-id
Body: { "releaseId": "tiktok-video-id" }
```
