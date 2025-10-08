/**
 * KEYWORD UNIVERSE - Google Docs Generator
 *
 * INSTRUCTIONS:
 * 1. Go to https://script.google.com
 * 2. Click "New Project"
 * 3. Delete the default code
 * 4. Paste this entire script
 * 5. Click "Run" > Select "createKeywordUniverseDoc"
 * 6. Authorize when prompted
 * 7. Check the execution log for the document URL
 * 8. Open the URL to view your formatted document
 */

function createKeywordUniverseDoc() {
  // Create new Google Doc
  const doc = DocumentApp.create('3M Lighting - Keyword Universe');
  const body = doc.getBody();

  // Define colors (Google Docs uses hex format)
  const NAVY = '#0a1628';
  const CHARCOAL = '#2c3e50';
  const STONE = '#5b6773';
  const ACCENT = '#00b4e0';
  const ACCENT_SOFT = '#7cc9e5';

  // Set document-wide styles
  const normalStyle = {};
  normalStyle[DocumentApp.Attribute.FONT_FAMILY] = 'Arial'; // Fallback (GT America/Space Grotesk not available)
  normalStyle[DocumentApp.Attribute.FONT_SIZE] = 11;
  normalStyle[DocumentApp.Attribute.LINE_SPACING] = 1.7;
  normalStyle[DocumentApp.Attribute.FOREGROUND_COLOR] = CHARCOAL;
  body.setAttributes(normalStyle);

  // Helper function to add header
  function addHeader(text, level) {
    const para = body.appendParagraph(text);
    const style = {};

    if (level === 1) {
      style[DocumentApp.Attribute.FONT_SIZE] = 28;
      style[DocumentApp.Attribute.BOLD] = true;
      style[DocumentApp.Attribute.FOREGROUND_COLOR] = NAVY;
      style[DocumentApp.Attribute.SPACING_AFTER] = 8;
    } else if (level === 2) {
      style[DocumentApp.Attribute.FONT_SIZE] = 18;
      style[DocumentApp.Attribute.BOLD] = true;
      style[DocumentApp.Attribute.FOREGROUND_COLOR] = NAVY;
      style[DocumentApp.Attribute.SPACING_BEFORE] = 20;
      style[DocumentApp.Attribute.SPACING_AFTER] = 10;
    } else if (level === 3) {
      style[DocumentApp.Attribute.FONT_SIZE] = 14;
      style[DocumentApp.Attribute.BOLD] = true;
      style[DocumentApp.Attribute.FOREGROUND_COLOR] = NAVY;
      style[DocumentApp.Attribute.SPACING_BEFORE] = 12;
      style[DocumentApp.Attribute.SPACING_AFTER] = 8;
    }

    para.setAttributes(style);
    return para;
  }

  // Helper function to add paragraph
  function addParagraph(text, options = {}) {
    const para = body.appendParagraph(text);
    const style = {};

    style[DocumentApp.Attribute.FONT_SIZE] = options.fontSize || 11;
    style[DocumentApp.Attribute.FOREGROUND_COLOR] = options.color || CHARCOAL;
    style[DocumentApp.Attribute.SPACING_AFTER] = options.spacingAfter || 8;

    if (options.bold) style[DocumentApp.Attribute.BOLD] = true;
    if (options.italic) style[DocumentApp.Attribute.ITALIC] = true;

    para.setAttributes(style);
    return para;
  }

  // Helper function to add table
  function addTable(headers, rows) {
    const tableData = [headers, ...rows];
    const table = body.appendTable(tableData);

    // Style header row
    const headerRow = table.getRow(0);
    for (let i = 0; i < headerRow.getNumCells(); i++) {
      const cell = headerRow.getCell(i);
      cell.setBackgroundColor('#e6f7ff'); // Light cyan background

      const cellStyle = {};
      cellStyle[DocumentApp.Attribute.BOLD] = true;
      cellStyle[DocumentApp.Attribute.FONT_SIZE] = 10;
      cellStyle[DocumentApp.Attribute.FOREGROUND_COLOR] = NAVY;
      cell.editAsText().setAttributes(cellStyle);

      cell.setPaddingTop(8);
      cell.setPaddingBottom(8);
      cell.setPaddingLeft(10);
      cell.setPaddingRight(10);
    }

    // Style data rows
    for (let i = 1; i < table.getNumRows(); i++) {
      const row = table.getRow(i);

      // Alternate row backgrounds
      if (i % 2 === 0) {
        for (let j = 0; j < row.getNumCells(); j++) {
          row.getCell(j).setBackgroundColor('#f9f9f9');
        }
      }

      // Style cells
      for (let j = 0; j < row.getNumCells(); j++) {
        const cell = row.getCell(j);
        const cellStyle = {};
        cellStyle[DocumentApp.Attribute.FONT_SIZE] = 10;
        cellStyle[DocumentApp.Attribute.FOREGROUND_COLOR] = STONE;

        // First column bold
        if (j === 0) {
          cellStyle[DocumentApp.Attribute.BOLD] = true;
          cellStyle[DocumentApp.Attribute.FOREGROUND_COLOR] = CHARCOAL;
        }

        cell.editAsText().setAttributes(cellStyle);
        cell.setPaddingTop(8);
        cell.setPaddingBottom(8);
        cell.setPaddingLeft(10);
        cell.setPaddingRight(10);
      }
    }

    table.setBorderWidth(1);
    table.setBorderColor('#d3d8de');

    return table;
  }

  // Helper function to add note box
  function addNoteBox(text) {
    const para = body.appendParagraph(text);
    const style = {};
    style[DocumentApp.Attribute.FONT_SIZE] = 11;
    style[DocumentApp.Attribute.FOREGROUND_COLOR] = CHARCOAL;
    style[DocumentApp.Attribute.BACKGROUND_COLOR] = '#e6f7ff';
    style[DocumentApp.Attribute.LEFT_TO_RIGHT] = true;
    para.setAttributes(style);
    para.setIndentStart(20);
    para.setIndentEnd(20);
    para.setSpacingBefore(10);
    para.setSpacingAfter(10);
    return para;
  }

  // Helper to add bullet list
  function addBulletList(items) {
    items.forEach(item => {
      const para = body.appendListItem(item);
      para.setGlyphType(DocumentApp.GlyphType.BULLET);
      const style = {};
      style[DocumentApp.Attribute.FONT_SIZE] = 11;
      style[DocumentApp.Attribute.FOREGROUND_COLOR] = STONE;
      para.setAttributes(style);
    });
  }

  // ========================================
  // START BUILDING DOCUMENT
  // ========================================

  // TITLE
  addHeader('Lighting Opportunity Mapping: Keyword Universe', 1);
  addParagraph('Search Criteria for Content Retrieval · Draft for Client Alignment', {
    fontSize: 12,
    color: STONE,
    italic: true,
    spacingAfter: 6
  });

  // META INFO
  addParagraph('Prepared for: 3M Strategic Innovation Office', { fontSize: 10, color: STONE });
  addParagraph('Date: 06 October 2025', { fontSize: 10, color: STONE });
  addParagraph('Document Type: Draft for Client Alignment', { fontSize: 10, color: STONE, spacingAfter: 20 });

  body.appendHorizontalRule();

  // SECTION: What This Document Is
  addHeader('What This Document Is', 2);
  addParagraph('These keywords define the dragnet across Reddit, YouTube, TikTok, Amazon reviews, and other platforms. Before we retrieve thousands of posts and videos, you validate the search terms.');
  addParagraph('What this is NOT: Pain points, jobs, or workarounds. We have not found those yet. These are the words people use when they talk about home lighting. The insights come later.', { bold: true });

  // SECTION: How to Use This
  addHeader('How to Use This', 2);
  addParagraph('1. Review the Universal Keywords (Section 1). These work everywhere.');
  addParagraph('2. Scan Platform-Specific Terms (Section 2). Some words only work on certain platforms.');
  addParagraph('3. Mark your adds/deletes in the sign-off section.');
  addParagraph('4. We refine and execute.');

  // SECTION: Research Questions
  addHeader('Research Questions This Serves', 2);
  addParagraph('Every keyword maps to one or more core questions:');
  addBulletList([
    'What lighting problems do consumers struggle to solve?',
    'What compensating behaviors exist? (hacks, workarounds, makeshift solutions)',
    'Where do 3M products already appear in solutions?',
    'What does success look like when lighting finally works?'
  ]);

  // SECTION 1: Universal Keywords
  addHeader('Section 1: Universal Keywords', 2);
  addParagraph('These terms retrieve relevant content across all platforms. Priority determines budget allocation.');

  addHeader('P0 (Must Include) — Core Functional & Pain Terms', 3);
  addTable(
    ['Category', 'Keywords', 'Why These Matter'],
    [
      ['Functional', 'brightness, dimmable, warm/cool color temperature, LED strip lights, under-cabinet lights, motion sensor lights, smart bulbs, ambient lighting, USB-powered', 'How people describe what they want lighting to do'],
      ['Pain/Frustration', 'flickering, harsh light, glare, too bright, too dim, dark corners, adhesive failure, buzzing', 'Direct problem language—high signal for unmet needs'],
      ['Outcome', 'cozy glow, even illumination, glare-free, energy saving', 'Success-state language—tells us what "working" looks like'],
      ['Workaround/Hack', 'LED strips, dimmer switches, diffusers, filters, Command strips, peel-and-stick', 'Compensating behaviors—signals of product gaps'],
      ['Room/Context', 'kitchen, bedroom, living room, home office, closet, hallway, under cabinets', 'Situational framing—jobs vary by space'],
      ['Installation', 'peel-and-stick adhesive, battery powered, USB, plug-in, no wiring, removable', 'Installation barriers drive product choices']
    ]
  );

  addHeader('P1 (Should Include) — Nuance & Specificity', 3);
  addTable(
    ['Category', 'Keywords', 'Why These Matter'],
    [
      ['Functional', 'color-changing/RGB lights, remote control, voice control, rechargeable, sunset lamp, fairy lights', 'Emerging trends and aesthetic preferences'],
      ['Pain/Frustration', 'uneven lighting, eyestrain, buzzing, adhesive residue, app glitches', 'Secondary pain points with strong engagement'],
      ['Outcome', 'aesthetic vibe, mood lighting, safe navigation at night, productivity boost', 'Emotional and functional outcomes beyond basics'],
      ['Workaround/Hack', 'repositioning fixtures, extra 3M tape, smart plugs, timers, mirrors to reflect light', 'Creative problem-solving—innovation signals'],
      ['Room/Context', 'dorm room, gaming setup, vanity, pantry, garage, stairway', 'Niche spaces with specific needs'],
      ['Installation', 'magnetic mount, cuttable strips, aluminum channels, app control', 'Advanced installation preferences'],
      ['Constraint Language', 'renter-friendly, landlord-approved, damage-free, non-permanent, lease-safe', 'Hypothesis to validate: Removability as decision driver']
    ]
  );

  addNoteBox('Note on Constraint Language: "Renter-friendly" appeared organically in preliminary scans (Reddit, YouTube, Etsy). We are testing whether this is a niche or a mainstream concern. Signal strength will be quantified during retrieval.');

  addHeader('P2 (Nice to Have) — Edge Cases & Trends', 3);
  addTable(
    ['Category', 'Keywords'],
    [
      ['Functional', 'hand-wave sensors, gesture control, cove lighting, wall sconces, track lights'],
      ['Pain/Frustration', 'battery drain, remote lag, connectivity issues'],
      ['Outcome', 'Instagram-ready, plant growth lighting, reading-friendly'],
      ['Workaround/Hack', 'power banks, micro-controllers, stacking fairy lights, jar lighting']
    ]
  );

  // SECTION 2: Platform-Specific Keywords
  addHeader('Section 2: Platform-Specific Keywords', 2);
  addParagraph('Some terms only work on certain platforms. This prevents wasted retrieval.');

  addHeader('Reddit / Forums', 3);
  addParagraph('Why it works: Long-form problem-solving. High signal for technical failures.', { italic: true });
  addTable(
    ['Add to Universal', 'Platform-Specific'],
    [
      ['All P0 + P1 keywords', 'voltage drop, circuit breaker, neutral connection, appliance startup flicker, troubleshooting steps']
    ]
  );
  addParagraph('Filters: ≥10 upvotes, 2023-2025 posts, subreddits: r/HomeImprovement, r/DIY, r/Lighting', { fontSize: 9, color: STONE });

  addHeader('YouTube', 3);
  addParagraph('Why it works: Visual tutorials. High signal for installation methods and product demos.', { italic: true });
  addTable(
    ['Add to Universal', 'Platform-Specific'],
    [
      ['All P0 functional + installation keywords', 'anti-glare products, louvers, color temperature under 3000K, LED-compatible dimmer']
    ]
  );
  addParagraph('Filters: ≥50k views, 2023-2025, comments enabled', { fontSize: 9, color: STONE });

  addHeader('TikTok / Instagram', 3);
  addParagraph('Why it works: Aesthetic transformations. High signal for emotional outcomes and hacks.', { italic: true });
  addTable(
    ['Add to Universal', 'Platform-Specific'],
    [
      ['P0 outcome + workaround keywords', '#DIYLighting, #HomeHacks, cloud ceiling, sunset lamp, behind-TV backlight, RGB, aesthetic room']
    ]
  );
  addParagraph('Filters: ≥100k views (TikTok), ≥10k likes (Instagram), 2023-2025', { fontSize: 9, color: STONE });

  addHeader('Pinterest', 3);
  addParagraph('Why it works: Aspirational ideas. High signal for desired outcomes.', { italic: true });
  addTable(
    ['Add to Universal', 'Platform-Specific'],
    [
      ['P0 outcome keywords', 'floating shelf lights, ceiling perimeter strips, mirror backlighting, neon sign DIY, reading nook']
    ]
  );
  addParagraph('Filters: ≥500 saves, recent pins', { fontSize: 9, color: STONE });

  addHeader('Etsy / Amazon Reviews', 3);
  addParagraph('Why it works: Purchase behavior. High signal for what is working/failing in products.', { italic: true });
  addTable(
    ['Add to Universal', 'Platform-Specific'],
    [
      ['P0 functional + pain keywords', 'weak adhesive, brightness levels, motion sensor sensitivity, battery life, magnetic mount failure']
    ]
  );
  addParagraph('Filters: ≥4 stars (success), ≤2 stars (pain), verified purchase, 2023-2025', { fontSize: 9, color: STONE });

  addHeader('Quora', 3);
  addParagraph('Why it works: Direct questions reveal specific problems.', { italic: true });
  addTable(
    ['Add to Universal', 'Platform-Specific'],
    [
      ['P0 pain keywords', 'how to soften LED glare, advice for renters, buzzing fluorescent lights']
    ]
  );
  addParagraph('Filters: ≥50 upvotes, 2023-2025', { fontSize: 9, color: STONE });

  // SECTION 3: Exclusion Safeguards
  addHeader('Section 3: Exclusion Safeguards', 2);
  addParagraph('What we filter OUT to prevent noise:');
  addBulletList([
    'Commercial/industrial lighting (high-bay, warehouse, office panels)',
    'Automotive/vehicle lighting',
    'Outdoor landscape lighting (except porch/entryway)',
    'Photography/videography lighting (studio, ring lights for filming)',
    'Medical/clinical lighting',
    'Aquarium/terrarium lighting',
    'Plant grow lights (unless home décor context)'
  ]);

  // SECTION 4: Quality Filters
  addHeader('Section 4: Quality Filters', 2);

  addHeader('Engagement Thresholds by Platform', 3);
  addTable(
    ['Platform', 'Minimum Threshold', 'Why'],
    [
      ['Reddit', '≥10 upvotes', 'Filters spam, validates community agreement'],
      ['YouTube', '≥50k views', 'Ensures content reached critical mass'],
      ['TikTok', '≥100k views', 'Viral threshold for trends'],
      ['Instagram', '≥500 likes', 'Meaningful engagement'],
      ['Amazon/Etsy', '≥10 reviews', 'Validates purchase behavior'],
      ['Quora', '≥50 upvotes', 'Expertise validation']
    ]
  );

  addHeader('Date Ranges', 3);
  addParagraph('2023-2025: Captures current LED/smart home tech. Older content risks outdated product references.');

  // SECTION 5: 3M Adjacency Tracking
  addHeader('Section 5: 3M Adjacency Tracking', 2);
  addParagraph('We will flag where these already appear in consumer solutions:');
  addBulletList([
    'Command hooks/strips (mounting, cord management)',
    'Scotch tape (reinforcement, adhesive backup)',
    '3M adhesives (LED strip mounting)',
    '3M films (diffusion, glare reduction—inferred)'
  ]);
  addParagraph('Tracking question: Are consumers already using 3M products to solve lighting problems? Where are the gaps?', { bold: true });

  // CLIENT ACTION ITEMS
  addHeader('Client Action Items', 2);

  addHeader('Your Review Checklist', 3);
  addParagraph('1. Add keywords we missed. What terms does your team use internally that consumers might also use?');
  addParagraph('2. Delete keywords that do not align. If a term does not map to a product opportunity, remove it.');
  addParagraph('3. Flag platform priorities. Which platforms matter most for Command brand insights?');
  addParagraph('4. Confirm renter hypothesis. Should we validate "renter-friendly" language as a distinct market signal?');

  addHeader('Sign-Off', 3);
  addParagraph('Adds: ___________________________________________________________');
  addParagraph('Deletes: ________________________________________________________');
  addParagraph('');
  addParagraph('Platform Priorities (rank 1-3):');
  addParagraph('Reddit: ___   YouTube: ___   TikTok/Instagram: ___   Amazon/Etsy: ___');
  addParagraph('');
  addParagraph('Renter Hypothesis (Y/N):');
  addParagraph('Should we quantify "renter-friendly" signal strength as a potential niche? ___');
  addParagraph('');
  addParagraph('Approved by: _____________________   Date: _____________________');

  body.appendHorizontalRule();

  addParagraph('Next Step: Upon approval, we execute the dragnet and return with categorized content samples for Phase 2 analysis.', {
    bold: true,
    fontSize: 12,
    spacingAfter: 20
  });

  // Log the document URL
  Logger.log('Document created successfully!');
  Logger.log('Document URL: ' + doc.getUrl());
  Logger.log('Document ID: ' + doc.getId());

  // Return doc URL
  return doc.getUrl();
}
