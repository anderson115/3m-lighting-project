import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";

// EXPANDED cabinet searches - additional queries to reach 10%+ coverage
const RETAILERS = [
  {
    name: "Lowes",
    searches: [
      "steel storage cabinet",
      "garage wall cabinet",
      "tool storage cabinet",
      "NewAge garage cabinet",
      "2-door storage cabinet",
      "lockable storage cabinet"
    ],
    baseUrl: "https://www.lowes.com/search?searchTerm=",
    urlPattern: "/pd/"
  },
  {
    name: "Home Depot",
    searches: [
      "steel cabinet garage",
      "tall garage cabinet",
      "cabinet with drawers garage",
      "freestanding garage cabinet",
      "workshop cabinet",
      "industrial cabinet"
    ],
    baseUrl: "https://www.homedepot.com/s/",
    urlPattern: "/p/"
  },
  {
    name: "Walmart",
    searches: [
      "steel cabinet storage",
      "lockable cabinet",
      "workshop storage cabinet",
      "2 door cabinet garage",
      "freestanding cabinet"
    ],
    baseUrl: "https://www.walmart.com/search?q=",
    urlPattern: "/ip/"
  }
];

const MAX_PRODUCTS = 100;

async function extractProducts(page, retailer, query) {
  try {
    console.log(`\n🔍 ${retailer.name}: "${query}"`);

    const searchUrl = `${retailer.baseUrl}${encodeURIComponent(query)}`;
    await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 120000 });
    await new Promise(resolve => setTimeout(resolve, 6000));

    await page.evaluate(async () => {
      for (let i = 0; i < 3; i++) {
        window.scrollBy(0, window.innerHeight);
        await new Promise(r => setTimeout(r, 1000));
      }
    });
    await new Promise(resolve => setTimeout(resolve, 2000));

    const products = await page.evaluate((urlPattern, maxItems) => {
      const results = [];
      const productLinks = Array.from(document.querySelectorAll(`a[href*="${urlPattern}"]`));

      const seen = new Set();
      const uniqueLinks = productLinks.filter(link => {
        const href = link.href;
        if (seen.has(href)) return false;
        seen.add(href);
        return true;
      });

      for (let i = 0; i < Math.min(uniqueLinks.length, maxItems); i++) {
        const link = uniqueLinks[i];
        const url = link.href;

        let title = '';
        let sku = '';

        if (urlPattern === '/pd/') {
          const match = url.match(/\/pd\/([^/]+)\/(\d+)/);
          if (match) {
            title = match[1].replace(/-/g, ' ');
            sku = match[2];
          }
        } else if (urlPattern === '/p/') {
          const match = url.match(/\/p\/([^/]+)\/(\d+)/);
          if (match) {
            title = match[1].replace(/-/g, ' ');
            sku = match[2];
          }
        } else if (urlPattern === '/ip/') {
          const match = url.match(/\/ip\/([^/]+)\/(\d+)/);
          if (match) {
            title = match[1].replace(/-/g, ' ');
            sku = match[2];
          }
        }

        if (title.length < 10) continue;

        const titleLower = title.toLowerCase();

        // Must be cabinet/locker/storage unit
        if (!titleLower.includes('cabinet') &&
            !titleLower.includes('locker') &&
            !(titleLower.includes('storage') && (titleLower.includes('unit') || titleLower.includes('system')))) {
          continue;
        }

        // Skip medicine cabinets, bathroom cabinets, kitchen cabinets
        if (titleLower.includes('medicine') ||
            titleLower.includes('bathroom') ||
            titleLower.includes('kitchen') ||
            titleLower.includes('vanity')) {
          continue;
        }

        results.push({
          title,
          link: url,
          sku,
          price: null,
          brand: null,
          rating: null,
          reviews: null
        });
      }

      return results;
    }, retailer.urlPattern, MAX_PRODUCTS);

    console.log(`   ✓ Found ${products.length} cabinet products`);
    return products.map(p => ({ ...p, retailer: retailer.name, search_query: query }));

  } catch (error) {
    console.log(`   ❌ Error: ${error.message.substring(0, 100)}`);
    return [];
  }
}

async function main() {
  console.log("=".repeat(70));
  console.log("EXPANDED CABINET COLLECTION - Target: +150 products");
  console.log("=".repeat(70));

  const allProducts = [];
  const seenUrls = new Set();
  let totalSearches = 0;

  for (const retailer of RETAILERS) {
    totalSearches += retailer.searches.length;
  }

  let searchCount = 0;

  for (const retailer of RETAILERS) {
    console.log(`\n${"=".repeat(70)}`);
    console.log(`RETAILER: ${retailer.name.toUpperCase()}`);
    console.log(`${"=".repeat(70)}`);

    for (const query of retailer.searches) {
      searchCount++;
      console.log(`\n[Search ${searchCount}/${totalSearches}]`);

      let browser, page;
      try {
        browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
        page = await browser.newPage();

        const products = await extractProducts(page, retailer, query);

        let newCount = 0;
        for (const product of products) {
          if (!seenUrls.has(product.link)) {
            seenUrls.add(product.link);
            allProducts.push(product);
            newCount++;
          }
        }

        await page.close();
        await browser.close();

        console.log(`   New unique: ${newCount}, Total: ${allProducts.length}`);

        if (searchCount < totalSearches) {
          console.log(`   Waiting 10 seconds...`);
          await new Promise(resolve => setTimeout(resolve, 10000));
        }

      } catch (error) {
        console.log(`   Session error: ${error.message.substring(0, 100)}`);
        try { if (page) await page.close(); } catch {}
        try { if (browser) await browser.close(); } catch {}
      }
    }
  }

  console.log(`\n${"=".repeat(70)}`);
  console.log(`EXPANDED CABINET COLLECTION COMPLETE`);
  console.log(`${"=".repeat(70)}`);
  console.log(`Total unique cabinets: ${allProducts.length}`);

  const byRetailer = {};
  allProducts.forEach(p => {
    byRetailer[p.retailer] = (byRetailer[p.retailer] || 0) + 1;
  });

  console.log("\nBy Retailer:");
  for (const [retailer, count] of Object.entries(byRetailer)) {
    console.log(`  ${retailer}: ${count} products`);
  }

  if (allProducts.length > 0) {
    const output = {
      category: "Cabinets (Expanded)",
      collected_at: new Date().toISOString(),
      method: "expanded_search_queries",
      retailers: RETAILERS.map(r => r.name),
      product_count: allProducts.length,
      products: allProducts
    };

    fs.writeFileSync('cabinets_expanded_collection.json', JSON.stringify(output, null, 2));
    console.log("\n✓ Saved to cabinets_expanded_collection.json");
  }

  return allProducts.length;
}

main().then(count => {
  console.log(`\n✅ Expanded collection complete: ${count} unique cabinet products`);
  process.exit(count > 0 ? 0 : 1);
}).catch(err => {
  console.error("❌ Failed:", err.message);
  process.exit(1);
});
