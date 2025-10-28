import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";

// Instagram hashtag searches for garage organization consumer insights
const HASHTAGS = [
  "garageorganization",
  "garagemakeover",
  "organizedgarage",
  "garagestorage",
  "garagetransformation",
  "garageideas",
  "dreamgarage"
];

async function scrapeInstagramHashtag(page, hashtag) {
  try {
    console.log(`\n📸 Instagram: #${hashtag}`);

    const url = `https://www.instagram.com/explore/tags/${hashtag}/`;
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 120000 });
    await new Promise(resolve => setTimeout(resolve, 8000));

    // Scroll to load posts
    await page.evaluate(async () => {
      for (let i = 0; i < 4; i++) {
        window.scrollBy(0, window.innerHeight);
        await new Promise(r => setTimeout(r, 1500));
      }
    });
    await new Promise(resolve => setTimeout(resolve, 3000));

    const posts = await page.evaluate(() => {
      const results = [];

      // Instagram post links
      const postLinks = document.querySelectorAll('a[href*="/p/"]');

      const seen = new Set();
      postLinks.forEach((link, idx) => {
        if (idx >= 40) return; // Limit to 40 posts per hashtag

        const href = link.href;
        if (seen.has(href)) return;
        seen.add(href);

        try {
          // Try to get caption from nearby elements
          const parent = link.closest('article') || link.parentElement;
          let caption = '';

          // Look for caption text in various possible locations
          const captionElems = parent?.querySelectorAll('span, div[class*="caption"]');
          if (captionElems) {
            for (const elem of captionElems) {
              const text = elem.textContent?.trim();
              if (text && text.length > 20 && text.length < 500) {
                caption = text;
                break;
              }
            }
          }

          // Get engagement if visible
          let likes = '';
          const likeElem = parent?.querySelector('[aria-label*="like"]');
          if (likeElem) {
            likes = likeElem.getAttribute('aria-label') || '';
          }

          results.push({
            url: href,
            caption: caption,
            engagement: likes,
            platform: 'instagram'
          });
        } catch (e) {
          // Skip failed extractions
        }
      });

      return results;
    });

    console.log(`   ✓ Found ${posts.length} Instagram posts`);
    return posts.map(p => ({ ...p, hashtag: hashtag }));

  } catch (error) {
    console.log(`   ❌ Error: ${error.message.substring(0, 100)}`);
    return [];
  }
}

async function main() {
  console.log("=".repeat(70));
  console.log("INSTAGRAM CONSUMER INSIGHTS COLLECTION");
  console.log("Target: Visual trends, aspirational language, pain points");
  console.log("=".repeat(70));

  const allPosts = [];
  let searchCount = 0;

  for (const hashtag of HASHTAGS) {
    searchCount++;
    console.log(`\n[Hashtag ${searchCount}/${HASHTAGS.length}]`);

    let browser, page;
    try {
      browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
      page = await browser.newPage();

      // Set user agent
      await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

      const posts = await scrapeInstagramHashtag(page, hashtag);
      allPosts.push(...posts);

      await page.close();
      await browser.close();

      console.log(`   Total collected: ${allPosts.length}`);

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
  console.log(`INSTAGRAM COLLECTION COMPLETE`);
  console.log(`${"=".repeat(70)}`);
  console.log(`Total Instagram posts collected: ${allPosts.length}`);

  if (allPosts.length > 0) {
    const output = {
      platform: "Instagram",
      collected_at: new Date().toISOString(),
      purpose: "Visual trends and aspirational consumer language",
      hashtags: HASHTAGS,
      post_count: allPosts.length,
      posts: allPosts
    };

    fs.writeFileSync('instagram_garage_insights.json', JSON.stringify(output, null, 2));
    console.log("\n✓ Saved to instagram_garage_insights.json");
  }

  return allPosts.length;
}

main().then(count => {
  console.log(`\n✅ Collection complete: ${count} Instagram posts analyzed`);
  process.exit(count > 0 ? 0 : 1);
}).catch(err => {
  console.error("❌ Failed:", err.message);
  process.exit(1);
});
