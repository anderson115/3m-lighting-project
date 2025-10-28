#!/bin/bash

echo "=========================================="
echo "DATA COLLECTION PROGRESS SUMMARY"
echo "=========================================="
echo ""

echo "1. WORKBENCHES:"
if [ -f "workbenches_collection.json" ]; then
    count=$(grep -o '"title"' workbenches_collection.json | wc -l)
    echo "   ✓ COMPLETE: $count products collected"
else
    echo "   ⏳ IN PROGRESS..."
fi

echo ""
echo "2. CABINETS:"
if [ -f "cabinets_collection.json" ]; then
    count=$(grep -o '"title"' cabinets_collection.json | wc -l)
    echo "   ✓ COMPLETE: $count products collected"
else
    echo "   ⏳ IN PROGRESS..."
fi

echo ""
echo "3. BINS & CONTAINERS:"
if [ -f "bins_containers_collection.json" ]; then
    count=$(grep -o '"title"' bins_containers_collection.json | wc -l)
    echo "   ✓ COMPLETE: $count products collected"
else
    echo "   ⏳ IN PROGRESS..."
fi

echo ""
echo "4. SHELVING:"
if [ -f "shelving_collection.json" ]; then
    count=$(grep -o '"title"' shelving_collection.json | wc -l)
    echo "   ✓ COMPLETE: $count products collected"
else
    echo "   ⏳ IN PROGRESS..."
fi

echo ""
echo "=========================================="

# Check if all complete
if [ -f "workbenches_collection.json" ] && [ -f "cabinets_collection.json" ] && [ -f "bins_containers_collection.json" ] && [ -f "shelving_collection.json" ]; then
    echo "✅ ALL COLLECTIONS COMPLETE!"

    total=0
    for file in workbenches_collection.json cabinets_collection.json bins_containers_collection.json shelving_collection.json; do
        count=$(grep -o '"title"' "$file" | wc -l)
        total=$((total + count))
    done

    echo "📊 Total new products collected: $total"
else
    echo "⏳ Collections still running..."
    echo "   Estimated time remaining: 20-40 minutes"
fi

echo "=========================================="
