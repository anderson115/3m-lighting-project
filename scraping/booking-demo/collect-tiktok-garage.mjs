import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";

// TikTok hashtag searches for garage organization consumer insights
const HASHTAGS = [
  "garageorganization",
  "garagemakeover",
  "garagehacks",
  "garagestorage",
  "garagetransformation",
  "organizedgarage",
  "garageideas",
  "garagediy"
];

async function scrapeTikTokHashtag(page, hashtag) {
  try {
    console.log(`\n🎵 TikTok: #${hashtag}`);

    const url = `https://www.tiktok.com/tag/${hashtag}`;
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 120000 });
    await new Promise(resolve => setTimeout(resolve, 8000));

    // Scroll to load videos
    await page.evaluate(async () => {
      for (let i = 0; i < 5; i++) {
        window.scrollBy(0, window.innerHeight);
        await new Promise(r => setTimeout(r, 1500));
      }
    });
    await new Promise(resolve => setTimeout(resolve, 3000));

    const videos = await page.evaluate(() => {
      const results = [];

      // TikTok video elements
      const videoElements = document.querySelectorAll('[data-e2e="search-card-item"], [data-e2e="challenge-item"]');

      videoElements.forEach((elem, idx) => {
        if (idx >= 30) return; // Limit to 30 videos per hashtag

        try {
          // Extract video description/caption
          const descElem = elem.querySelector('[data-e2e="search-card-desc"], [data-e2e="browse-video-desc"]');
          const desc = descElem ? descElem.textContent.trim() : '';

          // Extract author
          const authorElem = elem.querySelector('[data-e2e="search-card-user-unique-id"]');
          const author = authorElem ? authorElem.textContent.trim() : '';

          // Extract view/like counts if visible
          const statsElem = elem.querySelector('[data-e2e="search-card-like-count"]');
          const likes = statsElem ? statsElem.textContent.trim() : '';

          if (desc && desc.length > 10) {
            results.push({
              description: desc,
              author: author,
              likes: likes,
              platform: 'tiktok'
            });
          }
        } catch (e) {
          // Skip failed extractions
        }
      });

      return results;
    });

    console.log(`   ✓ Found ${videos.length} TikTok videos`);
    return videos.map(v => ({ ...v, hashtag: hashtag }));

  } catch (error) {
    console.log(`   ❌ Error: ${error.message.substring(0, 100)}`);
    return [];
  }
}

async function main() {
  console.log("=".repeat(70));
  console.log("TIKTOK CONSUMER INSIGHTS COLLECTION");
  console.log("Target: Consumer language, trends, pain points from TikTok");
  console.log("=".repeat(70));

  const allVideos = [];
  let searchCount = 0;

  for (const hashtag of HASHTAGS) {
    searchCount++;
    console.log(`\n[Hashtag ${searchCount}/${HASHTAGS.length}]`);

    let browser, page;
    try {
      browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
      page = await browser.newPage();

      // Set user agent to avoid bot detection
      await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

      const videos = await scrapeTikTokHashtag(page, hashtag);
      allVideos.push(...videos);

      await page.close();
      await browser.close();

      console.log(`   Total collected: ${allVideos.length}`);

      if (searchCount < HASHTAGS.length) {
        console.log(`   Waiting 12 seconds...`);
        await new Promise(resolve => setTimeout(resolve, 12000));
      }

    } catch (error) {
      console.log(`   Session error: ${error.message.substring(0, 100)}`);
      try { if (page) await page.close(); } catch {}
      try { if (browser) await browser.close(); } catch {}
    }
  }

  console.log(`\n${"=".repeat(70)}`);
  console.log(`TIKTOK COLLECTION COMPLETE`);
  console.log(`${"=".repeat(70)}`);
  console.log(`Total TikTok videos collected: ${allVideos.length}`);

  if (allVideos.length > 0) {
    const output = {
      platform: "TikTok",
      collected_at: new Date().toISOString(),
      purpose: "Consumer language and trend analysis",
      hashtags: HASHTAGS,
      video_count: allVideos.length,
      videos: allVideos
    };

    fs.writeFileSync('tiktok_garage_insights.json', JSON.stringify(output, null, 2));
    console.log("\n✓ Saved to tiktok_garage_insights.json");
  }

  return allVideos.length;
}

main().then(count => {
  console.log(`\n✅ Collection complete: ${count} TikTok videos analyzed`);
  process.exit(count > 0 ? 0 : 1);
}).catch(err => {
  console.error("❌ Failed:", err.message);
  process.exit(1);
});
